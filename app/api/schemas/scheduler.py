from typing import Dict, Any
from pydantic import BaseModel, field_validator
from croniter import croniter
from datetime import datetime


class CronRequest(BaseModel):
    args: Dict[str, Any]
    cron: str

    @field_validator('cron')
    @classmethod
    def validate_cron_expression(cls, v):
        base_time = datetime.now()
        try:
            croniter(v, base_time)
        except ValueError:
            raise ValueError("Invalid cron expression")

        return v