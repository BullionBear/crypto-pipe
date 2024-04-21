from fastapi import APIRouter, HTTPException
from .schema import WorkerConnectRequest
from services import WebSocketClient

router = APIRouter()


@router.post("/conn", tags=["connectivity"])
async def connect(request: WorkerConnectRequest):
    # Building the URI based on the input
    protocol = "wss" if request.tls else "ws"
    uri = f"{protocol}://{request.ip}:{request.port}"
    ws = WebSocketClient()
    return {"uri": uri}
    # try:
    #     # Handling TLS if needed
    #     ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT) if request.tls else None
    #     if ssl_context:
    #         ssl_context.check_hostname = False
    #         ssl_context.verify_mode = ssl.CERT_NONE
#
    #     # Connecting to the WebSocket server
    #     async with websockets.connect(uri, ssl=ssl_context) as websocket:
    #         # Here you can interact with the websocket
    #         await websocket.send("Hello server!")
    #         response = await websocket.recv()
    #         return {"message": "Connected successfully!", "response": response}
    # except Exception as e:
    #     raise HTTPException(status_code=400, detail=str(e))

