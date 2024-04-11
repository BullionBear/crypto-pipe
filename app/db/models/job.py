from typing import Dict, Any
from pydantic import BaseModel, Field


class Job(BaseModel):
    job_name: str
    created_by: str
    created_at: int
    job_id: str = Field(..., alias='_id')
    cron: str
    args: Dict[str, Any]

    class Config:
        populate_by_name = True
