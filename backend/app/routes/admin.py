# app/routes/admin.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
import httpx
import random
import uuid
from datetime import datetime, timedelta

from app.db import db
from app.dependencies import require_admin
from app.utils.auth import hash_password
from app.config import settings

router = APIRouter(prefix="/admin", tags=["Admin"])


# ======== MODELLI ========
class AdminUserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=2, max_length=50)
    password: Optional[str] = Field(None, min_length=6)
    is_admin: Optional[bool] = None


# ======== LISTA UTENTI + STATS ========
@router.get("/users")
async def list_users_with_stats(admin=Depends(require_admin)):
    users_cur = db["users"].find({}, {"email": 1, "username": 1, "is_admin": 1, "is_fake": 1})
    users = await users_cur.to_list(length=10000)

    pipe = [
        {
            "$group": {
                "_id": "$user_id",
                "total": {"$sum": 1},
                "watched": {"$sum": {"$cond": [{"$eq": ["$status", "watched"]}, 1, 0]}},
                "to_watch": {"$sum": {"$cond": [{"$eq": ["$status", "to_watch"]}, 1, 0]}},
                "watching": {"$sum": {"$cond": [{"$eq": ["$status", "watching"]}, 1, 0]}},
                "upcoming": {"$sum": {"$cond": [{"$eq": ["$status", "upcoming"]}, 1, 0]}},
                "avg_score": {
                    "$avg": {
                        "$cond": [
                            {
                                "$and": [
                                    {"$gte": ["$score", 1]},
                                    {"$lte": ["$score", 10]},
                                    {"$ne": ["$score", None]},
                                ]
                            },
                            "$score",
                            None,
                        ]
                    }
                },
            }
        }
    ]
    stats = await db["movies"].aggregate(pipe).to_list(length=10000)
    stats_by_uid = {s["_id"]: s for s in stats}

    out = []
    for u in users:
        uid = str(u.get("_id"))
        s = stats_by_uid.get(uid, {})
        out.append(
            {
                "id": uid,
                "email": u.get("email"),
                "username": u.get("username"),
                "is_admin": bool(u.get("is_admin", False)),
                "is_fake": bool(u.get("is_fake", False)),
                "stats": {
                    "total": s.get("total", 0),
                    "watched": s.get("watched", 0),
                    "to_watch": s.get("to_watch", 0),
                    "watching": s.get("watching", 0),
                    "upcoming": s.get("upcoming", 0),
                    "avg_score": round(s["avg_score"], 1)
                    if s.get("avg_score") is not None
                    else None,
                },
            }
        )

    return out


# ======== UPDATE UTENTE (ADMIN) ========
@router.put("/users/{user_id}")
async def admin_update_user(
    user_id: str,
    payload: AdminUserUpdate,
    admin=Depends(require_admin),
):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user id")

    if str(admin["_id"]) == user_id and payload.is_admin is False:
        raise HTTPException(
            status_code=400, detail="You cannot remove your own admin role"
        )

    update_doc = {}

    if payload.email is not None:
        exists = await db["users"].find_one(
            {"email": payload.email, "_id": {"$ne": ObjectId(user_id)}}
        )
        if exists:
            raise HTTPException(status_code=400, detail="Email already in use")
        update_doc["email"] = payload.email

    if payload.username is not None:
        update_doc["username"] = payload.username

    if payload.password:
        update_doc["hashed_password"] = hash_password(payload.password)

    if payload.is_admin is not None:
        update_doc["is_admin"] = bool(payload.is_admin)

    if not update_doc:
        user = await db["users"].find_one(
            {"_id": ObjectId(user_id)}, {"email": 1, "username": 1, "is_admin": 1}
        )
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user["id"] = str(user["_id"])
        user.pop("_id", None)
        return user

    res = await db["users"].update_one({"_id": ObjectId(user_id)}, {"$set": update_doc})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    updated = await db["users"].find_one(
        {"_id": ObjectId(user_id)}, {"email": 1, "username": 1, "is_admin": 1}
    )
    updated["id"] = str(updated["_id"])
    updated.pop("_id", None)
    return updated


