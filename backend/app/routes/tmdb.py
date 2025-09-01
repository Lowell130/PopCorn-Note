# app/routes/tmdb.py
from fastapi import APIRouter, HTTPException, Query, Depends
from app.config import settings
from app.dependencies import get_current_user
import httpx
from datetime import date
from dateutil.relativedelta import relativedelta  # pip install python-dateutil

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
    """
    Dettagli + credits: regista, cast, poster, runtime, overview IT.
    Includo anche external_ids per ottenere (eventualmente) imdb_id.
    """
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

    # regista
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

    imdb_id = (d.get("external_ids") or {}).get("imdb_id")  # opzionale

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
        "imdb_id": imdb_id,  # opzionale, se ti serve
    }
@router.get("/upcoming")
async def tmdb_upcoming(
    months: int = Query(3, ge=1, le=12),            # non usato direttamente con /movie/upcoming, ma lo teniamo per compat
    region: str = Query("IT", min_length=2, max_length=2),
    language: str = Query("it-IT"),
    page: int = Query(1, ge=1, le=10),

    # 🔧 filtri soft e opzionali
    min_votes: int = Query(50, ge=0),
    min_popularity: float = Query(5.0, ge=0.0),
    only_with_poster: bool = Query(True),
    allowed_langs: str = Query("", description="CSV di lingue originali consentite, es: it,en,fr"),
    user=Depends(get_current_user)
):
    """
    Film in uscita (lista TMDb curated) per `region` e `language`.
    Applica filtri soft (tutti opzionali). Se i filtri svuotano la lista, torna i risultati originali.
    """
    ensure_api_key()

    url = f"{BASE}/movie/upcoming"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": language,
        "region": region,
        "page": page,
    }

    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, params=params)
        if r.status_code != 200:
            raise HTTPException(status_code=502, detail="TMDb upstream error")
        data = r.json()

    base_img = "https://image.tmdb.org/t/p/w500"
    raw_items = []
    for m in data.get("results", []):
        raw_items.append({
            "id": m.get("id"),
            "title": m.get("title"),
            "release_date": m.get("release_date"),
            "poster_url": f"{base_img}{m['poster_path']}" if m.get("poster_path") else None,
            "overview": m.get("overview") or None,
            "vote_average": m.get("vote_average"),
            "vote_count": m.get("vote_count"),
            "popularity": m.get("popularity"),
            "original_language": (m.get("original_language") or "").lower(),
        })

    # ✅ filtri soft
    allowed = {x.strip().lower() for x in allowed_langs.split(",") if x.strip()} if allowed_langs else set()

    filtered = []
    for m in raw_items:
        if only_with_poster and not m["poster_url"]:
            continue
        if m["vote_count"] is not None and m["vote_count"] < min_votes:
            continue
        if m["popularity"] is not None and m["popularity"] < min_popularity:
            continue
        if allowed and m["original_language"] and m["original_language"] not in allowed:
            continue
        filtered.append(m)

    # 🛟 fallback: se i filtri sono troppo stringenti, torna i dati grezzi
    items = filtered if filtered else raw_items

    return {
        "page": data.get("page", 1),
        "total_pages": data.get("total_pages", 1),
        "total_results": data.get("total_results", 0),
        "results": items,
    }
