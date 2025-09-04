# app/routes/tmdb.py
from fastapi import APIRouter, HTTPException, Query, Depends
from app.config import settings
from app.dependencies import get_current_user
import httpx

router = APIRouter(prefix="/tmdb", tags=["TMDb"])
BASE = "https://api.themoviedb.org/3"

def ensure_api_key():
    if not settings.TMDB_API_KEY:
        raise HTTPException(status_code=500, detail="TMDb API key non configurata")

# -------------------------
# SEARCH (film o serie)
# -------------------------
@router.get("/search")
async def tmdb_search(
    q: str = Query(..., min_length=1),
    type: str = Query("movie", pattern="^(movie|tv)$"),
    user=Depends(get_current_user)
):
    ensure_api_key()
    endpoint = f"{BASE}/search/{type}"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "query": q,
        "language": "it-IT",
        "include_adult": "false",
        "page": 1,
    }
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(endpoint, params=params)
        if r.status_code != 200:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        data = r.json()

    results = []
    for item in (data.get("results") or [])[:10]:
        if not item.get("id"):
            continue
        if type == "movie":
            title = item.get("title")
            date_ = item.get("release_date")
        else:
            title = item.get("name")
            date_ = item.get("first_air_date")
        results.append({
            "id": item["id"],
            "title": title,
            "release_date": date_,
            "kind": type
        })
    return results

# -------------------------
# DETAILS FILM
# -------------------------
@router.get("/details/{tmdb_id}")
async def tmdb_details(tmdb_id: int, user=Depends(get_current_user)):
    ensure_api_key()
    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "it-IT",
        "append_to_response": "credits,external_ids",
    }
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{BASE}/movie/{tmdb_id}", params=params)
        if r.status_code != 200:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        d = r.json()

    director = None
    cast_list = []
    try:
        crew = d.get("credits", {}).get("crew", []) or []
        director = next((c.get("name") for c in crew if c.get("job") == "Director"), None)
        cast_list = [c.get("name") for c in (d.get("credits", {}).get("cast") or [])[:5] if c.get("name")]
    except Exception:
        pass

    poster_url = f"https://image.tmdb.org/t/p/w500{d['poster_path']}" if d.get("poster_path") else None
    release_date = d.get("release_date")
    release_year = int(release_date[:4]) if release_date and len(release_date) >= 4 else None

    return {
        "kind": "movie",
        "tmdb_id": d.get("id"),
        "title": d.get("title"),
        "release_date": release_date,
        "release_year": release_year,
        "poster_url": poster_url,
        "overview": d.get("overview") or None,
        "runtime": d.get("runtime"),
        "director": director,
        "cast": cast_list,
    }

# -------------------------
# DETAILS SERIE TV
# -------------------------
@router.get("/tv/{tmdb_id}")
async def tmdb_tv_details(tmdb_id: int, user=Depends(get_current_user)):
    ensure_api_key()
    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "it-IT",
        "append_to_response": "credits",
    }
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{BASE}/tv/{tmdb_id}", params=params)
        if r.status_code != 200:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        d = r.json()

    poster_url = f"https://image.tmdb.org/t/p/w500{d['poster_path']}" if d.get("poster_path") else None
    first_air_date = d.get("first_air_date")
    release_year = int(first_air_date[:4]) if first_air_date and len(first_air_date) >= 4 else None

    # “director”: per le serie uso il primo "created_by" (showrunner) se presente
    director = None
    created_by = d.get("created_by") or []
    if created_by:
        director = created_by[0].get("name")

    cast_list = []
    try:
        cast_list = [c.get("name") for c in (d.get("credits", {}).get("cast") or [])[:5] if c.get("name")]
    except Exception:
        pass

    # runtime: media del primo valore in episode_run_time, se esiste
    runtime = None
    er = d.get("episode_run_time") or []
    if er:
        runtime = er[0]

    return {
        "kind": "tv",
        "tmdb_id": d.get("id"),
        # normalizzo su "title"/"release_date" come per i film
        "title": d.get("name"),
        "release_date": first_air_date,
        "release_year": release_year,
        "poster_url": poster_url,
        "overview": d.get("overview") or None,
        "runtime": runtime,
        "director": director,
        "cast": cast_list,
        # opzionale: info stagioni (conteggio)
        "number_of_seasons": d.get("number_of_seasons"),
    }

# -------------------------
# STAGIONI: lista
# -------------------------
@router.get("/tv/{tmdb_id}/seasons")
async def tmdb_tv_seasons(tmdb_id: int, user=Depends(get_current_user)):
    ensure_api_key()
    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "it-IT",
    }
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{BASE}/tv/{tmdb_id}", params=params)
        if r.status_code != 200:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        d = r.json()

    seasons = []
    for s in d.get("seasons") or []:
        if s.get("season_number") is None:
            continue
        seasons.append({
            "season_number": s.get("season_number"),
            "name": s.get("name"),
            "episode_count": s.get("episode_count"),
        })
    # ordino per season_number
    seasons.sort(key=lambda x: x["season_number"])
    return seasons

# -------------------------
# EPISODI di una stagione
# -------------------------
@router.get("/tv/{tmdb_id}/season/{season_number}")
async def tmdb_tv_episodes(tmdb_id: int, season_number: int, user=Depends(get_current_user)):
    ensure_api_key()
    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "it-IT",
    }
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{BASE}/tv/{tmdb_id}/season/{season_number}", params=params)
        if r.status_code != 200:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        d = r.json()

    eps = []
    for e in d.get("episodes") or []:
        if e.get("episode_number") is None:
            continue
        eps.append({
            "episode_number": e.get("episode_number"),
            "name": e.get("name"),
        })
    eps.sort(key=lambda x: x["episode_number"])
    return eps
