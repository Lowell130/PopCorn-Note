# app/utils/run.py
import asyncio
import argparse
from datetime import datetime
from typing import Any, Dict

from app.db import db   # usa il client Motor già configurato
try:
    from app.utils.text import normalize_title
except Exception:
    # fallback ultra-semplice nel caso la utility non fosse disponibile
    import re
    _WS = re.compile(r"\s+")
    def normalize_title(s: str) -> str:
        return _WS.sub(" ", (s or "")).strip().lower()

COLL = "movies"

def to_int_or_none(v):
    if v is None:
        return None
    if isinstance(v, int):
        return v
    if isinstance(v, str) and v.isdigit():
        try:
            return int(v)
        except Exception:
            return None
    return None

def year_from_date(d: Any):
    if not d or not isinstance(d, str) or len(d) < 4:
        return None
    try:
        return int(d[:4])
    except Exception:
        return None

async def migrate(dry_run: bool = True) -> None:
    coll = db[COLL]

    cursor = coll.find({}, projection=None)
    total = 0
    to_update = 0

    print("▶ Inizio scansione documenti…")
    async for doc in cursor:
        total += 1
        updates: Dict[str, Any] = {}

        # 1) kind: default "movie" se mancante
        if "kind" not in doc or doc.get("kind") not in ("movie", "tv"):
            updates["kind"] = "movie"

        # 2) normalized_title dal titolo
        title = doc.get("title") or ""
        norm_now = normalize_title(title)
        if not doc.get("normalized_title") or doc.get("normalized_title") != norm_now:
            updates["normalized_title"] = norm_now

        # 3) release_year da release_date se mancante
        if doc.get("release_year") is None and doc.get("release_date"):
            y = year_from_date(doc.get("release_date"))
            if y is not None:
                updates["release_year"] = y

        # 4) tmdb_id → int, se possibile
        tmdb_id_fixed = to_int_or_none(doc.get("tmdb_id"))
        if tmdb_id_fixed is not None and tmdb_id_fixed != doc.get("tmdb_id"):
            updates["tmdb_id"] = tmdb_id_fixed

        if updates:
            to_update += 1
            updates["updated_at"] = datetime.utcnow()
            if dry_run:
                print(f"• DRY-RUN aggiornerei _id={doc.get('_id')} con: {updates}")
            else:
                await coll.update_one({"_id": doc["_id"]}, {"$set": updates})

    print(f"\n✅ Scansione completata. Documenti totali: {total}")
    if dry_run:
        print(f"🧪 DRY-RUN: documenti da aggiornare: {to_update} (nessuna modifica scritta).")
    else:
        print(f"✍️  Aggiornati {to_update} documenti.")

async def main():
    parser = argparse.ArgumentParser(description="Migrazione movies: kind/normalized_title/anni/tmdb_id")
    parser.add_argument("--apply", action="store_true", help="Esegue realmente gli update (default: dry run).")
    args = parser.parse_args()

    await migrate(dry_run=not args.apply)

if __name__ == "__main__":
    asyncio.run(main())
