# app/schemas/movie.py
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal, List
from datetime import datetime
import re

Status = Literal["watched", "to_watch", "upcoming", "watching"]
Liked = Literal["loved", "liked", "okay", "disliked", "terrible"]
Kind = Literal["movie", "tv"]

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

class MovieCreate(BaseModel):
    # 👇 nuovo: tipo dell’item
    kind: Kind = "movie"
    title: str
    status: Status = "to_watch"
    score: Optional[int] = Field(default=None, ge=1, le=10)
    liked: Optional[Liked] = None
    note: Optional[str] = None

    # campi informativi (riusati anche per le serie: mappiamo first_air_date -> release_date/year)
    release_year: Optional[int] = Field(default=None, ge=1888, le=2100)
    release_date: Optional[str] = None  # "YYYY-MM-DD"
    poster_url: Optional[str] = None
    director: Optional[str] = None
    cast: Optional[List[str]] = None
    runtime: Optional[int] = Field(default=None, ge=1, le=600)
    tmdb_id: Optional[int] = Field(default=None, ge=1)
    overview: Optional[str] = None

    @field_validator("release_date")
    @classmethod
    def validate_date(cls, v):
        if v is None:
            return v
        if not DATE_RE.match(v):
            raise ValueError('release_date deve essere "YYYY-MM-DD"')
        return v


class MovieUpdate(BaseModel):
    kind: Optional[Kind] = None

    status: Optional[Status] = None
    score: Optional[int] = Field(default=None, ge=1, le=10)
    liked: Optional[Liked] = None
    note: Optional[str] = None

    release_year: Optional[int] = Field(default=None, ge=1888, le=2100)
    release_date: Optional[str] = None
    poster_url: Optional[str] = None
    director: Optional[str] = None
    cast: Optional[List[str]] = None
    runtime: Optional[int] = Field(default=None, ge=1, le=600)
    tmdb_id: Optional[int] = Field(default=None, ge=1)
    overview: Optional[str] = None

    @field_validator("release_date")
    @classmethod
    def validate_date(cls, v):
        if v is None:
            return v
        if not DATE_RE.match(v):
            raise ValueError('release_date deve essere "YYYY-MM-DD"')
        return v


class MovieResponse(MovieCreate):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
