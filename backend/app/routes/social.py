# app/routes/social.py
from fastapi import APIRouter, Depends, HTTPException, Body
from app.db import db
from app.dependencies import get_current_user
from app.models.activity import Activity
from typing import List
from datetime import datetime

router = APIRouter(prefix="/social", tags=["Social"])

def _normalize(doc):
    doc["id"] = str(doc["_id"])
    doc.pop("_id", None)
    return doc

@router.get("/feed", response_model=List[Activity])
async def get_feed(limit: int = 50, user=Depends(get_current_user)):
    """
    Restituisce il feed globale delle attività.
    Accessibile SOLO agli utenti registrati.
    """
    cursor = db["activities"].find().sort("created_at", -1).limit(limit)
    activities = await cursor.to_list(length=limit)
    return [_normalize(a) for a in activities]

@router.post("/post", response_model=Activity)
async def create_post(
    content: str = Body(..., embed=True),
    user=Depends(get_current_user)
):
    """
    Crea un post manuale nel feed.
    """
    if not content.strip():
        raise HTTPException(status_code=400, detail="Il post non può essere vuoto")

    doc = {
        "user_id": str(user["_id"]),
        "username": user.get("username") or user["email"].split("@")[0],
        "type": "post",
        "content": content,
        "created_at": datetime.utcnow()
    }
    
    res = await db["activities"].insert_one(doc)
    new_doc = await db["activities"].find_one({"_id": res.inserted_id})
    return _normalize(new_doc)

@router.delete("/{activity_id}", status_code=204)
async def delete_activity(activity_id: str, user=Depends(get_current_user)):
    """
    Elimina un'attività. Solo admin o proprietario (implementazione semplice: solo admin per ora).
    """
    from bson import ObjectId
    
    # Check admin
    if not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Richiede privilegi di amministratore")
        
    res = await db["activities"].delete_one({"_id": ObjectId(activity_id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Activity not found")
    return

@router.post("/{activity_id}/react")
async def react_to_activity(
    activity_id: str,
    reaction_type: str = Body(..., embed=True),
    user=Depends(get_current_user)
):
    """
    Aggiungi o aggiorna la tua reazione a un'attività.
    Tipi validi: like, love, funny, fire, popcorn, dislike
    """
    from bson import ObjectId
    
    valid_types = ["like", "love", "funny", "fire", "popcorn", "dislike"]
    if reaction_type not in valid_types:
        raise HTTPException(status_code=400, detail="Tipo di reazione non valido")
    
    user_id = str(user["_id"])
    
    # Rimuovi eventuali reazioni precedenti dello stesso utente
    await db["activities"].update_one(
        {"_id": ObjectId(activity_id)},
        {"$pull": {"reactions": {"user_id": user_id}}}
    )
    
    # Aggiungi la nuova reazione
    result = await db["activities"].update_one(
        {"_id": ObjectId(activity_id)},
        {"$push": {"reactions": {
            "user_id": user_id,
            "type": reaction_type,
            "created_at": datetime.utcnow()
        }}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    return {"success": True}

@router.delete("/{activity_id}/react")
async def unreact_to_activity(activity_id: str, user=Depends(get_current_user)):
    """
    Rimuovi la tua reazione da un'attività.
    """
    from bson import ObjectId
    
    user_id = str(user["_id"])
    
    result = await db["activities"].update_one(
        {"_id": ObjectId(activity_id)},
        {"$pull": {"reactions": {"user_id": user_id}}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    return {"success": True}

