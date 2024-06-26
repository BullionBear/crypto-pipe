from typing import Dict
from fastapi import WebSocket
import loguru

logger = loguru.logger


class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = dict()

    async def add_connection(self, name: str, websocket: WebSocket):
        self.active_connections[name] = websocket

    async def disconnect(self, name):
        if name in self.active_connections:
            websocket = self.active_connections[name]
            await websocket.close()  # Properly close the connection
            del self.active_connections[name]  # Then remove it from the dictionary
            logger.info(f"Disconnected and removed connection: {name}")

    # async def send_personal_message(self, name: str, message: str):
    #     websocket = self.active_connections[name]
    #     await websocket.send_text(message)

    # async def broadcast(self, message: str):
    #     for connection in self.active_connections:
    #         await connection.send_text(message)
    # 
    # async def send_message(self, message: str):
    #     name = list(self.active_connections.keys())[0]
    #     await self.send_personal_message(name, message)

    # def all_workers(self):
    #     return list(self.active_connections.keys())


manager = WebSocketManager()

async def get_websocket_manager():
    return manager