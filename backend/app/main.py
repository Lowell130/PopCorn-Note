# app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from bson.errors import InvalidId
import os
import re
import traceback

from app.routes import auth, movies
from app.routes import tmdb as tmdb_routes
from app.routes import admin as admin_routes
from app.db import db
from app.routes import admin_tmdb_tools
from app.routes import watchlist
from app.utils import rate_limit

app = FastAPI(title="PopCornNote API")

# Evita redirect automatici / -> (/) che spesso rompono i CORS su 307/308
app.router.redirect_slashes = False

# Origini consentite (frontend)
ALLOWED_ORIGINS = [
    "https://popcornote.com",            # produzione (dominio custom)
    "https://www.popcornote.com",        # produzione www (dominio custom)
    "https://pop-corn-note.vercel.app",  # produzione (Vercel)
    "http://localhost:3000",             # sviluppo locale
    "http://127.0.0.1:3000",             # sviluppo locale IP
]

# Supporta eventuali domini passati da variabile d'ambiente ALLOWED_ORIGINS (es. su Cloud Run)
env_origins = os.getenv("ALLOWED_ORIGINS")
if env_origins:
    ALLOWED_ORIGINS.extend([o.strip() for o in env_origins.split(",") if o.strip()])

# Solo sottodomini di popcornote.com e le preview Vercel di QUESTO progetto
# (non più qualsiasi *.vercel.app)
ALLOWED_ORIGIN_REGEX = r"^https://(([a-z0-9-]+\.)?popcornote\.com|pop-corn-note(-[a-z0-9-]+)?\.vercel\.app)$"
_origin_re = re.compile(ALLOWED_ORIGIN_REGEX)


def _is_allowed_origin(origin: str | None) -> bool:
    return bool(origin) and (origin in ALLOWED_ORIGINS or bool(_origin_re.match(origin)))


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_origin_regex=ALLOWED_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault("X-Robots-Tag", "noindex, nofollow")
    return response


# Routers
app.include_router(auth.router)
app.include_router(movies.router)
app.include_router(tmdb_routes.router)
app.include_router(admin_routes.router)
app.include_router(admin_tmdb_tools.router)
app.include_router(watchlist.router)


async def _safe_index(coll, keys, **kwargs):
    try:
        await db[coll].create_index(keys, **kwargs)
    except Exception:
        print(f"==== STARTUP INDEX ERROR ({coll} {keys}) ====")
        traceback.print_exc()


@app.on_event("startup")
async def create_indexes():
    """Crea indici senza bloccare l'avvio in caso di errore (ognuno indipendente)."""
    await _safe_index("movies", "user_id")
    await _safe_index("movies", [("user_id", 1), ("created_at", -1)])
    await _safe_index("movies", [("user_id", 1), ("title", 1)])
    await _safe_index("users", "email", unique=True)
    await _safe_index("users", "username")
    await _safe_index("users", "created_at")
    # Evita duplicati per utente se tmdb_id esiste
    await _safe_index(
        "movies",
        [("user_id", 1), ("tmdb_id", 1), ("kind", 1)],
        unique=True,
        sparse=True,
        name="uq_user_tmdb_kind",
    )
    try:
        await rate_limit.ensure_indexes()
    except Exception:
        traceback.print_exc()


@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

# opzionale: health "semplice" senza prefisso
@app.get("/healthz")
async def healthz():
    return {"ok": True}

from starlette.exceptions import HTTPException as StarletteHTTPException


def _cors_headers(request: Request) -> dict:
    origin = request.headers.get("origin")
    if _is_allowed_origin(origin):
        return {"Access-Control-Allow-Origin": origin, "Access-Control-Allow-Credentials": "true", "Vary": "Origin"}
    return {}


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers={**(getattr(exc, "headers", None) or {}), **_cors_headers(request)},
    )


@app.exception_handler(InvalidId)
async def invalid_id_handler(request: Request, exc: InvalidId):
    # ID Mongo malformato nell'URL → risorsa inesistente, non errore del server
    return JSONResponse(status_code=404, content={"detail": "Not found"}, headers=_cors_headers(request))


@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    # stampa lo stacktrace nei log (utile su Cloud Run / Vercel)
    print("==== ERRORE INTERNO ====")
    traceback.print_exc()
    print("========================")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
        headers=_cors_headers(request),
    )
