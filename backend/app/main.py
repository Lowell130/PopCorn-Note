# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, movies
from app.routes import tmdb as tmdb_routes  # 👈 aggiunto
from app.db import db
from app.routes import admin as admin_routes
from fastapi.responses import JSONResponse
import traceback
from fastapi import Request





app = FastAPI(title="PopCornNote API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",              # sviluppo locale
        "https://pop-corn-note.vercel.app",   # produzione su Vercel (nota https:// e non http://)       
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(movies.router)
app.include_router(tmdb_routes.router)  # 👈 aggiunto
app.include_router(admin_routes.router)

@app.on_event("startup")
async def create_indexes():
    await db["movies"].create_index("user_id")
    await db["movies"].create_index([("user_id", 1), ("created_at", -1)])
    await db["movies"].create_index([("user_id", 1), ("title", 1)])
    await db["users"].create_index("email", unique=True)
    await db["users"].create_index("created_at")
   # 👇 nuovo: evita duplicati per utente, se tmdb_id esiste
    await db["movies"].create_index(
        [("user_id", 1), ("tmdb_id", 1), ("kind", 1)],
        unique=True,
        sparse=True,
        name="uq_user_tmdb_kind"
    )



# # This is important for Vercel
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


@app.get("/api/health")
def health_check():
    return {"status": "healthy"}


@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    # stampa lo stacktrace nei log di Vercel
    print("==== ERRORE INTERNO ====")
    traceback.print_exc()
    print("========================")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )