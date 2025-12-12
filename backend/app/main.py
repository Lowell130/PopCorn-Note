# app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import traceback

from app.routes import auth, movies
from app.routes import tmdb as tmdb_routes
from app.routes import social  # 👈 Import social
from app.routes import admin as admin_routes
from app.db import db
from app.routes import admin_tmdb_tools

app = FastAPI(title="PopCornNote API")

# Evita redirect automatici / -> (/) che spesso rompono i CORS su 307/308
app.router.redirect_slashes = False

# Origini consentite (frontend)
ALLOWED_ORIGINS = [
    "https://pop-corn-note.vercel.app",  # produzione (Vercel)
    "http://localhost:3000",             # sviluppo locale
    # Se usi preview Vercel, valuta:
    # allow_origin_regex=r"^https:\/\/([a-z0-9-]+\.)?vercel\.app$",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    # Se usi preview Vercel, commenta la riga sopra e usa:
    # allow_origin_regex=r"^https:\/\/([a-z0-9-]+\.)?vercel\.app$",
    allow_credentials=True,        # necessario se usi cookie/sessione
    allow_methods=["*"],
    allow_headers=["*"],
    # facoltativo: esponi header custom al browser
    # expose_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(movies.router)
app.include_router(tmdb_routes.router)
app.include_router(social.router) # 👈 Include social
app.include_router(admin_routes.router)
app.include_router(admin_tmdb_tools.router)

@app.on_event("startup")
async def create_indexes():
    """Crea indici senza bloccare l'avvio in caso di errore."""
    try:
        await db["movies"].create_index("user_id")
        await db["movies"].create_index([("user_id", 1), ("created_at", -1)])
        await db["movies"].create_index([("user_id", 1), ("title", 1)])
        await db["users"].create_index("email", unique=True)
        await db["users"].create_index("created_at")
        # Evita duplicati per utente se tmdb_id esiste
        await db["movies"].create_index(
            [("user_id", 1), ("tmdb_id", 1), ("kind", 1)],
            unique=True,
            sparse=True,
            name="uq_user_tmdb_kind",
        )
    except Exception as e:
        print("==== STARTUP INDEX ERROR ====")
        traceback.print_exc()
        print("=============================")

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

# opzionale: health "semplice" senza prefisso
@app.get("/healthz")
async def healthz():
    return {"ok": True}

@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    # stampa lo stacktrace nei log (utile su Cloud Run)
    print("==== ERRORE INTERNO ====")
    traceback.print_exc()
    print("========================")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )
