# app/routes/ai.py
from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from datetime import datetime, timezone
import httpx
import json
import re

from app.dependencies import get_current_user
from app.db import db
from app.config import settings

router = APIRouter(prefix="/ai", tags=["AI"])

TMDB_BASE = "https://api.themoviedb.org/3"

class ChatRequest(BaseModel):
    message: str
    chat_history: Optional[List[Dict[str, str]]] = []

@router.get("/usage")
async def get_ai_usage(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Restituisce l'utilizzo corrente dell'AI per l'utente loggato.
    """
    user_id = str(current_user["_id"])
    is_admin = bool(current_user.get("is_admin", False))
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    settings_doc = await db["system_settings"].find_one({"_id": "global"}) or {}
    daily_limit = settings_doc.get("ai_daily_limit_free", 1)
    ai_bot_enabled = settings_doc.get("ai_bot_enabled", True)

    usage_doc = await db["ai_usage"].find_one({"user_id": user_id, "date": today_str}) or {}
    today_count = usage_doc.get("count", 0)

    remaining = "illimitate" if is_admin else max(0, daily_limit - today_count)

    return {
        "is_admin": is_admin,
        "today_count": today_count,
        "daily_limit": daily_limit if not is_admin else "illimitato",
        "remaining": remaining,
        "can_request": (is_admin or (today_count < daily_limit)) and ai_bot_enabled,
        "ai_bot_enabled": ai_bot_enabled
    }


async def _call_llm(user_message: str, chat_history: List[Dict[str, str]], context_prompt: str, api_key: str, provider: str, model_name: str) -> str:
    """
    Esegue la chiamata all'API dell'LLM (Gemini o OpenAI o Mock).
    """
    if not api_key:
        # Fallback Mock elegante se l'admin non ha ancora impostato una API Key
        return """Ciao! Sono **PopCorn Bot** 🍿.
Al momento la chiave API dell'AI non è stata configurata dal pannello Admin, ma ecco un paio di ottimi suggerimenti basati sulle tue richieste:

```json
[
  {"title": "Upgrade", "kind": "movie", "year": "2018", "reason": "Azione e fantascienza ad alto ritmo"},
  {"title": "Severance", "kind": "tv", "year": "2022", "reason": "Thriller psicologico e mistero"}
]
```
Spero ti piacciano! L'amministratore può inserire una chiave API valida nella sezione Admin Settings."""

    system_instruction = f"""Sei PopCorn Bot, un assistente esperto e divertente di cinema e serie TV per l'app PopCornNote.
Il tuo compito è aiutare l'utente a scoprire NUOVI film o serie TV che NON sono ancora nella sua libreria.
Rispondi SEMPRE in ITALIANO con un tono amichevole, appassionato ed uso di emoji simpatiche.

{context_prompt}

IMPORTANTE: Alla fine del tuo messaggio, DEVI INCLUDERE una lista di film/serie raccomandati racchiusa in un blocco di codice JSON con la seguente struttura esatta:
```json
[
  {{
    "title": "Nome del Film o Serie",
    "kind": "movie" o "tv",
    "year": "2023",
    "reason": "Breve frase sul perché lo consigli"
  }}
]
```
Consiglia tra 1 e 3 titoli ad ogni risposta."""

    async with httpx.AsyncClient(timeout=25.0) as client:
        if provider == "openai":
            # API OpenAI Chat Completions
            url = "https://api.openai.com/v1/chat/completions"
            messages = [{"role": "system", "content": system_instruction}]
            for h in chat_history[-6:]:
                messages.append({"role": h.get("role", "user"), "content": h.get("content", "")})
            messages.append({"role": "user", "content": user_message})

            resp = await client.post(
                url,
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"model": model_name or "gpt-4o-mini", "messages": messages, "temperature": 0.7}
            )
            if resp.status_code != 200:
                raise Exception(f"Errore API OpenAI: {resp.status_code} - {resp.text}")
            data = resp.json()
            return data["choices"][0]["message"]["content"]

        else:
            # Default: API Google Gemini con ciclo di tentativi su modelli supportati
            primary_model = (model_name or "gemini-3.5-flash").replace("models/", "").strip()
            
            # Elenco di modelli supportati ed attivi
            candidate_models = [
                primary_model,
                "gemini-3.5-flash",
                "gemini-3.1-flash-lite",
                "gemini-flash-latest",
                "gemini-pro-latest",
                "gemini-2.0-flash"
            ]
            
            # Rimuovi duplicati mantenendo l'ordine
            seen = set()
            models_to_try = []
            for m in candidate_models:
                if m and m not in seen:
                    seen.add(m)
                    models_to_try.append(m)

            contents = []
            # Context iniziale
            contents.append({"role": "user", "parts": [{"text": system_instruction}]})
            contents.append({"role": "model", "parts": [{"text": "Capito! Sono PopCorn Bot, pronto ad aiutare l'utente con suggerimenti personalizzati sul cinema."}]})

            for h in chat_history[-6:]:
                role = "user" if h.get("role") == "user" else "model"
                contents.append({"role": role, "parts": [{"text": h.get("content", "")}]})

            contents.append({"role": "user", "parts": [{"text": user_message}]})

            last_error = ""
            for m in models_to_try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={api_key}"
                try:
                    resp = await client.post(
                        url,
                        headers={"Content-Type": "application/json"},
                        json={"contents": contents}
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        return data["candidates"][0]["content"]["parts"][0]["text"]
                    elif resp.status_code == 429:
                        raise Exception("Quota API Google esaurita (429): La tua chiave API Gemini ha raggiunto il limite di richieste gratuite o il tuo progetto Google Cloud ha quota 0. Controlla ai.google.dev per abilitare il piano o riprova più tardi.")
                    else:
                        last_error = f"{m} ({resp.status_code}): {resp.text}"
                except Exception as ex:
                    if "Quota API Google esaurita" in str(ex):
                        raise ex
                    last_error = str(ex)

            raise Exception(f"Errore API Gemini: {last_error}")




async def _enrich_with_tmdb(recommendations_raw: List[Dict[str, Any]], user_movies_tmdb: set, user_watchlist_tmdb: set) -> List[Dict[str, Any]]:
    """
    Cerca i film consigliati dall'AI su TMDb API e crea oggetti rich card.
    """
    enriched = []
    tmdb_key = settings.TMDB_API_KEY

    async with httpx.AsyncClient(timeout=10.0) as client:
        for item in recommendations_raw[:4]:
            title = item.get("title")
            kind = item.get("kind", "movie")
            reason = item.get("reason", "")
            if not title:
                continue

            # Cerca su TMDb
            search_type = "tv" if kind == "tv" else "movie"
            params = {"api_key": tmdb_key, "query": title, "language": "it-IT"}
            r = await client.get(f"{TMDB_BASE}/search/{search_type}", params=params)

            card_data = {
                "title": title,
                "kind": kind,
                "reason": reason,
                "tmdb_id": None,
                "poster_path": None,
                "release_year": item.get("year", ""),
                "vote_average": None,
                "overview": "",
                "in_user_library": False,
                "in_user_watchlist": False
            }

            if r.status_code == 200:
                results = r.json().get("results", [])
                if results:
                    first = results[0]
                    tmdb_id = str(first.get("id"))
                    card_data["tmdb_id"] = tmdb_id
                    card_data["title"] = first.get("title") or first.get("name") or title
                    card_data["poster_path"] = first.get("poster_path")
                    date_str = first.get("release_date") or first.get("first_air_date") or ""
                    if date_str:
                        card_data["release_year"] = date_str[:4]
                    card_data["vote_average"] = first.get("vote_average")
                    card_data["overview"] = first.get("overview", "")

                    # Controlla presenza in libreria/watchlist utente
                    if tmdb_id in user_movies_tmdb:
                        card_data["in_user_library"] = True
                    if tmdb_id in user_watchlist_tmdb:
                        card_data["in_user_watchlist"] = True

            enriched.append(card_data)

    return enriched


@router.post("/chat")
async def ai_chat(
    payload: ChatRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Endpoint principale per interagire con il PopCorn Bot.
    """
    user_id = str(current_user["_id"])
    is_admin = bool(current_user.get("is_admin", False))
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # 1. Verifica se il bot è abilitato e Rate Limiting per utenti non-admin
    settings_doc = await db["system_settings"].find_one({"_id": "global"}) or {}
    ai_bot_enabled = settings_doc.get("ai_bot_enabled", True)
    if not ai_bot_enabled:
        raise HTTPException(
            status_code=400,
            detail="Il servizio PopCorn Bot è stato disattivato dall'amministratore."
        )

    daily_limit = settings_doc.get("ai_daily_limit_free", 1)

    usage_doc = await db["ai_usage"].find_one({"user_id": user_id, "date": today_str}) or {}
    today_count = usage_doc.get("count", 0)

    if not is_admin and today_count >= daily_limit:
        raise HTTPException(
            status_code=429,
            detail=f"Hai raggiunto il tuo limite giornaliero di {daily_limit} richiesta/e all'assistente PopCorn Bot. Riprova domani!"
        )

    # 2. Carica contesto utente dal DB (film già salvati / visti e watchlist)
    movies_cursor = db["movies"].find({"user_id": user_id}, {"title": 1, "tmdb_id": 1, "status": 1, "score": 1, "kind": 1})
    user_movies = await movies_cursor.to_list(length=1000)

    user_watchlist = current_user.get("watchlist", [])

    user_movies_tmdb = {str(m["tmdb_id"]) for m in user_movies if m.get("tmdb_id")}
    user_watchlist_tmdb = {str(w["id"]) for w in user_watchlist if w.get("id")}

    # Formatta lista per il prompt
    favorite_movies = [m["title"] for m in user_movies if m.get("score") and m.get("score") >= 7][:10]
    watched_titles = [m["title"] for m in user_movies][:15]
    watchlist_titles = [w.get("title", "") for w in user_watchlist if w.get("title")][:10]

    context_prompt = f"""
    Contesto dell'utente:
    - Username: {current_user.get('username', 'Utente')}
    - Alcuni film visti/salvati dall'utente: {', '.join(watched_titles) if watched_titles else 'Nessuno ancora'}
    - I suoi film preferiti (voto >= 7): {', '.join(favorite_movies) if favorite_movies else 'Nessuno ancora'}
    - Titoli attualmente in watchlist: {', '.join(watchlist_titles) if watchlist_titles else 'Nessuno ancora'}
    """

    # 3. Esegui la chiamata all'LLM
    api_key = settings_doc.get("ai_api_key") or settings.TMDB_API_KEY
    provider = settings_doc.get("ai_provider", "gemini")
    model_name = settings_doc.get("ai_model", "gemini-1.5-flash")

    try:
        raw_response = await _call_llm(payload.message, payload.chat_history, context_prompt, api_key, provider, model_name)
    except Exception as e:
        print("==== ERRORE CHIAMATA AI ====", e)
        raise HTTPException(status_code=500, detail=f"Impossibile comunicare con il servizio AI: {str(e)}")

    # 4. Estrai il blocco JSON delle raccomandazioni dalla risposta
    recommendations_raw = []
    json_match = re.search(r"```json\s*([\s\S]*?)\s*```", raw_response)
    clean_reply = raw_response

    if json_match:
        try:
            recommendations_raw = json.loads(json_match.group(1))
            # Rimuovi il blocco JSON dal testo mostrato all'utente per rendere il messaggio pulito
            clean_reply = re.sub(r"```json\s*[\s\S]*?\s*```", "", raw_response).strip()
        except Exception:
            pass

    # 5. Arricchisci i suggerimenti con TMDb
    enriched_recommendations = await _enrich_with_tmdb(recommendations_raw, user_movies_tmdb, user_watchlist_tmdb)

    # 6. Aggiorna conteggio utilizzi
    new_count = today_count + 1
    await db["ai_usage"].update_one(
        {"user_id": user_id, "date": today_str},
        {"$set": {"count": new_count, "last_request": datetime.utcnow()}},
        upsert=True
    )

    remaining = "illimitate" if is_admin else max(0, daily_limit - new_count)

    return {
        "reply": clean_reply,
        "recommendations": enriched_recommendations,
        "usage": {
            "is_admin": is_admin,
            "today_count": new_count,
            "daily_limit": daily_limit if not is_admin else "illimitato",
            "remaining": remaining
        }
    }