# ======== DELETE UTENTE (ADMIN) ========
@router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: str, admin=Depends(require_admin)):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user id")

    if str(admin["_id"]) == user_id:
        raise HTTPException(
            status_code=400, detail="You cannot delete your own account"
        )

    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db["users"].delete_one({"_id": ObjectId(user_id)})
    await db["movies"].delete_many({"user_id": user_id})
    # Elimina anche le attività, reazioni e commenti di questo utente
    await db["activities"].delete_many({"user_id": user_id})
    await db["activities"].update_many({}, {"$pull": {"reactions": {"user_id": user_id}}})
    await db["activities"].update_many({}, {"$pull": {"comments": {"user_id": user_id}}})
    # Elimina lo storico della chat dell'utente
    await db["ai_chat_history"].delete_many({"user_id": user_id})
    return


@router.get("/users/{user_id}/chat-history")
async def get_user_chat_history(user_id: str, admin=Depends(require_admin)):
    """
    Recupera lo storico chat di un qualsiasi utente (solo Admin).
    """
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user id")
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    cursor = db["ai_chat_history"].find({"user_id": user_id}).sort("created_at", 1)
    messages = await cursor.to_list(length=200)
    
    normalized = []
    for msg in messages:
        normalized.append({
            "role": msg["role"],
            "content": msg["content"],
            "recommendations": msg.get("recommendations", [])
        })
    return normalized



# ======== GENERATORE UTENTI FAKE & SIMULAZIONE COMMUNITY ========

PREFIXES = ["Cine", "Popcorn", "Movie", "Film", "Director", "Screen", "Plot", "Genre", "Retro", "Binge", "Oscar", "Indie", "Couch", "Frames", "Clapper", "Focus", "Lens", "Scene", "Spike", "Quentin", "Star", "Show"]
SUFFIXES = ["Buff", "Lover", "Queen", "King", "Geek", "Nerd", "Watcher", "Addict", "Fanatic", "Critic", "Guru", "Master", "Star", "Hunter", "Chaser", "Junkie", "Freak", "Wizard", "Knight"]

REVIEWS_TEMPLATES = {
    10: [
        "Un capolavoro assoluto! Regia impeccabile, colonna sonora pazzesca e interpretazione da Oscar.",
        "Uno dei film più belli che abbia mai visto. Mi ha lasciato senza parole dall'inizio alla fine.",
        "Perfetto sotto ogni punto di vista. Ti entra dentro e non ti lascia più. Voto 10/10!",
        "Stupendo, commovente, indimenticabile. Un'opera d'arte cinematografica."
    ],
    8: [
        "Davvero un ottimo film. La trama è solida e gli attori sono in stato di grazia. Consigliato!",
        "Molto bello! Mi ha tenuto incollato alla sedia. Ritmo perfetto e ottima regia.",
        "Una bellissima sorpresa. Non mi aspettavo un livello così alto. Da vedere sicuramente.",
        "Scritto benissimo e recitato altrettanto bene. Un film di grandissimo intrattenimento."
    ],
    6: [
        "Un buon intrattenimento per una serata rilassata. Non un capolavoro, ma si lascia guardare.",
        "Carino, l'idea di base è interessante ma lo sviluppo poteva essere migliore. Sufficienza piena.",
        "Un film piacevole ma senza troppe pretese. Alcune scene sono ottime, altre un po' lente.",
        "Onesto. Non annoia, ma non lascia un segno profondo. Cast discreto."
    ],
    4: [
        "Mi ha deluso parecchio. Le premesse c'erano tutte ma la trama fa acqua da tutte le parti.",
        "Abbastanza noioso ed estremamente prevedibile. Non mi è piaciuto per nulla.",
        "Occasione sprecata. Regia confusa e recitazione poco convincente. Peccato.",
        "Fatica ad arrivare alla fine. Piatto e privo di mordente. Sconsigliato."
    ],
    2: [
        "Pessimo. Uno dei film peggiori dell'anno. Regia inguardabile e dialoghi imbarazzanti.",
        "Tempo perso. Non si salva assolutamente nulla in questa produzione. Terribile.",
        "Veramente orribile. Storia senza senso e attori fuori parte. Statene lontani.",
        "Disastroso sotto ogni aspetto. Non riesco a trovare una singola nota positiva."
    ]
}

COMMENTS_TEMPLATES = [
    "Concordo pienamente con questa recensione!",
    "Anche a me è piaciuto moltissimo, uno dei migliori!",
    "Ce l'ho in lista da un po', mi hai fatto venire voglia di vederlo stasera.",
    "Secondo me è un po' sopravvalutato, ma comunque godibile.",
    "La colonna sonora in questa scena è qualcosa di spettacolare.",
    "Bello, ma il finale mi ha lasciato un po' con l'amaro in bocca.",
    "Cast pazzesco, solo per loro vale la pena guardarlo.",
    "Io l'ho trovato un po' lento nella parte centrale, ma nel complesso ci sta.",
    "Un classico intramontabile!",
    "La regia è davvero un'altra cosa qui."
]

