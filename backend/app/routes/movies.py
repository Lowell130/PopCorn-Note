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
import re
import httpx

from app.config import settings

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

    # Se il film ha tmdb_id ma non ha tag, recuperiamoli da TMDb in automatico
    if movie_dict.get("tmdb_id") and not movie_dict.get("tags"):
        try:
            tmdb_key = settings.TMDB_API_KEY
            if tmdb_key:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    tmdb_id = movie_dict["tmdb_id"]
                    kind = movie_dict["kind"]
                    url = f"https://api.themoviedb.org/3/tv/{tmdb_id}" if kind == "tv" else f"https://api.themoviedb.org/3/movie/{tmdb_id}"
                    r = await client.get(url, params={"api_key": tmdb_key, "language": "it-IT"})
                    if r.status_code == 200:
                        data = r.json()
                        genres = data.get("genres", [])
                        tags = [g.get("name").lower() for g in genres if g.get("name")]
                        if tags:
                            movie_dict["tags"] = tags
        except Exception as e:
            print(f"Errore auto-tagging backend: {e}")

    try:
        result = await db["movies"].insert_one(movie_dict)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail="Questo titolo è già presente nella tua collezione."
        )
    new_movie = await db["movies"].find_one({"_id": result.inserted_id})
    
    return _normalize(new_movie)


