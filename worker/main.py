from fastapi import FastAPI
from api.routers import connectivity_router

app = FastAPI()
app.include_router(connectivity_router, prefix='')


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=55432, reload=True)


