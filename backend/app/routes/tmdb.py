from fastapi import APIRouter, HTTPException, Query, Depends
from app.config import settings
from app.dependencies import get_current_user  # proteggiamo questi endpoint
import httpx

router = APIRouter(prefix="/tmdb", tags=["TMDb"])

BASE = "https://api.themoviedb.org/3"

def ensure_api_key():
    if not settings.TMDB_API_KEY:
        raise HTTPException(status_code=500, detail="TMDb API key non configurata")

@router.get("/search")
async def tmdb_search(q: str = Query(..., min_length=1), user=Depends(get_current_user)):
    """Ritorna una lista ridotta di risultati (id, title, release_date)."""
    ensure_api_key()
    params = {
        "api_key": settings.TMDB_API_KEY,
        "query": q,
        "language": "it-IT",
        "include_adult": "false",
        "page": 1,
    }
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{BASE}/search/movie", params=params)
        if r.status_code != 200:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        data = r.json()
    results = data.get("results", [])[:10]
    # normalizza
    return [
        {
            "id": m.get("id"),
            "title": m.get("title"),
            "release_date": m.get("release_date"),
        }
        for m in results
        if m.get("id")
    ]

@router.get("/details/{tmdb_id}")
async def tmdb_details(tmdb_id: int, user=Depends(get_current_user)):
    """Dettagli + credits: regista, cast, poster, runtime, ecc."""
    ensure_api_key()
    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": "it-IT",
        "append_to_response": "credits",
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
