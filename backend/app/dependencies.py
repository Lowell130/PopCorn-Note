# app/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.utils.auth import decode_token
from app.db import db
import calendar

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def is_truthy_admin(val):
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        return val.strip().lower() in ("true", "1", "yes", "y")
    if isinstance(val, int):
        return val == 1
    return False


def is_admin_user(user) -> bool:
    """Unico punto di verità per stabilire se un utente è admin."""
    return bool(user) and is_truthy_admin(user.get("is_admin", False))


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if payload is None or not payload.get("sub"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = await db["users"].find_one({"email": payload.get("sub")})
    if user is None or user.get("is_fake"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    # Token emessi prima dell'ultimo cambio password non sono più validi
    changed_at = user.get("password_changed_at")
    iat = payload.get("iat")
    if changed_at and iat is not None and int(iat) < calendar.timegm(changed_at.utctimetuple()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired")

    return user


async def require_admin(user=Depends(get_current_user)):
    if not is_admin_user(user):
        raise HTTPException(status_code=403, detail="Admins only")
    return user
