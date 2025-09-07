# app/routes/movies.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from app.schemas.movie import MovieCreate, MovieUpdate, MovieResponse
from app.dependencies import get_current_user
from app.db import db
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/movies", tags=["Movies"])

def _normalize(doc: dict) -> dict:
    doc = dict(doc)
    doc["id"] = str(doc["_id"])
    doc.pop("_id", None)
    return doc

@router.post("/", response_model=MovieResponse, status_code=201)
async def add_movie(movie: MovieCreate, user=Depends(get_current_user)):
    movie_dict = movie.dict(exclude_unset=True)
    movie_dict["kind"] = movie_dict.get("kind") or "movie"
    movie_dict["user_id"] = str(user["_id"])
    now = datetime.utcnow()
    movie_dict["created_at"] = now
    movie_dict["updated_at"] = now

    result = await db["movies"].insert_one(movie_dict)
    new_movie = await db["movies"].find_one({"_id": result.inserted_id})
    return _normalize(new_movie)

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
):
    # costruiamo filtri componibili
    and_clauses = [{"user_id": str(user["_id"])}]

    if status:
        and_clauses.append({"status": status})

    if kind:
        if kind == "movie":
            # include anche storici senza 'kind'
            and_clauses.append({"$or": [{"kind": "movie"}, {"kind": {"$exists": False}}]})
        else:
            and_clauses.append({"kind": "tv"})

    if q:
        like = {"$regex": q, "$options": "i"}
        and_clauses.append({"$or": [{"title": like}, {"note": like}]})

    filt = {"$and": and_clauses} if len(and_clauses) > 1 else and_clauses[0]

    # ordinamento
    if sort == "title_asc":
        sort_spec = [("title", 1)]
    elif sort == "score_desc":
        sort_spec = [("score", -1), ("created_at", -1)]
    else:
        sort_spec = [("created_at", -1)]

    cursor = db["movies"].find(filt).sort(sort_spec).skip(skip).limit(limit)
    docs = await cursor.to_list(length=limit)
    return [_normalize(d) for d in docs]

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

@router.delete("/{movie_id}", status_code=204)
async def delete_movie(movie_id: str, user=Depends(get_current_user)):
    res = await db["movies"].delete_one({"_id": ObjectId(movie_id), "user_id": str(user["_id"])})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Movie not found")
    return
