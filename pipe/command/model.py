from typing import Dict, Any
from pydantic import BaseModel

class Message(BaseModel):
    cmd: str
    id: str
    data: Dict[str, Any]