@router.get("/random", response_model=MovieResponse)
async def get_random_movie(
    user=Depends(get_current_user),
    status: str = Query("to_watch", pattern="^(to_watch|watched|upcoming|watching)$"),
    kind: str | None = Query(None, pattern="^(movie|tv)$"),
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

    # 4. Total watchtime (in minutes) for watched items
    watchtime_pipeline = [
        {"$match": {
            "user_id": uid,
            "status": "watched",
            "runtime": {"$type": "number", "$gt": 0}
        }},
        {"$group": {"_id": None, "total_runtime": {"$sum": "$runtime"}}}
    ]
    watchtime_agg = await db["movies"].aggregate(watchtime_pipeline).to_list(length=1)
    total_watchtime = watchtime_agg[0]["total_runtime"] if watchtime_agg else 0

    # --- AGGREGAZIONI AVANZATE ---
    
    # 1. Top Directors (Top 5)
    dir_pipeline = [
        {"$match": {"user_id": uid, "director": {"$ne": None}}},
        {"$group": {"_id": "$director", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ]
    top_directors = await db["movies"].aggregate(dir_pipeline).to_list(length=5)
    
    # 1.5 Top Actors (Top 5)
    actor_pipeline = [
        {"$match": {"user_id": uid, "cast": {"$exists": True, "$not": {"$size": 0}}}},
        {"$unwind": "$cast"},
        {"$group": {"_id": "$cast", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ]
    top_actors = await db["movies"].aggregate(actor_pipeline).to_list(length=5)
    
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

    # 3.5 Tag Distribution (Top 20)
    tag_pipeline = [
        {"$match": {"user_id": uid, "tags": {"$exists": True, "$not": {"$size": 0}}}},
        {"$unwind": "$tags"},
        {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 20}
    ]
    top_tags = await db["movies"].aggregate(tag_pipeline).to_list(length=20)

    return {
        "total_movies": total_movies,
        "total_series": total_series,
        "watched": watched,
        "to_watch": to_watch,
        "upcoming": upcoming,
        "watching": watching,
        "avg_score": avg_score,
        "total_watchtime": total_watchtime,
        "stats_advanced": {
            "directors": [{"name": x["_id"], "count": x["count"]} for x in top_directors if x["_id"]],
            "actors": [{"name": x["_id"], "count": x["count"]} for x in top_actors if x["_id"]],
            "years": [{"year": x["_id"], "count": x["count"]} for x in years_dist],
            "scores": [{"score": x["_id"], "count": x["count"]} for x in scores_dist],
            "tags": [{"name": x["_id"], "count": x["count"]} for x in top_tags if x["_id"]],
        }
    }



def _oid_or_404(movie_id: str) -> ObjectId:
    if not ObjectId.is_valid(movie_id):
        raise HTTPException(status_code=404, detail="Movie not found")
    return ObjectId(movie_id)


async def _fetch_tmdb_item(tmdb_id: int, kind: str) -> dict | None:
    """Scarica da TMDb i dati di un film/serie e li converte nel formato del DB."""
    tmdb_key = settings.TMDB_API_KEY
    if not tmdb_key:
        return None
    path = "tv" if kind == "tv" else "movie"
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(
            f"https://api.themoviedb.org/3/{path}/{tmdb_id}",
            params={"api_key": tmdb_key, "language": "it-IT", "append_to_response": "credits"},
        )
    if r.status_code != 200:
        return None
    data = r.json()

    poster_path = data.get("poster_path")
    date_str = data.get("release_date") or data.get("first_air_date") or ""
    director = None
    cast_list = []
    credits = data.get("credits") or {}
    for member in credits.get("crew", []):
        if member.get("job") == "Director":
            director = member.get("name")
            break
    if not director and kind == "tv":
        creators = data.get("created_by") or []
        if creators:
            director = creators[0].get("name")
    cast_list = [c.get("name") for c in credits.get("cast", [])[:5] if c.get("name")]
    runtime = data.get("runtime")
    if not runtime and data.get("episode_run_time"):
        runtime = data["episode_run_time"][0]

    return {
        "tmdb_id": tmdb_id,
        "title": data.get("title") or data.get("name") or "Sconosciuto",
        "kind": kind,
        "poster_url": f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None,
        "release_year": int(date_str[:4]) if date_str[:4].isdigit() else None,
        "release_date": date_str if re.match(r"^\d{4}-\d{2}-\d{2}$", date_str) else None,
        "overview": data.get("overview", ""),
        "director": director,
        "cast": cast_list,
        "runtime": runtime if isinstance(runtime, int) and 0 <= runtime <= 600 else None,
        "tmdb_vote": data.get("vote_average"),
        "tags": [g.get("name").lower() for g in data.get("genres", []) if g.get("name")],
    }


async def _find_by_tmdb(user_id: str, tmdb_id: int, kind: str | None):
    q = {"user_id": user_id, "$or": [{"tmdb_id": tmdb_id}, {"tmdb_id": str(tmdb_id)}]}
    if kind == "tv":
        q["kind"] = "tv"
    elif kind == "movie":
        q["$and"] = [{"$or": [{"kind": "movie"}, {"kind": {"$exists": False}}]}]
    return await db["movies"].find_one(q)


@router.get("/{movie_id}", response_model=MovieResponse)
async def get_movie(
    movie_id: str,
    user=Depends(get_current_user),
    kind: str | None = Query(None, pattern="^(movie|tv)$"),
):
    """
    Legge un titolo della collezione dell'utente (per _id o per tmdb_id).
    Sola lettura: per importare un titolo da TMDb usare POST /movies/import/{tmdb_id}.
    """
    user_id_str = str(user["_id"])
    m = None

    if ObjectId.is_valid(movie_id):
        m = await db["movies"].find_one({"_id": ObjectId(movie_id), "user_id": user_id_str})

    if not m and movie_id.isdigit():
        m = await _find_by_tmdb(user_id_str, int(movie_id), kind)

    if not m:
        raise HTTPException(status_code=404, detail="Film o Serie TV non trovato")
    return _normalize(m)


@router.post("/import/{tmdb_id}", response_model=MovieResponse)
async def import_from_tmdb(
    tmdb_id: int,
    user=Depends(get_current_user),
    kind: str = Query("movie", pattern="^(movie|tv)$"),
):
    """
    Importa un titolo da TMDb nella collezione dell'utente (status 'to_watch').
    Se è già presente restituisce quello esistente (idempotente).
    """
    if tmdb_id < 1:
        raise HTTPException(status_code=404, detail="Film o Serie TV non trovato")
    user_id_str = str(user["_id"])

    existing = await _find_by_tmdb(user_id_str, tmdb_id, kind)
    if existing:
        return _normalize(existing)

    try:
        data = await _fetch_tmdb_item(tmdb_id, kind)
    except httpx.HTTPError:
        raise HTTPException(status_code=502, detail="TMDb non raggiungibile, riprova più tardi")
    if not data:
        raise HTTPException(status_code=404, detail="Film o Serie TV non trovato su TMDb")

    now = datetime.utcnow()
    doc = {**data, "user_id": user_id_str, "status": "to_watch", "created_at": now, "updated_at": now}
    try:
        res = await db["movies"].insert_one(doc)
        doc["_id"] = res.inserted_id
    except DuplicateKeyError:
        doc = await _find_by_tmdb(user_id_str, tmdb_id, kind)
        if not doc:
            raise HTTPException(status_code=409, detail="Titolo già presente")
    return _normalize(doc)


@router.get("/", response_model=List[MovieResponse])
async def list_movies(
    user=Depends(get_current_user),
    status: str | None = Query(None, pattern="^(to_watch|watched|upcoming|watching)$"),
    q: str | None = None,
    kind: str | None = Query(None, pattern="^(movie|tv)$"),
    limit: int = Query(100, ge=1, le=500),
    skip: int = Query(0, ge=0, le=100000),
    sort: str = Query("created_at_desc", pattern="^(created_at_desc|title_asc|score_desc|release_date_asc)$"),
    # priorità in alto (come già fatto)
    priority_status: str | None = Query(None, pattern="^(to_watch|watched|upcoming|watching)$"),
    # 👇 NUOVO: spinge questo status in fondo
    push_last_status: str | None = Query(None, pattern="^(to_watch|watched|upcoming|watching)$"),
    director: str | None = Query(None, description="Filtra per nome del regista"),
    cast: str | None = Query(None, description="Filtra per nome di un attore nel cast"),
    tag: str | None = Query(None, description="Filtra per tag"),
    upcoming_calendar: bool = Query(False, description="Se True, restituisce solo i titoli per il calendario uscite (upcoming o data futura)"),
):
    and_clauses = [{"user_id": str(user["_id"])}]
    if status:
        and_clauses.append({"status": status})

    if upcoming_calendar:
        today_str = datetime.utcnow().strftime("%Y-%m-%d")
        and_clauses.append({
            "$or": [
                {"release_date": {"$gte": today_str}},
                {
                    "status": "upcoming",
                    "$or": [
                        {"release_date": {"$exists": False}},
                        {"release_date": None},
                        {"release_date": ""}
                    ]
                }
            ]
        })

    if kind:
        if kind == "movie":
            and_clauses.append({"$or": [{"kind": "movie"}, {"kind": {"$exists": False}}]})
        else:
            and_clauses.append({"kind": "tv"})

    q = (q or "").strip()[:100]
    if q:
        # escape: i caratteri speciali vengono cercati letteralmente (no errori 500 / ReDoS)
        like = {"$regex": re.escape(q), "$options": "i"}
        and_clauses.append({"$or": [{"title": like}, {"note": like}, {"tags": like}]})

    if director:
        and_clauses.append({"director": director})

    if cast:
        and_clauses.append({"cast": cast})

    if tag:
        and_clauses.append({"tags": tag})

    filt = {"$and": and_clauses} if len(and_clauses) > 1 else and_clauses[0]

    # ordinamento base
    if sort == "title_asc":
        tail_sort = {"title": 1, "created_at": -1}
        sort_spec = [("title", 1)]
    elif sort == "score_desc":
        tail_sort = {"score": -1, "created_at": -1}
        sort_spec = [("score", -1), ("created_at", -1)]
    elif sort == "release_date_asc":
        tail_sort = {"release_date": 1, "created_at": -1}
        sort_spec = [("release_date", 1), ("created_at", -1)]
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
    oid = _oid_or_404(movie_id)
    changes = movie.dict(exclude_unset=True)
    update_doc = {"$currentDate": {"updated_at": True}}
    if changes:
        update_doc["$set"] = changes
    res = await db["movies"].update_one(
        {"_id": oid, "user_id": str(user["_id"])},
        update_doc
    )
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Movie not found")
    updated = await db["movies"].find_one({"_id": oid})
    return _normalize(updated)


@router.put("/{movie_id}/progress", response_model=MovieResponse)
async def update_progress(
    movie_id: str,
    payload: ProgressUpdate,
    user=Depends(get_current_user),
):
    # verifica esistenza item dell'utente
    oid = _oid_or_404(movie_id)
    m = await db["movies"].find_one({"_id": oid, "user_id": str(user["_id"])})
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
    await db["movies"].update_one({"_id": oid}, update_doc)
    updated = await db["movies"].find_one({"_id": oid})
    return _normalize(updated)


@router.delete("/{movie_id}", status_code=204)
async def delete_movie(movie_id: str, user=Depends(get_current_user)):
    # Find the movie to ensure it exists and belongs to the user
    movie_obj_id = _oid_or_404(movie_id)
    user_id_str = str(user["_id"])
    
    movie_to_delete = await db["movies"].find_one({"_id": movie_obj_id, "user_id": user_id_str})
    
    if not movie_to_delete:
        raise HTTPException(status_code=404, detail="Movie not found")

    # Pulisce eventuali attività social legacy collegate al titolo
    await db["activities"].delete_many({"movie_id": movie_id})
    
    delete_result = await db["movies"].delete_one({"_id": movie_obj_id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=500, detail="Movie not deleted")

