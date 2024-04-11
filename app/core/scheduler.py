import time

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import HTTPException
from apscheduler.jobstores.mongodb import MongoDBJobStore
from app.db.db import MONGO_URL, DATABASE, get_collection
from app.db.models import Job
from jobs import JOB_REGISTRY

AP_COLLECTION = 'apscheduler'
JOB_COLLECTION = 'job'


async def verify_job_name(job_name: str):
    job = JOB_REGISTRY.get(job_name)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


# Create an instance of MongoDBJobStore
jobstore = MongoDBJobStore(database=DATABASE, collection=AP_COLLECTION, host=MONGO_URL)
scheduler = BackgroundScheduler(jobstores={'default': jobstore})
scheduler.start()


async def create_cron_job(user: str, cron_expression: str, job_name: str, **kwargs):
    job = JOB_REGISTRY.get(job_name)
    cron = cron_expression_to_dict(cron_expression)
    schedule = scheduler.add_job(job, 'cron', **cron, kwargs=kwargs)
    data = Job(
        job_name=job_name,
        created_by=user,
        created_at=int(time.time()),
        job_id=schedule.id,
        cron=cron_expression,
        args=kwargs
    )

    get_collection(JOB_COLLECTION).insert_one(
        data.dict(by_alias=True)
    )
    return schedule.id


def cron_expression_to_dict(cron_expression):
    """
    Convert a cron expression into a dictionary with keys for minute, hour,
    day of the month, month, and day of the week.

    Args:
        cron_expression (str): A cron expression string, e.g., "*/15 * * * *"

    Returns:
        dict: A dictionary with the parts of the cron expression.
    """
    parts = cron_expression.split()
    if len(parts) != 5:
        raise ValueError("Invalid cron expression. A cron expression must have exactly 5 parts.")

    cron_dict = {
        "minute": parts[0],
        "hour": parts[1],
        "day": parts[2],
        "month": parts[3],
        "day_of_week": parts[4],
    }

    return cron_dict


async def list_crons(user: str):
    job_collection = get_collection(JOB_COLLECTION)
    # Initialize an empty list to hold your documents
    ids = []
    # Async for loop to iterate over the cursor
    async for document in job_collection.find({"created_by": user}):
        ids.append(document["_id"])  # Or process the document as needed
    return ids


async def get_cron_by_id(user: str, job_id: str):
    job_collection = get_collection(JOB_COLLECTION)
    job = await job_collection.find_one({"_id": job_id})
    if job is None or job["created_by"] != user:
        raise HTTPException(status_code=404, detail="Job id not found")
    return job


async def delete_cron_by_id(job_id: str):
    """
    Delete cron by id should verify the id existence and job owner before deleting
    """
    job_collection = get_collection(JOB_COLLECTION)
    await job_collection.delete_one({"_id": job_id})
    scheduler.remove_job(job_id)
    return

