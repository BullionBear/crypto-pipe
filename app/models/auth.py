from typing import Optional
from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class User(BaseModel):
    username: str
    password: str
    token: Optional[str] = None
    token_expire: Optional[int] = None

