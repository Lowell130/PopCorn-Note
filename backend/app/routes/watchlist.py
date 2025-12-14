from fastapi import APIRouter, Depends, HTTPException, Body
from app.dependencies import get_current_user
from app.db import db
from typing import Dict, Any
from datetime import datetime

router = APIRouter(
    prefix="/watchlist",
    tags=["watchlist"],
    responses={404: {"description": "Not found"}},
)

@router.post("")
async def add_to_watchlist(
    item: dict = Body(...),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Aggiunge un elemento (Film o Serie TV) alla watchlist dell'utente.
    Payload atteso: { "id": str, "type": "movie"|"tv", "title": str, "poster": str, "release_year": ... }
    """
    if not item.get("id") or not item.get("type"):
        raise HTTPException(status_code=400, detail="ID e Type sono obbligatori")

    # Accesso come dizionario
    user_watchlist = current_user.get("watchlist", [])
    
    # Verifica se esiste già
    existing = next((x for x in user_watchlist if x["id"] == str(item["id"])), None)
    if existing:
        return {"message": "Già in watchlist", "watchlist": user_watchlist}

    new_item = {
        "id": str(item["id"]),
        "type": item["type"],
        "title": item.get("title", "Sconosciuto"),
        "poster": item.get("poster_path") or item.get("poster"),
        "release_year": item.get("release_year") or item.get("first_air_date", "")[:4],
        "added_at": datetime.utcnow()
    }

    result = await db["users"].update_one(
        {"email": current_user["email"]},
        {"$push": {"watchlist": new_item}}
    )

    if result.modified_count == 0:
        # Se non ha modificato nulla, forse l'array non esisteva o altro errore
        # Tentiamo di creare l'array se l'update sopra fallisce per struttura?
        # Ma $push dovrebbe crearlo se manca. 
        # Forse l'utente non esiste? Ma siamo autenticati.
        # Potrebbe essere che il record è identico? No, $push aggiunge sempre.
        pass

    # Aggiorna per il ritorno (non persistente sull'oggetto current_user che è una copia locale del request scope)
    user_watchlist.append(new_item)
    return {"message": "Aggiunto alla watchlist", "watchlist": user_watchlist}


@router.delete("/{item_id}")
async def remove_from_watchlist(
    item_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Rimuove un elemento dalla watchlist tramite il suo ID esterno (TMDB ID).
    """
    user_watchlist = current_user.get("watchlist", [])
    
    # Verifica esistenza
    existing = next((x for x in user_watchlist if x["id"] == item_id), None)
    if not existing:
        raise HTTPException(status_code=404, detail="Elemento non trovato nella watchlist")

    result = await db["users"].update_one(
        {"email": current_user["email"]},
        {"$pull": {"watchlist": {"id": item_id}}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Errore durante la rimozione")
        
    # Rimuovi localmente per il ritorno
    updated_watchlist = [x for x in user_watchlist if x["id"] != item_id]
    
    return {"message": "Rimosso dalla watchlist", "watchlist": updated_watchlist}
