from typing import List, Any, Dict
from pydantic import BaseModel


class MasterConnectionRequest(BaseModel):
    ip: str
    port: int

class CreateTaskRequest(BaseModel):
    task: str
    args: List[Any] = []
    kwargs: Dict[str, Any] = dict()
