# app/utils/rate_limit.py
"""
Rate limiting semplice basato su MongoDB.
Funziona anche in ambienti serverless (Vercel / Cloud Run) dove la memoria
del processo non è condivisa tra le istanze.
"""
from datetime import datetime, timedelta
from fastapi import HTTPException, Request
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError

from app.db import db

COLL = "rate_limits"


def client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    real = request.headers.get("x-real-ip")
    if real:
        return real.strip()
    return request.client.host if request.client else "unknown"


async def ensure_indexes():
    # TTL: i documenti scaduti vengono eliminati automaticamente da Mongo
    await db[COLL].create_index("expires_at", expireAfterSeconds=0)
    await db[COLL].create_index("key", unique=True)


async def is_blocked(key: str, max_attempts: int) -> bool:
    doc = await db[COLL].find_one({"key": key})
    if not doc:
        return False
    if doc.get("expires_at") and doc["expires_at"] < datetime.utcnow():
        return False
    return doc.get("count", 0) >= max_attempts


async def hit(key: str, window_seconds: int) -> int:
    """Registra un tentativo e restituisce il numero di tentativi nella finestra."""
    now = datetime.utcnow()
    # se la finestra è scaduta (e il TTL non ha ancora ripulito) riparti da zero
    await db[COLL].delete_one({"key": key, "expires_at": {"$lt": now}})
    update = {
        "$inc": {"count": 1},
        "$setOnInsert": {"expires_at": now + timedelta(seconds=window_seconds)},
    }
    try:
        doc = await db[COLL].find_one_and_update(
            {"key": key}, update, upsert=True, return_document=ReturnDocument.AFTER
        )
    except DuplicateKeyError:
        # due richieste concorrenti hanno creato il documento: riprova senza upsert
        doc = await db[COLL].find_one_and_update(
            {"key": key}, {"$inc": {"count": 1}}, return_document=ReturnDocument.AFTER
        )
    return (doc or {}).get("count", 1)


async def reset(key: str):
    await db[COLL].delete_one({"key": key})


async def enforce(key: str, max_attempts: int, window_seconds: int, message: str):
    """Conta il tentativo e blocca con 429 se si supera il limite."""
    count = await hit(key, window_seconds)
    if count > max_attempts:
        raise HTTPException(status_code=429, detail=message)
