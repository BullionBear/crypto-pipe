from typing import Callable
from fastapi import APIRouter, Depends, HTTPException
from app.core.auth import get_current_user
from app.api.schemas.scheduler import CronRequest
import app.core.scheduler as sc
from registry.jobs import JOB_REGISTRY

router = APIRouter()


@router.get("/jobs", tags=["scheduler"])
async def list_jobs():
    return {"jobs": list(JOB_REGISTRY)}


@router.get("/job/{job_name}", tags=["scheduler"])
async def list_job_detail(job: Callable = Depends(sc.verify_job_name)):
    return {'doc': job.__doc__}


@router.post("/cron/{job_name}", tags=["scheduler"])
async def create_cron(cron_request: CronRequest, job: Callable = Depends(sc.verify_job_name), current_user: str = Depends(get_current_user)):
    job_keys = set(job.__annotations__.keys())
    arg_keys = set(cron_request.args.keys())
    if not job_keys.issubset(arg_keys):
        missing_keys = job_keys - arg_keys
        raise HTTPException(status_code=400, detail=f"Missing Key {list(missing_keys)}")
    args = {key: cron_request.args[key] for key in job_keys}
    job_id = await sc.create_cron_job(current_user, cron_request.cron, job.__name__, **args)
    return {"job_id": job_id}


@router.get("/crons", tags=["scheduler", "cron"])
async def list_crons(current_user: str = Depends(get_current_user)):
    job_id = await sc.list_crons(current_user)
    return job_id


@router.get("/cron/{job_id}", tags=["scheduler", "cron"])
async def list_cron_detail(job_id: str, current_user: str = Depends(get_current_user)):
    job = await sc.get_cron_by_id(current_user, job_id)
    return job


@router.delete("/cron/{job_id}",  tags=["scheduler", "cron"])
async def delete_cron(job_id: str, current_user: str = Depends(get_current_user)):
    job = await sc.get_cron_by_id(current_user, job_id)
    if job:
        await sc.delete_cron_by_id(job_id)
    return {}


