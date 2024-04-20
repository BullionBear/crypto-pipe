from fastapi import WebSocket, APIRouter

router = APIRouter()


@router.websocket("")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except Exception as e:
        print('Error:', e)
    finally:
        await websocket.close()