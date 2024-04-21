from typing import Set
from api.services import get_websocket_manager, WebSocketManager
from fastapi import WebSocket, APIRouter, Depends

router = APIRouter()


@router.websocket("")
async def websocket_endpoint(websocket: WebSocket, manager: WebSocketManager = Depends(get_websocket_manager)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo the received message back to the client
            await manager.send_personal_message(f"Message received: {data}", websocket)
    except Exception as e:
        print('Error:', e)
    finally:
        manager.disconnect(websocket)

@router.get("/broadcast")
async def broadcast_message(message: str, manager: WebSocketManager = Depends(get_websocket_manager)):
    await manager.broadcast(message)
    return {"message": "Message sent to all clients", "content": message}
