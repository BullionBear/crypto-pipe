from fastapi import APIRouter, Request, HTTPException, Depends
from .schema import MasterConnectionRequest, CreateTaskRequest
import loguru
import httpx
from api.services import get_websocket_manager, WebSocketManager
import pipe.command as command

logger = loguru.logger
router = APIRouter()

@router.post("/connect", tags=["worker"])
async def connect_to(request: Request, conn_request: MasterConnectionRequest):
    worker_ip = conn_request.ip
    worker_port = conn_request.port
    url = f"http://{worker_ip}:{worker_port}/conn"

    data = {
        "ip": request.url.hostname,
        "port": request.url.port
    }
    logger.info(f"Send Master info {data} to {url}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"http://{worker_ip}:{worker_port}/conn", json=data)
            response.raise_for_status()

            return {"status": "success", "data": response.json()}
    except httpx.RequestError as exc:
        logger.error(f"An error occurred while requesting {exc.request.url!r}.")
        raise HTTPException(status_code=400, detail=f"Request to {worker_ip}:{worker_port} failed.")
    except httpx.HTTPStatusError as exc:
        logger.error(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
        raise HTTPException(status_code=exc.response.status_code, detail="Error from worker.")


@router.post("/create_task", tags=["worker"])
async def create_task(request: CreateTaskRequest, manager: WebSocketManager = Depends(get_websocket_manager)):
    logger.info(f"{request=}")
    data = request.dict()
    msg = command.make_command(command.MASTER_CREATE_TASK, data)
    await manager.active_connections["worker"].send_text(msg)
    return {}

@router.get("/workers", tags=["worker"])
async def get_workers(manager: WebSocketManager = Depends(get_websocket_manager)):
    return {
        "n_connections": len(manager.active_connections)
    }
