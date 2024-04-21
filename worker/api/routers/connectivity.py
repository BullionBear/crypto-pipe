import asyncio
from fastapi import APIRouter, HTTPException
from .schema import WorkerConnectRequest
from services import WebSocketClient
import loguru

logger = loguru.logger
router = APIRouter()


@router.post("/conn", tags=["connectivity"])
async def connect(request: WorkerConnectRequest):
    # Building the URI based on the input
    protocol = "ws"
    uri = f"{protocol}://{request.ip}:{request.port}/ws"
    logger.info(f"Connection to {uri=}")
    ws = WebSocketClient(uri)
    asyncio.create_task(ws.connect())
    return {"msg": "Connection Established"}

