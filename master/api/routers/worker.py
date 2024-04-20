from fastapi import APIRouter, Request, HTTPException
from .schema import MasterConnectionRequest
import loguru
import httpx

logger = loguru.logger
router = APIRouter()

@router.post("/connect", tags=["conn"])
async def connect_to(request: Request, conn_request: MasterConnectionRequest):
    worker_ip = conn_request.ip
    worker_port = conn_request.port
    logger.info(f"Send request to http://{worker_ip}:{worker_port}/conn")
    data = {
        "ip": request.url.hostname,
        "port": request.url.port
    }
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
