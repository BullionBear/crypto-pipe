from fastapi import APIRouter, Request, HTTPException, Depends
from .schema import MasterConnectionRequest, CreateTaskRequest
import loguru
import httpx
import uuid
from api.services import get_websocket_manager, WebSocketManager
import pipe.command as cmd

logger = loguru.logger
router = APIRouter()

@router.post("/connect", tags=["deployment"])
async def connect_to(request: Request, conn_request: MasterConnectionRequest):
    worker_ip = conn_request.ip
    worker_port = conn_request.port
    url = f"http://{worker_ip}:{worker_port}/accept"

    data = {
        "ip": request.url.hostname,
        "port": request.url.port
    }
    logger.info(f"Send Master info {data} to {url}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
            response.raise_for_status()

            return {"status": "success", "data": response.json()}
    except httpx.RequestError as exc:
        logger.error(f"An error occurred while requesting {exc.request.url!r}.")
        raise HTTPException(status_code=400, detail=f"Request to {worker_ip}:{worker_port} failed.")
    except httpx.HTTPStatusError as exc:
        logger.error(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
        raise HTTPException(status_code=exc.response.status_code, detail="Error from worker.")


@router.post("/create", tags=["deployment"])
async def create_task(request: CreateTaskRequest, manager: WebSocketManager = Depends(get_websocket_manager)):
    logger.info(f"{request=}")
    data = request.model_dump()
    msg = cmd.Message(cmd=cmd.MASTER_CREATE_TASK, id=uuid.uuid4().hex, data=data)
    await manager.active_connections["worker"].send_text(msg.model_dump_json())
    return {}

@router.get("/workers", tags=["worker"])
async def get_workers(manager: WebSocketManager = Depends(get_websocket_manager)):
    return {
        "n_connections": len(manager.active_connections)
    }
