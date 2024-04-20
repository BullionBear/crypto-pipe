import asyncio
import websockets


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
                await self.on_message(message)
        except websockets.ConnectionClosed:
            await self.on_close()
        except Exception as e:
            await self.on_error(e)

    async def on_message(self, message):
        print(f"Received message: {message}")

    async def on_error(self, error):
        print(f"Encountered error: {error}")

    async def on_close(self):
        print("Connection closed")

    async def on_open(self, websocket):
        print("Connection opened")
        await websocket.send("Hello, Server!")

# Function to run the WebSocket client
async def run_client():
    client = WebSocketClient("ws://127.0.0.1:9988/ws")
    await client.connect()

# Start the event loop and run the client
if __name__ == "__main__":
    asyncio.run(run_client())