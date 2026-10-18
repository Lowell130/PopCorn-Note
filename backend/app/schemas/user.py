#app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., max_length=100)
    password: str = Field(..., max_length=256)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=256)

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

class ChangePassword(BaseModel):
    current_password: str = Field(..., max_length=256)
    new_password: str = Field(..., max_length=256)