POSTS_TEMPLATES = [
    "Stasera maratona cinematografica! Cosa mi consigliate tra un classico di Kubrick o un thriller moderno?",
    "Ho appena visto la mia serie preferita finire... quel senso di vuoto cosmico che ti lascia un finale perfetto. 😭",
    "Domanda del giorno: qual è il miglior sequel della storia del cinema? Per me senza dubbio Il Padrino - Parte II o Terminator 2.",
    "Adoro l'odore dei popcorn caldi appena prima che si spengano le luci in sala. C'è qualcosa di magico al cinema.",
    "Finalmente ho iniziato quella serie di cui parlano tutti. I primi due episodi sono promettenti!",
    "Alla ricerca di un bel film di fantascienza anni '80/'90 che mi sia sfuggito. Consigli?",
    "Che fatica trovare qualcosa di veramente originale ultimamente. Troppi remake e sequel non necessari.",
    "Consiglio spassionato: se non avete mai visto i film di Miyazaki, fatevi un regalo e recuperateli tutti!"
]

@router.post("/fake-users/generate")
async def generate_fake_users(
    count: int = Query(10, ge=1, le=50),
    admin=Depends(require_admin)
):
    """
    Genera utenti fake, popola le loro watchlists con film popolari reali presi da TMDb,
    crea attività social, e genera commenti e reazioni reciproche nel feed globale.
    """
    # 1. Recupera film popolari da TMDb
    titles_pool = []
    if settings.TMDB_API_KEY:
        async with httpx.AsyncClient(timeout=20) as client:
            for page in [1, 2]:
                # Film
                try:
                    res = await client.get(
                        "https://api.themoviedb.org/3/movie/popular",
                        params={"api_key": settings.TMDB_API_KEY, "language": "it-IT", "page": page}
                    )
                    if res.status_code == 200:
                        for item in res.json().get("results", []):
                            titles_pool.append({
                                "kind": "movie",
                                "title": item.get("title"),
                                "release_date": item.get("release_date"),
                                "poster_url": f"https://image.tmdb.org/t/p/w500{item['poster_path']}" if item.get("poster_path") else None,
                                "tmdb_id": item.get("id"),
                                "overview": item.get("overview"),
                                "tmdb_vote": item.get("vote_average")
                            })
                except Exception as e:
                    print(f"Error fetching movies from TMDB: {e}")
                
                # Serie TV
                try:
                    res = await client.get(
                        "https://api.themoviedb.org/3/tv/popular",
                        params={"api_key": settings.TMDB_API_KEY, "language": "it-IT", "page": page}
                    )
                    if res.status_code == 200:
                        for item in res.json().get("results", []):
                            titles_pool.append({
                                "kind": "tv",
                                "title": item.get("name"),
                                "release_date": item.get("first_air_date"),
                                "poster_url": f"https://image.tmdb.org/t/p/w500{item['poster_path']}" if item.get("poster_path") else None,
                                "tmdb_id": item.get("id"),
                                "overview": item.get("overview"),
                                "tmdb_vote": item.get("vote_average")
                            })
                except Exception as e:
                    print(f"Error fetching TV from TMDB: {e}")

    # Fallback in caso di assenza API key o errore di connessione
    if not titles_pool:
        titles_pool = [
            {"kind": "movie", "title": "Inception", "release_date": "2010-07-16", "poster_url": "https://image.tmdb.org/t/p/w500/9gk7adHYeHC5gh092yw1zsU6w2F.jpg", "tmdb_id": 27205, "overview": "Un ladro che ruba segreti aziendali...", "tmdb_vote": 8.4},
            {"kind": "movie", "title": "Pulp Fiction", "release_date": "1994-09-10", "poster_url": "https://image.tmdb.org/t/p/w500/d5i2fMNcj1wt6JUZeoaqgo1aEnz.jpg", "tmdb_id": 680, "overview": "Le vite di due sicari della mafia...", "tmdb_vote": 8.5},
            {"kind": "movie", "title": "Il Cavaliere Oscuro", "release_date": "2008-07-16", "poster_url": "https://image.tmdb.org/t/p/w500/qJ2tW6XJKtgIMj3q6889nS61OR3.jpg", "tmdb_id": 155, "overview": "Batman continua la sua lotta...", "tmdb_vote": 8.5},
            {"kind": "movie", "title": "Interstellar", "release_date": "2014-11-05", "poster_url": "https://image.tmdb.org/t/p/w500/gEU2QvH3w57v2xVzJv744Zbhjbp.jpg", "tmdb_id": 157336, "overview": "Un gruppo di esploratori viaggia...", "tmdb_vote": 8.4},
            {"kind": "movie", "title": "Fight Club", "release_date": "1999-10-15", "poster_url": "https://image.tmdb.org/t/p/w500/bptq15a7p5nHeLw8GI4v1COx4ns.jpg", "tmdb_id": 550, "overview": "Un impiegato insonne...", "tmdb_vote": 8.4},
            {"kind": "tv", "title": "Breaking Bad", "release_date": "2008-01-20", "poster_url": "https://image.tmdb.org/t/p/w500/ztkUQnBTTn9i31vquG7S0t0944X.jpg", "tmdb_id": 1396, "overview": "Un professore di chimica...", "tmdb_vote": 8.9},
            {"kind": "tv", "title": "Stranger Things", "release_date": "2016-07-15", "poster_url": "https://image.tmdb.org/t/p/w500/49WJfeN0mhmqj9R6Ok1k8t647ft.jpg", "tmdb_id": 66732, "overview": "La scomparsa di un ragazzino...", "tmdb_vote": 8.6}
        ]

    new_users = []
    generated_activities = []

    # 2. Genera utenti
    for _ in range(count):
        # Genera username unico
        username = ""
        for _ in range(5):  # Tenta 5 volte prima di cedere
            candidate = f"{random.choice(PREFIXES)}{random.choice(SUFFIXES)}{random.randint(10, 99)}"
            exists = await db["users"].find_one({"username": candidate})
            if not exists:
                username = candidate
                break
        if not username:
            username = f"User{uuid.uuid4().hex[:8]}"

        email = f"{username.lower()}@fake.popcornnote.com"
        
        # Cifra la password
        hashed_password = hash_password("password123")
        created_at_date = datetime.utcnow() - timedelta(days=random.randint(1, 30), hours=random.randint(1, 23))

        user_doc = {
            "email": email,
            "username": username,
            "hashed_password": hashed_password,
            "is_fake": True,
            "is_admin": False,
            "created_at": created_at_date
        }

        res = await db["users"].insert_one(user_doc)
        user_id = str(res.inserted_id)
        user_doc["_id"] = user_id
        new_users.append(user_doc)

        # 3. Popola watchlist (film/serie) per questo utente
        num_items = random.randint(5, 20)
        items_to_add = random.sample(titles_pool, min(num_items, len(titles_pool)))

        for item in items_to_add:
            status = random.choices(["watched", "to_watch", "watching", "upcoming"], weights=[65, 20, 8, 7])[0]
            
            score = None
            liked = None
            note = None

            if status in ["watched", "watching"]:
                # Genera voto
                score = random.choices([5, 6, 7, 8, 9, 10], weights=[5, 10, 30, 35, 15, 5])[0]
                
                # Associa giudizio qualitativo
                if score >= 9:
                    liked = random.choices(["loved", "liked"], weights=[80, 20])[0]
                elif score >= 7:
                    liked = random.choices(["liked", "loved", "okay"], weights=[80, 10, 10])[0]
                elif score >= 5:
                    liked = random.choices(["okay", "liked", "disliked"], weights=[80, 10, 10])[0]
                else:
                    liked = "disliked"

                # 40% possibilità di scrivere un commento/nota
                if random.random() < 0.4:
                    rounded_score_key = 10 if score >= 9 else (8 if score >= 7 else 6)
                    note = random.choice(REVIEWS_TEMPLATES[rounded_score_key])

            year = None
            if item.get("release_date"):
                try:
                    year = int(item["release_date"][:4])
                except:
                    pass

            movie_doc = {
                "user_id": user_id,
                "kind": item["kind"],
                "title": item["title"],
                "status": status,
                "score": score,
                "liked": liked,
                "note": note,
                "release_year": year,
                "release_date": item.get("release_date"),
                "poster_url": item.get("poster_url"),
                "tmdb_id": item.get("tmdb_id"),
                "overview": item.get("overview"),
                "tmdb_vote": item.get("tmdb_vote"),
                "created_at": created_at_date + timedelta(hours=random.randint(1, 48)),
                "updated_at": created_at_date + timedelta(hours=random.randint(1, 48))
            }

            if item["kind"] == "tv" and status == "watching":
                movie_doc["last_watched"] = {
                    "season": random.randint(1, 3),
                    "episode": random.randint(1, 10),
                    "updated_at": movie_doc["created_at"]
                }

            movie_res = await db["movies"].insert_one(movie_doc)
            movie_id = str(movie_res.inserted_id)

            # Crea attività social collegata
            activity_created_at = movie_doc["created_at"]
            if status == "watched" and note:
                activity_type = "rate_movie"
                activity_content = f"ha valutato {item['title']} con {score}/10: \"{note}\""
            else:
                activity_type = "add_movie"
                activity_status_ita = {
                    "watched": "visto",
                    "to_watch": "da vedere",
                    "watching": "in visione",
                    "upcoming": "in attesa di uscita"
                }.get(status, "lista")
                activity_content = f"ha aggiunto {item['title']} come '{activity_status_ita}'"

            activity_doc = {
                "user_id": user_id,
                "username": username,
                "type": activity_type,
                "content": activity_content,
                "movie_id": movie_id,
                "movie_title": item["title"],
                "movie_poster": item.get("poster_url"),
                "movie_score": float(score) if score else None,
                "reactions": [],
                "comments": [],
                "created_at": activity_created_at
            }
            act_res = await db["activities"].insert_one(activity_doc)
            activity_doc["_id"] = act_res.inserted_id
            generated_activities.append(activity_doc)

        # 30% possibilità di scrivere un post libero
        if random.random() < 0.3:
            post_content = random.choice(POSTS_TEMPLATES)
            post_doc = {
                "user_id": user_id,
                "username": username,
                "type": "post",
                "content": post_content,
                "reactions": [],
                "comments": [],
                "created_at": created_at_date + timedelta(days=random.randint(1, 3))
            }
            act_res = await db["activities"].insert_one(post_doc)
            post_doc["_id"] = act_res.inserted_id
            generated_activities.append(post_doc)

    # 4. Genera commenti e reazioni incrociate
    if len(new_users) > 1 and generated_activities:
        for act in generated_activities:
            # 50% possibilità di reazioni
            if random.random() < 0.5:
                num_reactions = random.randint(1, min(4, len(new_users)))
                reactors = random.sample(new_users, num_reactions)
                reactions_list = []
                for r in reactors:
                    if r["_id"] == act["user_id"]:
                        continue  # non reagisce a se stesso
                    reactions_list.append({
                        "user_id": r["_id"],
                        "type": random.choice(["like", "love", "funny", "fire", "popcorn"]),
                        "created_at": act["created_at"] + timedelta(minutes=random.randint(5, 180))
                    })
                if reactions_list:
                    await db["activities"].update_one(
                        {"_id": act["_id"]},
                        {"$set": {"reactions": reactions_list}}
                    )

            # 30% possibilità di commenti
            if random.random() < 0.3:
                num_comments = random.randint(1, min(2, len(new_users)))
                commenters = random.sample(new_users, num_comments)
                comments_list = []
                for c in commenters:
                    if c["_id"] == act["user_id"]:
                        continue  # non commenta se stesso
                    comments_list.append({
                        "id": str(uuid.uuid4()),
                        "user_id": c["_id"],
                        "username": c["username"],
                        "content": random.choice(COMMENTS_TEMPLATES),
                        "created_at": act["created_at"] + timedelta(minutes=random.randint(10, 240))
                    })
                if comments_list:
                    await db["activities"].update_one(
                        {"_id": act["_id"]},
                        {"$set": {"comments": comments_list}}
                    )

    return {
        "success": True,
        "message": f"Generati con successo {len(new_users)} utenti fake e popolata la community.",
        "generated_count": len(new_users)
    }


