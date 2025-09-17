#dependency.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.utils.auth import decode_token
from app.db import db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = await db["users"].find_one({"email": payload.get("sub")})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def is_truthy_admin(val):
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        return val.strip().lower() in ("true", "1", "yes", "y")
    return False

async def require_admin(user = Depends(get_current_user)):
    if not is_truthy_admin(user.get("is_admin", False)):
        raise HTTPException(status_code=403, detail="Admins only")
    return user