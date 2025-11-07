# app/utils/auth.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.config import settings
import bcrypt

# --- PASSWORD HASH / VERIFY con bcrypt nativo ---

def hash_password(password: str) -> str:
    # bcrypt accetta max 72 byte: se vuoi, tronca tu (opzionale)
    pw_bytes = password.encode("utf-8")
    # opzionale: enforce limite esplicito
    if len(pw_bytes) > 72:
        pw_bytes = pw_bytes[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pw_bytes, salt)
    return hashed.decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    try:
        pw_bytes = password.encode("utf-8")
        if len(pw_bytes) > 72:
            pw_bytes = pw_bytes[:72]
        return bcrypt.checkpw(pw_bytes, hashed.encode("utf-8"))
    except Exception:
        # evita 500 per hash malformati / eccezioni strane
        return False

# --- JWT ---

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None
