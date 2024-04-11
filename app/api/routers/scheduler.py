from typing import Callable
from fastapi import APIRouter, Depends, HTTPException
from app.core.auth import get_current_user
from app.api.schemas.scheduler import CronRequest
from app.core.scheduler import verify_job_name, create_cron_job
from jobs import JOB_REGISTRY

router = APIRouter()


@router.get("/jobs")
async def list_jobs():
    return {"jobs": list(JOB_REGISTRY)}


@router.get("/job/{job_name}")
async def list_job_detail(job: Callable = Depends(verify_job_name)):
    return {'doc': job.__doc__}


@router.post("/cron/{job_name}")
async def create_execution(cron_request: CronRequest, job: Callable = Depends(verify_job_name), current_user: str = Depends(get_current_user)):
    job_keys = set(job.__annotations__.keys())
    arg_keys = set(cron_request.args.keys())
    if not job_keys.issubset(arg_keys):
        missing_keys = job_keys - arg_keys
        raise HTTPException(status_code=400, detail=f"Missing Key {list(missing_keys)}")
    args = {key: cron_request.args[key] for key in job_keys}
    await create_cron_job(cron_request.cron, job.__name__, **args)
    return {"msg": "Success"}


@router.get("/crons")
async def list_crons():
    pass


