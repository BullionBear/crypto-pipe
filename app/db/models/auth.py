from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    token: Optional[str] = None

