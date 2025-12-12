# app/routes/movies.py
from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.responses import Response
from starlette import status
from pymongo.errors import DuplicateKeyError
from typing import List
from app.schemas.movie import MovieCreate, MovieUpdate, MovieResponse
from app.dependencies import get_current_user
from app.db import db
from bson import ObjectId
from datetime import datetime
from pydantic import BaseModel, Field

router = APIRouter(prefix="/movies", tags=["Movies"])

def _normalize(doc: dict) -> dict:
    doc = dict(doc)
    doc["id"] = str(doc["_id"])
    doc.pop("_id", None)
    # rimuovo eventuale campo interno usato dalla pipeline
    doc.pop("_prio", None)
    return doc

class ProgressUpdate(BaseModel):
    season: int = Field(..., ge=1)
    episode: int = Field(..., ge=1)

@router.post("/", response_model=MovieResponse, status_code=201)
async def add_movie(movie: MovieCreate, user=Depends(get_current_user)):
    movie_dict = movie.dict(exclude_unset=True)
    movie_dict["kind"] = movie_dict.get("kind") or "movie"
    movie_dict["user_id"] = str(user["_id"])
    now = datetime.utcnow()
    movie_dict["created_at"] = now
    movie_dict["updated_at"] = now

    try:
        result = await db["movies"].insert_one(movie_dict)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail="Questo titolo è già presente nella tua collezione."
        )
    new_movie = await db["movies"].find_one({"_id": result.inserted_id})
    
    # --- SOCIAL ACTIVITY ---
    try:
        activity = {
            "user_id": str(user["_id"]),
            "username": user.get("username") or user["email"].split("@")[0],
            "type": "add_movie",
            "content": f"ha aggiunto {new_movie['title']} alla sua lista.",
            "movie_id": str(new_movie["_id"]),
            "movie_title": new_movie["title"],
            "movie_poster": new_movie.get("poster_url"),
            "movie_score": new_movie.get("score"),
            "created_at": datetime.utcnow()
        }
        await db["activities"].insert_one(activity)
    except Exception as e:
        print(f"Social activity error: {e}")
    # -----------------------

    return _normalize(new_movie)


@router.get("/random", response_model=MovieResponse)
async def get_random_movie(
    user=Depends(get_current_user),
    status: str = Query("to_watch", regex="^(to_watch|watched|upcoming|watching)$"),
    kind: str | None = Query(None, regex="^(movie|tv)$"),
):
    """
    Restituisce un film a caso dalla lista dell'utente, filtrato opzionalmente per status (default=to_watch) e kind.
    """
    uid = str(user["_id"])
    match_stage = {"user_id": uid, "status": status}
    
    if kind:
        if kind == "movie":
            match_stage["$or"] = [{"kind": "movie"}, {"kind": {"$exists": False}}]
        else:
            match_stage["kind"] = "tv"

    pipeline = [
        {"$match": match_stage},
        {"$sample": {"size": 1}}
    ]
    
    docs = await db["movies"].aggregate(pipeline).to_list(length=1)
    if not docs:
        raise HTTPException(status_code=404, detail="Nessun titolo trovato con questi criteri.")
    
    return _normalize(docs[0])



