import asyncio
import sys
import httpx
from app.config import settings
from app.db import db

# Forza l'output della console in UTF-8 per Windows
sys.stdout.reconfigure(encoding='utf-8')

async def auto_tag():
    print("Inizio tagging automatico...")
    if not settings.TMDB_API_KEY:
        print("Errore: TMDB_API_KEY non configurata!")
        return

    # Trova tutti i film con un tmdb_id che non hanno il campo tags o hanno tags vuoti/Null
    cursor = db["movies"].find({
        "tmdb_id": {"$exists": True, "$ne": None},
        "$or": [
            {"tags": {"$exists": False}},
            {"tags": None},
            {"tags": []}
        ]
    })
    movies = await cursor.to_list(length=10000)
    print(f"Trovati {len(movies)} film/serie da aggiornare.")

    async with httpx.AsyncClient(timeout=15.0) as client:
        for m in movies:
            movie_id = m["_id"]
            tmdb_id = m["tmdb_id"]
            kind = m.get("kind", "movie")
            title = m.get("title", "Sconosciuto")

            # Determina URL
            if kind == "tv":
                url = f"https://api.themoviedb.org/3/tv/{tmdb_id}"
            else:
                url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"

            try:
                r = await client.get(
                    url,
                    params={"api_key": settings.TMDB_API_KEY, "language": "it-IT"}
                )
                if r.status_code == 200:
                    data = r.json()
                    genres = data.get("genres", [])
                    tags = [g.get("name").lower() for g in genres if g.get("name")]
                    if tags:
                        await db["movies"].update_one(
                            {"_id": movie_id},
                            {"$set": {"tags": tags}}
                        )
                        print(f"Aggiornato '{title}': {tags}")
                    else:
                        print(f"Nessun genere trovato per '{title}'")
                else:
                    print(f"Errore TMDB per '{title}' (ID {tmdb_id}): status {r.status_code}")
            except Exception as e:
                print(f"Errore durante l'aggiornamento di '{title}': {e}")
            # Aspetta un attimo per non sovraccaricare le API
            await asyncio.sleep(0.1)

    print("Tagging completato!")

if __name__ == "__main__":
    asyncio.run(auto_tag())
