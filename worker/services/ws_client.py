from typing import Dict, Any
import asyncio
import websockets
import loguru
import uuid
import pipe.command as cmd, Message


logger = loguru.logger


class WebSocketClient:
    def __init__(self, uri):
        self.uri = uri

    async def connect(self):
        async with websockets.connect(self.uri) as websocket:
            await self.on_open(websocket)
            await self.receive_messages(websocket)

    async def receive_messages(self, websocket):
        try:
            while True:
                message = await websocket.recv()
                await self.on_message(message, websocket)
        except websockets.ConnectionClosed:
            await self.on_close()
        except Exception as e:
            await self.on_error(e)

    async def on_message(self, message_str, websocket):
        logger.info(f"Received message: {message_str}")
        message = cmd.resolve_command(message_str)
        command = message.cmd
        logger.info(f"Receive {command} with {message.id}")
        if command == cmd.MASTER_CONNECTION_ESTABLISHED_ACK:
            await self.on_ack(message)
        elif command == cmd.MASTER_CREATE_TASK:
            await self.on_create_task(message, websocket)
    
    async def on_ack(self, message: Message):
        pass
        
    
    async def on_create_task(self, message: Dict[str, Any], websocket):
        response = cmd.make_command(cmd.WORKER_CREATE_TASK_ACK, message["id"], dict())
        await websocket.send(response)
        task_name = message["task"]
        args = message["args"]
        kwargs = message["kwargs"]
        logger.info(f"Start running {task_name}({args}, {kwargs})")
        reply = cmd.make_command(cmd.WORKER_TASK_DONE, uuid.uuid4().hex, dict())
        await websocket.send(reply)

    async def on_error(self, error):
        logger.info(f"Encountered error: {error}")

    async def on_close(self):
        logger.info("Connection closed")

    async def on_open(self, websocket):
        message = cmd.make_command(cmd.WORKER_CONNECTION_ESTABLISH, uuid.uuid4().hex, dict())
        logger.info("Connection opened")
        await websocket.send(message)

# Function to run the WebSocket client
async def run_client():
    client = WebSocketClient("ws://127.0.0.1:9988/ws")
    await client.connect()

# Start the event loop and run the client
if __name__ == "__main__":
    asyncio.run(run_client())