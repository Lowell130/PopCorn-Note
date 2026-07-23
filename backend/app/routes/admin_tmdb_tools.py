# app/routes/admin_tmdb_tools.py
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from app.config import settings
from app.dependencies import get_current_user, require_admin
from app.db import db
import httpx
from datetime import datetime
from app.routes.tmdb import safe_release_year
import asyncio

router = APIRouter(prefix="/admin/tmdb-tools", tags=["admin-tmdb"])

BASE = "https://api.themoviedb.org/3"

# Stato globale per la sincronizzazione in background
sync_state = {
    "running": False,
    "total_updated": 0,
    "remaining": 0,
    "last_batch_updated": 0,
    "error": None,
    "completed": False
}


def ensure_api_key():
    if not settings.TMDB_API_KEY:
        raise HTTPException(status_code=500, detail="TMDb API key non configurata")


async def run_backfill_loop():
    global sync_state
    try:
        ensure_api_key()
        movies_coll = db.movies
        start_time = datetime.utcnow()
        
        while True:
            # Trova i film che hanno un tmdb_id, escludendo quelli già aggiornati in questo specifico run
            query = {
                "tmdb_id": {"$ne": None},
                "$or": [
                    {"tmdb_sync_at": {"$exists": False}},
                    {"tmdb_sync_at": None},
                    {"tmdb_sync_at": {"$lt": start_time}}
                ]
            }
            
            # Conta rimanenti
            remaining = await movies_coll.count_documents(query)
            sync_state["remaining"] = remaining
            
            if remaining == 0 or not sync_state["running"]:
                break
                
            # Batch di 20 elementi alla volta
            docs = await movies_coll.find(query).limit(20).to_list(length=20)
            if not docs:
                break
                
            batch_updated = 0
            async with httpx.AsyncClient(timeout=15) as client:
                for doc in docs:
                    if not sync_state["running"]:
                        break

                    tmdb_id = doc.get("tmdb_id")
                    kind = doc.get("kind") or "movie"

                    if not tmdb_id:
                        continue

                    if kind == "tv":
                        url = f"{BASE}/tv/{tmdb_id}"
                        params = {
                            "api_key": settings.TMDB_API_KEY,
                            "language": "it-IT",
                            "append_to_response": "credits",
                        }
                    else:
                        url = f"{BASE}/movie/{tmdb_id}"
                        params = {
                            "api_key": settings.TMDB_API_KEY,
                            "language": "it-IT",
                            "append_to_response": "credits",
                        }

                    try:
                        r = await client.get(url, params=params)
                        if r.status_code != 200:
                            await movies_coll.update_one(
                                {"_id": doc["_id"]},
                                {"$set": {"tmdb_sync_at": datetime.utcnow()}},
                            )
                            continue
                        
                        data = r.json()
                        vote = data.get("vote_average")
                        overview = data.get("overview") or None
                        poster_path = data.get("poster_path")
                        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
                        
                        director = None
                        cast_list = []
                        runtime = None
                        
                        if kind == "tv":
                            created_by = data.get("created_by") or []
                            if created_by:
                                director = created_by[0].get("name")
                            er = data.get("episode_run_time") or []
                            if er:
                                runtime = er[0]
                            release_date = data.get("first_air_date")
                        else:
                            crew = data.get("credits", {}).get("crew", []) or []
                            director = next((c.get("name") for c in crew if c.get("job") == "Director"), None)
                            runtime = data.get("runtime")
                            release_date = data.get("release_date")
                        
                        try:
                            cast_list = [c.get("name") for c in (data.get("credits", {}).get("cast") or [])[:5] if c.get("name")]
                        except Exception:
                            pass
                        
                        release_year = safe_release_year(release_date)

                        update_fields = {
                            "tmdb_vote": vote,
                            "tmdb_sync_at": datetime.utcnow(),
                            "updated_at": datetime.utcnow()
                        }

                        if runtime is not None and runtime > 0:
                            if not doc.get("runtime") or doc.get("runtime") == 0:
                                update_fields["runtime"] = runtime

                        if release_date:
                            if not doc.get("release_date"):
                                update_fields["release_date"] = release_date
                            if not doc.get("release_year") and release_year:
                                update_fields["release_year"] = release_year

                        if overview and not doc.get("overview"):
                            update_fields["overview"] = overview
                        
                        if poster_url and not doc.get("poster_url"):
                            update_fields["poster_url"] = poster_url
                        
                        if director and not doc.get("director"):
                            update_fields["director"] = director
                        
                        if cast_list and (not doc.get("cast") or len(doc.get("cast")) == 0):
                            update_fields["cast"] = cast_list

                        await movies_coll.update_one(
                            {"_id": doc["_id"]},
                            {"$set": update_fields},
                        )
                        batch_updated += 1
                        sync_state["total_updated"] += 1
                    except Exception:
                        continue
                    
                    # Breve pausa tra le richieste per evitare di intasare le API di TMDB
                    await asyncio.sleep(0.15)
            
            sync_state["last_batch_updated"] = batch_updated
            await asyncio.sleep(0.5)
            
        sync_state["completed"] = True
    except Exception as e:
        sync_state["error"] = str(e)
    finally:
        sync_state["running"] = False


@router.post("/backfill-tmdb-votes")
async def backfill_tmdb_votes(
    background_tasks: BackgroundTasks,
    admin=Depends(require_admin),
):
    """
    Avvia la sincronizzazione in background di voti e info da TMDb.
    """
    global sync_state
    if sync_state["running"]:
        return {"message": "Sincronizzazione già in corso", "state": sync_state}

    sync_state["running"] = True
    sync_state["total_updated"] = 0
    sync_state["last_batch_updated"] = 0
    sync_state["error"] = None
    sync_state["completed"] = False
    
    background_tasks.add_task(run_backfill_loop)
    return {"message": "Sincronizzazione avviata in background", "state": sync_state}


@router.get("/backfill-status")
async def get_backfill_status(admin=Depends(require_admin)):
    """
    Restituisce lo stato corrente della sincronizzazione in background.
    """
    global sync_state
    if not sync_state["running"]:
        # Calcola quanti elementi in totale non sono mai stati sincronizzati
        movies_coll = db.movies
        remaining = await movies_coll.count_documents({
            "tmdb_id": {"$ne": None},
            "tmdb_sync_at": {"$exists": False}
        })
        sync_state["remaining"] = remaining
    return sync_state
