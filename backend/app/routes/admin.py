# app/routes/admin.py
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
import re

from app.db import db
from app.dependencies import require_admin
from app.utils.auth import hash_password
from app.routes.auth import USERNAME_RE, _validate_password, _email_query
from datetime import datetime

router = APIRouter(prefix="/admin", tags=["Admin"])


# ======== MODELLI ========
class AdminUserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=2, max_length=50)
    password: Optional[str] = Field(None, min_length=8, max_length=128)
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


# ======== CREA UTENTE (ADMIN) ========
# Le registrazioni pubbliche sono chiuse: i nuovi account li crea l'admin.
class AdminUserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., max_length=100)
    password: str = Field(..., max_length=256)
    is_admin: bool = False


@router.post("/users", status_code=201)
async def admin_create_user(payload: AdminUserCreate, admin=Depends(require_admin)):
    email = payload.email.strip().lower()
    username = payload.username.strip()
    if not USERNAME_RE.match(username):
        raise HTTPException(status_code=400, detail="Lo username deve avere 3-30 caratteri: lettere, numeri, punto, trattino o underscore")
    _validate_password(payload.password)
    if await db["users"].find_one(_email_query(email)):
        raise HTTPException(status_code=400, detail="Email già registrata")
    if await db["users"].find_one({"username": re.compile(f"^{re.escape(username)}$", re.IGNORECASE)}):
        raise HTTPException(status_code=400, detail="Username già in uso")
    doc = {
        "email": email,
        "username": username,
        "hashed_password": hash_password(payload.password),
        "is_admin": bool(payload.is_admin),
        "created_at": datetime.utcnow(),
    }
    res = await db["users"].insert_one(doc)
    return {
        "id": str(res.inserted_id), "email": email, "username": username,
        "is_admin": doc["is_admin"], "is_fake": False,
        "stats": {"total": 0, "watched": 0, "to_watch": 0, "watching": 0, "upcoming": 0, "avg_score": None},
    }


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
        uname = payload.username.strip()
        taken = await db["users"].find_one({
            "username": re.compile(f"^{re.escape(uname)}$", re.IGNORECASE),
            "_id": {"$ne": ObjectId(user_id)},
        })
        if taken:
            raise HTTPException(status_code=400, detail="Username already in use")
        update_doc["username"] = uname

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



# ======== STATISTICHE SINGOLO UTENTE (ADMIN) ========
@router.get("/users/{user_id}/stats")
async def admin_user_stats(user_id: str, admin=Depends(require_admin)):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user id")
    if not await db["users"].find_one({"_id": ObjectId(user_id)}, {"_id": 1}):
        raise HTTPException(status_code=404, detail="User not found")

    movie_filter = {"$or": [{"kind": "movie"}, {"kind": {"$exists": False}}]}
    total_movies = await db["movies"].count_documents({"user_id": user_id, **movie_filter})
    total_series = await db["movies"].count_documents({"user_id": user_id, "kind": "tv"})
    counts = {}
    for st in ("watched", "to_watch", "watching", "upcoming"):
        counts[st] = await db["movies"].count_documents({"user_id": user_id, "status": st})
    agg = await db["movies"].aggregate([
        {"$match": {"user_id": user_id, "score": {"$type": "number", "$gte": 1, "$lte": 10}}},
        {"$group": {"_id": None, "avg": {"$avg": "$score"}}},
    ]).to_list(length=1)
    return {
        "total_movies": total_movies,
        "total_series": total_series,
        **counts,
        "avg_score": round(agg[0]["avg"], 1) if agg and agg[0].get("avg") is not None else None,
    }
