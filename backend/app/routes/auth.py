#app/routes/auth.py
from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user import UserCreate, UserLogin
from app.utils.auth import hash_password, verify_password, create_access_token
from app.db import db
from app.dependencies import get_current_user  # 👈 importa la dipendenza

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register(user: UserCreate):
    existing = await db["users"].find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = hash_password(user.password)
    new_user = {"email": user.email, "username": user.username, "hashed_password": hashed_pw}
    result = await db["users"].insert_one(new_user)
    return {"id": str(result.inserted_id), "email": user.email, "username": user.username}

@router.post("/login")
async def login(user: UserLogin):
    db_user = await db["users"].find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    token = create_access_token({"sub": db_user["email"]})
    return {"access_token": token, "token_type": "bearer"}


# 👇 NUOVO: profilo utente corrente
@router.get("/me")
async def me(user=Depends(get_current_user)):
    return {
        "id": str(user["_id"]),
        "email": user.get("email"),
        "username": user.get("username") or (user.get("email", "").split("@")[0] if user.get("email") else None),
        "is_admin": bool(user.get("is_admin", False)),
    }

@router.post("/refresh")
async def refresh(user=Depends(get_current_user)):
    """
    Endpoint per rinnovare il token (heartbeat).
    Richiede un token valido (non scaduto).
    Restituisce un nuovo token con scadenza resettata.
    """
    new_token = create_access_token({"sub": user["email"]})
    return {"access_token": new_token, "token_type": "bearer"}