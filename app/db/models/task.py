from typing import Dict, Optional, Any
from pydantic import BaseModel


class Task(BaseModel):
    task_id: str
    job_id: str
    task_name: str
    created_by: str
    created_at: int
    args: Optional[Dict[str, Any]]
    start_time: int
    end_time: int
    status: str
    worker: str
    logging: str
