# app/models/activity.py
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

class Activity(BaseModel):
    id: Optional[str] = None
    user_id: str
    username: str
    type: Literal["post", "add_movie", "rate_movie"]
    content: Optional[str] = None
    
    # Snapshot del film (per non fare join pesanti)
    movie_title: Optional[str] = None
    movie_id: Optional[str] = None
    movie_poster: Optional[str] = None
    movie_score: Optional[float] = None
    
    # Reactions: lista di {user_id, type, created_at}
    reactions: list = Field(default_factory=list)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
