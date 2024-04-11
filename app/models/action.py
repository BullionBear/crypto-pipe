from typing import List, Dict, Any
from pydantic import BaseModel




class Action(BaseModel):
    task_id: str
    task_name: str
    start_time: int
    end_time: int
    status: str
    depend_on: List[str]
    log: str



