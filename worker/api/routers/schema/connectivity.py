from pydantic import BaseModel


class WorkerConnectRequest(BaseModel):
    ip: str
    port: int

