from starlette.websockets import WebSocketDisconnect
from api.services import get_websocket_manager, WebSocketManager
from fastapi import WebSocket, APIRouter, Depends
import loguru

logger = loguru.logger
router = APIRouter()


@router.websocket("")
async def websocket_endpoint(websocket: WebSocket, manager: WebSocketManager = Depends(get_websocket_manager)):
    await websocket.accept()
    manager.active_connections["worker"] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    finally:
        del manager.active_connections["worker"]


@router.get("/broadcast")
async def broadcast_message(message: str, manager: WebSocketManager = Depends(get_websocket_manager)):
    # await manager.broadcast(message)
    return {"message": "Message sent to all clients", "content": message}