@router.delete("/fake-users", status_code=200)
async def delete_all_fake_users(admin=Depends(require_admin)):
    """
    Rimuove completamente tutti gli utenti fake dal database, i loro film
    e tutte le relative attività, commenti e reazioni nel feed.
    """
    # Trova tutti gli id utenti fake
    fake_users_cursor = db["users"].find({"is_fake": True}, {"_id": 1})
    fake_users = await fake_users_cursor.to_list(length=10000)
    fake_ids = [str(u["_id"]) for u in fake_users]

    if not fake_ids:
        return {"deleted_users": 0, "message": "Nessun utente fake trovato nel database."}

    # 1. Elimina i film associati
    movies_res = await db["movies"].delete_many({"user_id": {"$in": fake_ids}})

    # 2. Elimina le attività create da utenti fake
    activities_res = await db["activities"].delete_many({"user_id": {"$in": fake_ids}})

    # 3. Pulisci reazioni e commenti lasciati da utenti fake nei post degli altri
    # Rimuovi reazioni degli utenti fake da tutti i post rimanenti
    await db["activities"].update_many(
        {},
        {"$pull": {"reactions": {"user_id": {"$in": fake_ids}}}}
    )

    # Rimuovi commenti degli utenti fake da tutti i post rimanenti
    await db["activities"].update_many(
        {},
        {"$pull": {"comments": {"user_id": {"$in": fake_ids}}}}
    )

    # 3.5 Rimuovi storico chat degli utenti fake
    await db["ai_chat_history"].delete_many({"user_id": {"$in": fake_ids}})

    # 4. Elimina gli utenti
    users_res = await db["users"].delete_many({"is_fake": True})


    return {
        "deleted_users": users_res.deleted_count,
        "deleted_movies": movies_res.deleted_count,
        "deleted_activities": activities_res.deleted_count,
        "message": f"Eliminati con successo {users_res.deleted_count} utenti fake e tutti i loro dati correlati."
    }


