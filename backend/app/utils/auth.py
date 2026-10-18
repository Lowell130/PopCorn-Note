# app/utils/auth.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.config import settings
import bcrypt
import time

# --- PASSWORD HASH / VERIFY con bcrypt nativo ---

# hash fittizio usato per rendere costante il tempo di risposta del login
# anche quando l'email non esiste (evita l'enumerazione degli utenti)
_DUMMY_HASH = bcrypt.hashpw(b"popcornnote-dummy-password", bcrypt.gensalt()).decode("utf-8")


def _pw_bytes(password: str) -> bytes:
    # bcrypt accetta max 72 byte
    return (password or "").encode("utf-8")[:72]


def hash_password(password: str) -> str:
    return bcrypt.hashpw(_pw_bytes(password), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(_pw_bytes(password), (hashed or _DUMMY_HASH).encode("utf-8"))
    except Exception:
        # evita 500 per hash malformati / eccezioni strane
        return False


def burn_password_check(password: str) -> None:
    """Esegue un confronto bcrypt a vuoto (stesso costo di un login reale)."""
    verify_password(password, _DUMMY_HASH)


# --- JWT ---

def create_access_token(data: dict):
    to_encode = data.copy()
    now = datetime.utcnow()
    expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "iat": int(time.time())})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None
