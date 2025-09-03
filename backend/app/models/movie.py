#app/models/movie.py
from pydantic import BaseModel
from typing import Optional, Literal

class Movie(BaseModel):
    id: Optional[str] = None
    title: str
    status: Literal["watched", "to_watch", "upcoming", "watching"] = "to_watch"
    score: Optional[int] = None
    liked: Optional[Literal["loved", "liked", "okay", "disliked", "terrible"]] = None
    note: Optional[str] = None
    user_id: str
