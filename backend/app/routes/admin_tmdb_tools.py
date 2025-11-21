# app/routes/admin_tmdb_tools.py
from fastapi import APIRouter, Depends, HTTPException, Query
from app.config import settings
from app.dependencies import get_current_user
from app.db import db
import httpx

router = APIRouter(prefix="/admin/tmdb-tools", tags=["admin-tmdb"])

BASE = "https://api.themoviedb.org/3"


def ensure_api_key():
    if not settings.TMDB_API_KEY:
        raise HTTPException(status_code=500, detail="TMDb API key non configurata")


@router.post("/backfill-tmdb-votes")
async def backfill_tmdb_votes(
    limit: int = Query(50, ge=1, le=500),
    user=Depends(get_current_user),
):
    """
    Aggiorna tmdb_vote per i film/serie che hanno tmdb_id ma non tmdb_vote.
    Esegue al massimo 'limit' aggiornamenti per chiamata.
    """
    # opzionale: controllo admin
    # if not user.get("is_admin"):
    #     raise HTTPException(status_code=403, detail="Solo admin")

    ensure_api_key()

    movies_coll = db.movies

    # prendi solo quelli con tmdb_id presente e tmdb_vote mancante/null
    query = {
        "tmdb_id": {"$ne": None},
        "$or": [
            {"tmdb_vote": {"$exists": False}},
            {"tmdb_vote": None},
        ],
    }

    docs = await movies_coll.find(query).limit(limit).to_list(length=limit)
    if not docs:
        return {"updated": 0, "message": "Nessun film/serie da aggiornare"}

    updated = 0

    async with httpx.AsyncClient(timeout=10) as client:
        for doc in docs:
            tmdb_id = doc.get("tmdb_id")
            kind = doc.get("kind") or "movie"  # default movie

            if not tmdb_id:
                continue

            if kind == "tv":
                url = f"{BASE}/tv/{tmdb_id}"
            else:
                url = f"{BASE}/movie/{tmdb_id}"

            params = {
                "api_key": settings.TMDB_API_KEY,
                "language": "it-IT",
            }

            try:
                r = await client.get(url, params=params)
                if r.status_code != 200:
                    continue
                data = r.json()
                vote = data.get("vote_average")
                await movies_coll.update_one(
                    {"_id": doc["_id"]},
                    {"$set": {"tmdb_vote": vote}},
                )
                updated += 1
            except Exception:
                # logga se vuoi
                continue

    return {
        "updated": updated,
        "remaining_hint": "Richiama l'endpoint finché updated < limit per svuotare la coda",
    }
