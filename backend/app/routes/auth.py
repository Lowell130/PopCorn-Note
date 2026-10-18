#app/routes/auth.py
import re
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, Request
from app.schemas.user import UserLogin, ChangePassword
from app.utils.auth import hash_password, verify_password, create_access_token, burn_password_check
from app.utils import rate_limit
from app.db import db
from app.dependencies import get_current_user, is_admin_user

router = APIRouter(prefix="/auth", tags=["Auth"])

USERNAME_RE = re.compile(r"^[A-Za-z0-9_.-]{3,30}$")
PASSWORD_MIN = 8

# Limiti anti brute-force
LOGIN_MAX_PER_EMAIL = 5        # tentativi falliti per email
LOGIN_MAX_PER_IP = 20          # tentativi falliti per IP
LOGIN_WINDOW = 15 * 60         # 15 minuti


def _validate_password(pw: str):
    if len(pw) < PASSWORD_MIN:
        raise HTTPException(status_code=400, detail=f"La password deve contenere almeno {PASSWORD_MIN} caratteri")
    if pw.isdigit() or pw.isalpha():
        raise HTTPException(status_code=400, detail="La password deve contenere sia lettere che numeri o simboli")


def _email_query(email: str) -> dict:
    """Match case-insensitive sull'email (gli utenti storici possono avere maiuscole)."""
    return {"email": re.compile(f"^{re.escape(email.strip())}$", re.IGNORECASE)}


async def _find_user_by_email(email: str):
    user = await db["users"].find_one({"email": email.strip().lower()})
    if user:
        return user
    return await db["users"].find_one(_email_query(email))


@router.delete("/me", status_code=204)
async def delete_account(user=Depends(get_current_user)):
    """
    Elimina permanentemente l'account utente e tutti i dati associati.
    """
    user_id = str(user["_id"])

    await db["movies"].delete_many({"user_id": user_id})
    await db["activities"].delete_many({"user_id": user_id})
    await db["activities"].update_many({}, {"$pull": {"reactions": {"user_id": user_id}}})
    await db["activities"].update_many({}, {"$pull": {"comments": {"user_id": user_id}}})
    await db["ai_chat_history"].delete_many({"user_id": user_id})

    res = await db["users"].delete_one({"_id": user["_id"]})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return


@router.post("/change-password")
async def change_password(data: ChangePassword, request: Request, user=Depends(get_current_user)):
    """
    Consente all'utente di cambiare la propria password.
    Restituisce un nuovo token: le altre sessioni aperte vengono invalidate.
    """
    rl_key = f"chpw:{user['_id']}"
    if await rate_limit.is_blocked(rl_key, LOGIN_MAX_PER_EMAIL):
        raise HTTPException(status_code=429, detail="Troppi tentativi. Riprova tra qualche minuto.")

    if not verify_password(data.current_password, user["hashed_password"]):
        await rate_limit.hit(rl_key, LOGIN_WINDOW)
        raise HTTPException(status_code=400, detail="La password corrente non è corretta")

    if verify_password(data.new_password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="La nuova password deve essere diversa da quella attuale")

    _validate_password(data.new_password)

    await db["users"].update_one(
        {"_id": user["_id"]},
        {"$set": {
            "hashed_password": hash_password(data.new_password),
            "password_changed_at": datetime.utcnow().replace(microsecond=0),
        }}
    )
    await rate_limit.reset(rl_key)

    token = create_access_token({"sub": user["email"]})
    return {"detail": "Password aggiornata con successo", "access_token": token, "token_type": "bearer"}


@router.post("/login")
async def login(user: UserLogin, request: Request):
    ip = rate_limit.client_ip(request)
    email_key = f"login:email:{user.email.strip().lower()}"
    ip_key = f"login:ip:{ip}"

    if await rate_limit.is_blocked(email_key, LOGIN_MAX_PER_EMAIL) or \
       await rate_limit.is_blocked(ip_key, LOGIN_MAX_PER_IP):
        raise HTTPException(status_code=429, detail="Troppi tentativi di accesso. Riprova tra 15 minuti.")

    db_user = await _find_user_by_email(user.email)

    if not db_user or db_user.get("is_fake"):
        burn_password_check(user.password)
        ok = False
    else:
        ok = verify_password(user.password, db_user.get("hashed_password"))

    if not ok:
        await rate_limit.hit(email_key, LOGIN_WINDOW)
        await rate_limit.hit(ip_key, LOGIN_WINDOW)
        raise HTTPException(status_code=400, detail="Email o password non corretti")

    await rate_limit.reset(email_key)
    token = create_access_token({"sub": db_user["email"]})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
async def me(user=Depends(get_current_user)):
    return {
        "id": str(user["_id"]),
        "email": user.get("email"),
        "username": user.get("username") or (user.get("email", "").split("@")[0] if user.get("email") else None),
        "is_admin": is_admin_user(user),
        "watchlist": user.get("watchlist", [])
    }


@router.post("/refresh")
async def refresh(user=Depends(get_current_user)):
    """
    Endpoint per rinnovare il token (heartbeat).
    Richiede un token valido (non scaduto).
    """
    new_token = create_access_token({"sub": user["email"]})
    return {"access_token": new_token, "token_type": "bearer"}
