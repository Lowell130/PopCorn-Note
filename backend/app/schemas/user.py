#app/schemas/user.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str

class UserOut(BaseModel):
    id: str
    email: EmailStr
    username: str
    watchlist: list[dict] = []
    is_admin: bool = False
