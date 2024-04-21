from starlette.websockets import WebSocketDisconnect
from api.services import get_websocket_manager, WebSocketManager
from fastapi import WebSocket, APIRouter, Depends
import pipe.command as cmd
import loguru

logger = loguru.logger
router = APIRouter()


@router.websocket("")
async def websocket_endpoint(websocket: WebSocket, manager: WebSocketManager = Depends(get_websocket_manager)):
    try:
        while True:
            message_str = await websocket.receive_text()
            message = cmd.resolve_command(message_str)
            command = message["cmd"]
            logger.info(f"Receive {command} with {message["id"]}")
            if command == cmd.WORKER_CONNECTION_ESTABLISH:
                await on_connection_establish(message, websocket, manager)
            elif command == cmd.WORKER_CREATE_TASK_ACK:
                await on_ack(message, websocket)
            elif command == cmd.WORKER_TASK_DONE:
                await on_task_done(message, websocket)
        
    except WebSocketDisconnect:
        logger.warning("WebSocket disconnected")
    finally:
        del manager.active_connections["worker"]

async def on_connection_establish(message, websocket, websocket_manager):
    server_name = message["name"]
    websocket_manager.add_connection(server_name, websocket)

    response = cmd.make_command(cmd.MASTER_CONNECTION_ESTABLISHED_ACK, message["id"], dict())
    await websocket.send_text(response)

async def on_ack(message, websocket):
    pass

async def on_task_done(message, websocket):
    response = cmd.make_command(cmd.MASTER_TASK_DONE_ACK, message["id"], dict())
    await websocket.send_text(response)



@router.get("/broadcast")
async def broadcast_message(message: str, manager: WebSocketManager = Depends(get_websocket_manager)):
    # await manager.broadcast(message)
    return {"message": "Message sent to all clients", "content": message}