@router.get("/stats")
async def movies_stats(user=Depends(get_current_user)):
    """
    Statistiche complete per l'utente corrente.
    Calcolate a DB (no dipendenza dall'infinite scroll).
    """
    uid = str(user["_id"])

    # counts per tipo
    total_movies = await db["movies"].count_documents({
        "user_id": uid,
        "$or": [{"kind": "movie"}, {"kind": {"$exists": False}}]
    })
    total_series = await db["movies"].count_documents({"user_id": uid, "kind": "tv"})

    # counts per stato
    watched     = await db["movies"].count_documents({"user_id": uid, "status": "watched"})
    to_watch    = await db["movies"].count_documents({"user_id": uid, "status": "to_watch"})
    upcoming    = await db["movies"].count_documents({"user_id": uid, "status": "upcoming"})
    watching    = await db["movies"].count_documents({"user_id": uid, "status": "watching"})

    # media score (solo valori numerici validi 1..10)
    pipeline = [
        {"$match": {
            "user_id": uid,
            "score": {"$type": "number", "$gte": 1, "$lte": 10}
        }},
        {"$group": {"_id": None, "avg": {"$avg": "$score"}}}
    ]
    agg = await db["movies"].aggregate(pipeline).to_list(length=1)
    avg_score = round(agg[0]["avg"], 1) if agg else None

    # --- AGGREGAZIONI AVANZATE ---
    
    # 1. Top Directors (Top 5)
    dir_pipeline = [
        {"$match": {"user_id": uid, "director": {"$ne": None}}},
        {"$group": {"_id": "$director", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ]
    top_directors = await db["movies"].aggregate(dir_pipeline).to_list(length=5)
    
    # 2. Release Years Distribution (Ultimi 50 anni, raggruppati)
    # Per semplicità restituiamo raw list, il frontend raggruppa
    year_pipeline = [
        {"$match": {"user_id": uid, "release_year": {"$type": "number"}}},
        {"$group": {"_id": "$release_year", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}} # ordine cronologico
    ]
    years_dist = await db["movies"].aggregate(year_pipeline).to_list(length=100)

    # 3. Score Distribution
    score_pipeline = [
        {"$match": {"user_id": uid, "score": {"$type": "number"}}},
        {"$group": {"_id": "$score", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    scores_dist = await db["movies"].aggregate(score_pipeline).to_list(length=11)

    return {
        "total_movies": total_movies,
        "total_series": total_series,
        "watched": watched,
        "to_watch": to_watch,
        "upcoming": upcoming,
        "watching": watching,
        "avg_score": avg_score,
        "stats_advanced": {
            "directors": [{"name": x["_id"], "count": x["count"]} for x in top_directors],
            "years": [{"year": x["_id"], "count": x["count"]} for x in years_dist],
            "scores": [{"score": x["_id"], "count": x["count"]} for x in scores_dist],
        }
    }



@router.get("/{movie_id}", response_model=MovieResponse)
async def get_movie(movie_id: str, user=Depends(get_current_user)):
    m = await db["movies"].find_one({"_id": ObjectId(movie_id), "user_id": str(user["_id"])})
    if not m:
        raise HTTPException(status_code=404, detail="Movie not found")
    return _normalize(m)

@router.get("/", response_model=List[MovieResponse])
async def list_movies(
    user=Depends(get_current_user),
    status: str | None = Query(None, regex="^(to_watch|watched|upcoming|watching)$"),
    q: str | None = None,
    kind: str | None = Query(None, regex="^(movie|tv)$"),
    limit: int = Query(100, le=1000),
    skip: int = Query(0, ge=0),
    sort: str = Query("created_at_desc"),
    # priorità in alto (come già fatto)
    priority_status: str | None = Query(None, regex="^(to_watch|watched|upcoming|watching)$"),
    # 👇 NUOVO: spinge questo status in fondo
    push_last_status: str | None = Query(None, regex="^(to_watch|watched|upcoming|watching)$"),
):
    and_clauses = [{"user_id": str(user["_id"])}]
    if status:
        and_clauses.append({"status": status})

    if kind:
        if kind == "movie":
            and_clauses.append({"$or": [{"kind": "movie"}, {"kind": {"$exists": False}}]})
        else:
            and_clauses.append({"kind": "tv"})

    if q:
        like = {"$regex": q, "$options": "i"}
        and_clauses.append({"$or": [{"title": like}, {"note": like}]})

    filt = {"$and": and_clauses} if len(and_clauses) > 1 else and_clauses[0]

    # ordinamento base
    if sort == "title_asc":
        tail_sort = {"title": 1, "created_at": -1}
        sort_spec = [("title", 1)]
    elif sort == "score_desc":
        tail_sort = {"score": -1, "created_at": -1}
        sort_spec = [("score", -1), ("created_at", -1)]
    else:
        tail_sort = {"created_at": -1}
        sort_spec = [("created_at", -1)]

    need_pipeline = bool(priority_status or push_last_status)

    if need_pipeline:
        sort_stage = {}
        # priorità in alto
        if priority_status:
            sort_stage["_head"] = 1  # 0 = priorità, 1 = resto
        # push in fondo
        if push_last_status:
            sort_stage["_tail"] = 1  # 0 = non push-last, 1 = push-last

        # aggiungo sort tail
        sort_stage.update(tail_sort)

        add_fields = {}
        if priority_status:
            add_fields["_head"] = {
                "$cond": [{"$eq": ["$status", priority_status]}, 0, 1]
            }
        if push_last_status:
            add_fields["_tail"] = {
                "$cond": [{"$eq": ["$status", push_last_status]}, 1, 0]
            }

        pipeline = [
            {"$match": filt},
            {"$addFields": add_fields} if add_fields else {"$match": filt},
            {"$sort": sort_stage},
            {"$skip": skip},
            {"$limit": limit},
        ]
        cursor = db["movies"].aggregate(pipeline)
        docs = await cursor.to_list(length=limit)
    else:
        cursor = db["movies"].find(filt).sort(sort_spec).skip(skip).limit(limit)
        docs = await cursor.to_list(length=limit)

    # normalizza e rimuovi flag interni
    out = []
    for d in docs:
        d.pop("_head", None)
        d.pop("_tail", None)
        out.append(_normalize(d))
    return out


@router.put("/{movie_id}", response_model=MovieResponse)
async def update_movie(movie_id: str, movie: MovieUpdate, user=Depends(get_current_user)):
    update_doc = {
        "$set": movie.dict(exclude_unset=True),
        "$currentDate": {"updated_at": True},
    }
    res = await db["movies"].update_one(
        {"_id": ObjectId(movie_id), "user_id": str(user["_id"])},
        update_doc
    )
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Movie not found")
    updated = await db["movies"].find_one({"_id": ObjectId(movie_id)})
    return _normalize(updated)


@router.put("/{movie_id}/progress", response_model=MovieResponse)
async def update_progress(
    movie_id: str,
    payload: ProgressUpdate,
    user=Depends(get_current_user),
):
    # verifica esistenza item dell'utente
    m = await db["movies"].find_one({"_id": ObjectId(movie_id), "user_id": str(user["_id"])})
    if not m:
        raise HTTPException(status_code=404, detail="Movie not found")

    # opzionale: verifica che sia una serie
    if m.get("kind") != "tv":
         raise HTTPException(status_code=400, detail="Progress is only for TV shows")

    update_doc = {
        "$set": {
            "last_watched": {
                "season": payload.season,
                "episode": payload.episode,
                "updated_at": datetime.utcnow(),
            }
        },
        "$currentDate": {"updated_at": True},
    }
    await db["movies"].update_one({"_id": ObjectId(movie_id)}, update_doc)
    updated = await db["movies"].find_one({"_id": ObjectId(movie_id)})
    return _normalize(updated)


@router.delete("/{movie_id}", status_code=204)
async def delete_movie(movie_id: str, user=Depends(get_current_user)):
    # Find the movie to ensure it exists and belongs to the user
    movie_obj_id = ObjectId(movie_id)
    user_id_str = str(user["_id"])
    
    movie_to_delete = await db["movies"].find_one({"_id": movie_obj_id, "user_id": user_id_str})
    
    if not movie_to_delete:
        raise HTTPException(status_code=404, detail="Movie not found")

    # Remove social activity
    await db["activities"].delete_many({"movie_id": movie_id})
    
    delete_result = await db["movies"].delete_one({"_id": movie_obj_id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=500, detail="Movie not deleted")

