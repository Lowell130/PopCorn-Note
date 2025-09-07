# app/routes/tmdb.py
from fastapi import APIRouter, HTTPException, Query, Depends
from app.config import settings
from app.dependencies import get_current_user
import httpx
import asyncio

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
    page: int = Query(1, ge=1, le=50),
    user=Depends(get_current_user)
):
    """
    Ricerca TMDb con paginazione e arricchimento risultati:
    - page / total_pages
    - per ciascun item: poster_url (w92), overview, release_year, vote_average, director/showrunner
    """
    ensure_api_key()

    search_endpoint = f"{BASE}/search/{type}"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "query": q,
        "language": "it-IT",
        "include_adult": "false",
        "page": page,
    }

    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(search_endpoint, params=params)
        if r.status_code != 200:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        data = r.json()

        raw_results = data.get("results") or []

        async def enrich(item):
            try:
                tmdb_id = item.get("id")
                if not tmdb_id:
                    return None

                if type == "movie":
                    title = item.get("title")
                    date_ = item.get("release_date")
                    details_url = f"{BASE}/movie/{tmdb_id}"
                else:
                    title = item.get("name")
                    date_ = item.get("first_air_date")
                    details_url = f"{BASE}/tv/{tmdb_id}"

                release_year = int(date_[:4]) if date_ and len(date_) >= 4 else None
                poster_url = f"https://image.tmdb.org/t/p/w92{item['poster_path']}" if item.get("poster_path") else None

                # prendo credits per ricavare director/showrunner
                details_params = {
                    "api_key": settings.TMDB_API_KEY,
                    "language": "it-IT",
                    "append_to_response": "credits"
                }
                dr = await client.get(details_url, params=details_params)

                director = None
                if dr.status_code == 200:
                    dd = dr.json()
                    if type == "movie":
                        crew = (dd.get("credits", {}) or {}).get("crew") or []
                        director = next((c.get("name") for c in crew if c.get("job") == "Director"), None)
                    else:
                        created_by = dd.get("created_by") or []
                        if created_by:
                            director = created_by[0].get("name")

                return {
                    "id": tmdb_id,
                    "kind": type,
                    "title": title,
                    "release_date": date_,
                    "release_year": release_year,
                    "poster_url": poster_url,
                    "overview": item.get("overview") or None,
                    "vote_average": item.get("vote_average"),
                    "tmdb_id": tmdb_id,
                    "director": director,
                }
            except Exception:
                return None

        # enrichment in parallelo per gli item della pagina
        results = await asyncio.gather(*[enrich(it) for it in raw_results])

    return {
        "page": data.get("page", 1),
        "total_pages": data.get("total_pages", 1),
        "results": [x for x in results if x],
    }
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


# --- TRENDING / POPOLARI -----------------------------------------
MAX_TMDB_PAGES = 1000

@router.get("/trending")
async def tmdb_trending(
    media: str = Query("all", pattern="^(all|movie|tv)$"),
    window: str = Query("day", pattern="^(day|week)$"),
    language: str = Query("it-IT"),
    page: int = Query(1, ge=1, le=MAX_TMDB_PAGES),
    user=Depends(get_current_user)
):
    """
    Trending TMDb: /trending/{media}/{window}
    media: all|movie|tv
    window: day|week
    """
    ensure_api_key()
    url = f"{BASE}/trending/{media}/{window}"
    params = {"api_key": settings.TMDB_API_KEY, "language": language, "page": page}

    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, params=params)
        if r.status_code != 200:
            raise HTTPException(status_code=502, detail="TMDb upstream error")
        data = r.json()

    base_img = "https://image.tmdb.org/t/p/w500"
    items = []
    for m in data.get("results", []):
        mtype = m.get("media_type") or ("movie" if "title" in m else "tv")
        title = m.get("title") or m.get("name")
        release_date = m.get("release_date") or m.get("first_air_date")
        items.append({
            "id": m.get("id"),
            "kind": "movie" if mtype == "movie" else ("tv" if mtype == "tv" else None),
            "title": title,
            "release_date": release_date,
            "release_year": int(release_date[:4]) if release_date else None,
            "poster_url": f"{base_img}{m['poster_path']}" if m.get("poster_path") else None,
            "overview": m.get("overview") or None,
            "vote_average": m.get("vote_average"),
            "vote_count": m.get("vote_count"),
            "popularity": m.get("popularity"),
            "tmdb_id": m.get("id"),
        })

    return {
        "page": data.get("page", 1),
        "total_pages": min(data.get("total_pages", 1), MAX_TMDB_PAGES),
        "results": items,
    }


@router.get("/popular")
async def tmdb_popular(
    media: str = Query("movie", pattern="^(movie|tv)$"),
    language: str = Query("it-IT"),
    page: int = Query(1, ge=1, le=MAX_TMDB_PAGES),
    user=Depends(get_current_user)
):
    """
    Popolari TMDb: /movie/popular o /tv/popular
    """
    ensure_api_key()
    url = f"{BASE}/{media}/popular"
    params = {"api_key": settings.TMDB_API_KEY, "language": language, "page": page}

    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, params=params)
        if r.status_code != 200:
            raise HTTPException(status_code=502, detail="TMDb upstream error")
        data = r.json()

    base_img = "https://image.tmdb.org/t/p/w500"
    items = []
    for m in data.get("results", []):
        title = m.get("title") or m.get("name")
        release_date = m.get("release_date") or m.get("first_air_date")
        items.append({
            "id": m.get("id"),
            "kind": "movie" if media == "movie" else "tv",
            "title": title,
            "release_date": release_date,
            "release_year": int(release_date[:4]) if release_date else None,
            "poster_url": f"{base_img}{m['poster_path']}" if m.get("poster_path") else None,
            "overview": m.get("overview") or None,
            "vote_average": m.get("vote_average"),
            "vote_count": m.get("vote_count"),
            "popularity": m.get("popularity"),
            "tmdb_id": m.get("id"),
        })

    return {
        "page": data.get("page", 1),
        "total_pages": min(data.get("total_pages", 1), MAX_TMDB_PAGES),
        "results": items,
    }