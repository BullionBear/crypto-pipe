from typing import List, Dict, Any
from pydantic import BaseModel


class Task(BaseModel):
    task_id: str
    task_name: str
    args: Dict[str, Any]
    start_time: int
    end_time: int
    status: str
    depend_on: List[str]
    log: str



