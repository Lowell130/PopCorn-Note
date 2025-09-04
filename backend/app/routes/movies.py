# app/routes/movies.py
from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.movie import MovieCreate, MovieUpdate
from app.dependencies import get_current_user
from app.db import db
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.post("/")
async def add_movie(movie: MovieCreate, user=Depends(get_current_user)):
    movie_dict = movie.dict(exclude_unset=True)
    movie_dict["kind"] = movie_dict.get("kind") or "movie"   # 👈 default sicuro
    movie_dict["user_id"] = str(user["_id"])
    # timestamps
    now = datetime.utcnow()
    movie_dict["created_at"] = now
    movie_dict["updated_at"] = now

    result = await db["movies"].insert_one(movie_dict)
    new_movie = await db["movies"].find_one({"_id": result.inserted_id})

    # normalize id
    new_movie["id"] = str(new_movie["_id"])
    del new_movie["_id"]
    return new_movie


@router.get("/{movie_id}")
async def get_movie(movie_id: str, user=Depends(get_current_user)):
    m = await db["movies"].find_one({"_id": ObjectId(movie_id), "user_id": str(user["_id"])})
    if not m:
        raise HTTPException(status_code=404, detail="Movie not found")
    m["id"] = str(m["_id"])
    del m["_id"]
    return m

@router.get("/")
async def list_movies(
    user=Depends(get_current_user),
    # opzionale: parametri per estensioni future
    status: str | None = None,
    q: str | None = None,
     kind: str | None = None,   # 🔽 NUOVO
    limit: int = Query(100, le=1000),
    skip: int = 0,
):
    filt = {"user_id": str(user["_id"])}
    if status:
        filt["status"] = status
    if kind in ("movie", "tv"):   # 🔽 NUOVO
        if kind == "movie":
            # 👇 include anche i record storici senza 'kind'
            filt["$or"] = [
                {"kind": "movie"},
                {"kind": {"$exists": False}},
            ]
        else:
            filt["kind"] = "tv"

    if q:
        filt["$or"] = [
            {"title": {"$regex": q, "$options": "i"}},
            {"note": {"$regex": q, "$options": "i"}},
        ]

    cursor = db["movies"].find(filt).sort("created_at", -1).skip(skip).limit(limit)
    movies = await cursor.to_list(length=limit)
    for m in movies:
        m["id"] = str(m["_id"])
        del m["_id"]
    return movies

@router.put("/{movie_id}")
async def update_movie(movie_id: str, movie: MovieUpdate, user=Depends(get_current_user)):
    # aggiornamento parziale + updated_at automatico
    update_doc = {
        "$set": movie.dict(exclude_unset=True),
        "$currentDate": {"updated_at": True},
    }
    result = await db["movies"].update_one(
        {"_id": ObjectId(movie_id), "user_id": str(user["_id"])},
        update_doc
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Movie not found")

    updated = await db["movies"].find_one({"_id": ObjectId(movie_id)})
    updated["id"] = str(updated["_id"])
    del updated["_id"]
    return updated

@router.delete("/{movie_id}")
async def delete_movie(movie_id: str, user=Depends(get_current_user)):
    result = await db["movies"].delete_one({"_id": ObjectId(movie_id), "user_id": str(user["_id"])})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"msg": "Movie deleted"}
