# app/routes/admin.py
from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from app.db import db
from app.dependencies import require_admin  # deve restituire l'utente se is_admin=True

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users")
async def list_users_with_stats(admin=Depends(require_admin)):
    # utenti (prendo email/username/is_admin; _id arriva di default)
    users_cur = db["users"].find({}, {"email": 1, "username": 1, "is_admin": 1})
    users = await users_cur.to_list(length=10000)

    # aggregazione statistiche per utente
    pipe = [
        {
            "$group": {
                "_id": "$user_id",
                "total": {"$sum": 1},
                "watched": {"$sum": {"$cond": [{"$eq": ["$status", "watched"]}, 1, 0]}},
                "to_watch": {"$sum": {"$cond": [{"$eq": ["$status", "to_watch"]}, 1, 0]}},
                "watching": {"$sum": {"$cond": [{"$eq": ["$status", "watching"]}, 1, 0]}},
                "upcoming": {"$sum": {"$cond": [{"$eq": ["$status", "upcoming"]}, 1, 0]}},
                # media solo se score numerico tra 1..10, altrimenti ignora
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
                    "avg_score": round(s["avg_score"], 1) if s.get("avg_score") is not None else None,
                },
            }
        )

    return out


@router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: str, admin=Depends(require_admin)):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user id")

    # impedisci la cancellazione di se stessi
    if str(admin["_id"]) == user_id:
        raise HTTPException(status_code=400, detail="You cannot delete your own account")

    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # opzionale: vieta cancellazione di altri admin
    # if user.get("is_admin"):
    #     raise HTTPException(status_code=400, detail="Cannot delete another admin")

    await db["users"].delete_one({"_id": ObjectId(user_id)})
    await db["movies"].delete_many({"user_id": user_id})
    return
