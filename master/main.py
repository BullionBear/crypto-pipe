from fastapi import FastAPI
from api.routers import deployment_router
from api.routers import websocket_router


app = FastAPI()
app.include_router(websocket_router, prefix='/ws')
app.include_router(deployment_router, prefix='/deployment')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=9988, reload=True)
