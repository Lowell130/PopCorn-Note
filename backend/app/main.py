# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, movies
from app.routes import tmdb as tmdb_routes  # 👈 aggiunto
from app.db import db

app = FastAPI(title="PopCornNote API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(movies.router)
app.include_router(tmdb_routes.router)  # 👈 aggiunto

@app.on_event("startup")
async def create_indexes():
    await db["movies"].create_index("user_id")
    await db["movies"].create_index([("user_id", 1), ("created_at", -1)])
    await db["movies"].create_index([("user_id", 1), ("title", 1)])
