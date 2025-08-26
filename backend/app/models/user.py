#app/models/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    username: str
    hashed_password: str
