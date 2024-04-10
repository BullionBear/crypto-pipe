import time
import string
import random
from datetime import datetime, UTC
from app.models.task import Task
import pandas as pd
import functools
from threading import Lock


class TaskManager:
    def __init__(self):
        self.tasks = pd.DataFrame(columns=list(Task.model_fields))
        self.lock = Lock()
        self._task_id = 1

    def atomic(self, f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            with self.lock:
                return f(*args, **kwargs)

        return wrapped

    @atomic
    def create_task(self, task_name: str, depends_on: list[str], **kwargs):
        trigger_dt = datetime.now(UTC)
        task_id = f"{task_name}-{trigger_dt.isoformat()}-{self._task_id}"
        t = Task(task_id=task_id, task_name=task_name, args=kwargs, start_time=time.time(), end_time=-1, depends_on=depends_on, status="Pending")
        self.tasks.loc[t.task_id] = dict(t)












def task(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        trigger_dt = datetime.now(UTC)
        random_string = ''.join(random.sample(string.ascii_letters + string.digits, 6))
        task_name = f"{func.__name__}-{trigger_dt.isoformat()}-{random_string}"
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        return result

    return wrapper


def async_task(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):

        start_time = time.time()
        result = await func(*args, **kwargs)

        end_time = time.time()
        elapsed_time = end_time - start_time
        return result

    return wrapper