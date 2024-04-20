from pydantic import BaseModel


class MasterConnectionRequest(BaseModel):
    ip: str
    port: int
