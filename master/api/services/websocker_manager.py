from typing import List
from fastapi import WebSocket
import loguru

logger = loguru.logger

class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = list()
        self._round_rubin_count = 0

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
    
    async def send_round_robin_message(self, message: str):
        attempts = len(self.active_connections)  # Limit attempts to the number of connections
        while attempts > 0:
            if not self.active_connections:  # Check if there are any connections left
                logger.error("No WebSocket connection available.")
                break
            ws = self.active_connections[self._round_robin_count]
            try:
                await ws.send_text(message)
                logger.info(f"Message successfully sent to WebSocket at index {self._round_robin_count}.")
                self._round_robin_count = (self._round_robin_count + 1) % len(self.active_connections)
                break  # Break the loop on successful send
            except Exception as e:
                logger.error(f"Error sending round-robin message: {e}")
                self.disconnect(ws)  # Disconnect the failing WebSocket
                # No increment needed here because we want to try the next WebSocket immediately
            attempts -= 1  # Decrement the number of attempts left


manager = WebSocketManager()

async def get_websocket_manager():
    return manager