# ======== IMPOSTAZIONI DI SISTEMA (API KEY & BOT AI) ========
class SystemSettingsUpdate(BaseModel):
    ai_provider: Optional[str] = "gemini"
    ai_api_key: Optional[str] = None
    ai_model: Optional[str] = "gemini-1.5-flash"
    ai_daily_limit_free: Optional[int] = Field(1, ge=1)
    ai_bot_enabled: Optional[bool] = True


@router.get("/settings")
async def get_system_settings(admin=Depends(require_admin)):
    """
    Recupera le impostazioni di sistema (API Key AI, limiti, provider).
    La chiave API viene restituita mascherata per sicurezza.
    """
    settings_doc = await db["system_settings"].find_one({"_id": "global"}) or {}
    
    raw_key = settings_doc.get("ai_api_key") or settings.TMDB_API_KEY  # o env fallback
    masked_key = ""
    if raw_key:
        if len(raw_key) > 8:
            masked_key = raw_key[:4] + "•" * (len(raw_key) - 8) + raw_key[-4:]
        else:
            masked_key = "••••••••"

    return {
        "ai_provider": settings_doc.get("ai_provider", "gemini"),
        "ai_api_key_set": bool(raw_key),
        "ai_api_key_masked": masked_key,
        "ai_model": settings_doc.get("ai_model", "gemini-1.5-flash"),
        "ai_daily_limit_free": settings_doc.get("ai_daily_limit_free", 1),
        "ai_bot_enabled": settings_doc.get("ai_bot_enabled", True)
    }


@router.post("/settings")
async def update_system_settings(
    settings_data: SystemSettingsUpdate,
    admin=Depends(require_admin)
):
    """
    Aggiorna le impostazioni di sistema in MongoDB.
    """
    update_dict = {}
    if settings_data.ai_provider is not None:
        update_dict["ai_provider"] = settings_data.ai_provider
    if settings_data.ai_api_key is not None and settings_data.ai_api_key.strip() != "":
        # Se non è una chiave mascherata, salvala
        if "•" not in settings_data.ai_api_key:
            update_dict["ai_api_key"] = settings_data.ai_api_key.strip()
    if settings_data.ai_model is not None:
        update_dict["ai_model"] = settings_data.ai_model
    if settings_data.ai_daily_limit_free is not None:
        update_dict["ai_daily_limit_free"] = settings_data.ai_daily_limit_free
    if settings_data.ai_bot_enabled is not None:
        update_dict["ai_bot_enabled"] = settings_data.ai_bot_enabled

    if update_dict:
        update_dict["updated_at"] = datetime.utcnow()
        await db["system_settings"].update_one(
            {"_id": "global"},
            {"$set": update_dict},
            upsert=True
        )
    return {"message": "Impostazioni salvate con successo"}

