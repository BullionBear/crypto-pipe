import websockets
import loguru
import uuid
import pipe.command as cmd
from api.core.config import Settings


logger = loguru.logger


class WebSocketClient:
    def __init__(self, uri):
        self.uri = uri

    async def connect(self):
        async with websockets.connect(self.uri) as websocket:
            await self.on_open(websocket)
            await self.receive_messages(websocket)

    async def receive_messages(self, websocket: websockets.WebSocketClientProtocol):
        try:
            while True:
                message = await websocket.recv()
                await self.on_message(message, websocket)
        except websockets.ConnectionClosed:
            await self.on_close()
        except Exception as e:
            await self.on_error(e)

    async def on_message(self, message_str: str, websocket: websockets.WebSocketClientProtocol):
        logger.info(f"Received message: {message_str}")
        message = cmd.Message.model_validate_json(message_str)
        command = message.cmd
        logger.info(f"Receive {command} with {message.id}")
        if command == cmd.MASTER_CONNECTION_ESTABLISHED_ACK:
            await self.on_ack(message)
        elif command == cmd.MASTER_CREATE_TASK:
            await self.on_create_task(message, websocket)
    
    async def on_ack(self, message: cmd.Message):
        pass

    async def on_create_task(self, message: cmd.Message, websocket: websockets.WebSocketClientProtocol):
        response = cmd.Message(cmd=cmd.WORKER_CREATE_TASK_ACK, id=message.id)
        await websocket.send(response.model_dump_json())
        data = message.data
        task_name = data["task"]
        args = data["args"]
        kwargs = data["kwargs"]
        logger.info(f"Start running {task_name}({args}, {kwargs})")
        reply = cmd.Message(cmd=cmd.WORKER_TASK_DONE, id=uuid.uuid4().hex)
        await websocket.send(reply.model_dump_json())

    async def on_error(self, error):
        logger.info(f"Encountered error: {error}")

    async def on_close(self):
        logger.info("Connection closed")

    async def on_open(self, websocket):
        message = cmd.Message(cmd=cmd.WORKER_CONNECTION_ESTABLISH, id=uuid.uuid4().hex, data={
            "name": Settings().worker_name
        })
        logger.info("Connection opened")
        await websocket.send(message.model_dump_json())
