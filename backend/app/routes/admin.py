# app/routes/admin.py
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId

from app.db import db
from app.dependencies import require_admin
from app.utils.auth import hash_password

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
    users_cur = db["users"].find({}, {"email": 1, "username": 1, "is_admin": 1})
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
    return
