from fastapi import FastAPI
from db import create_start_app_handler, create_stop_app_handler
from app.api.routers import auth_router


app = FastAPI()

app.add_event_handler("startup", create_start_app_handler(app))
app.add_event_handler("shutdown", create_stop_app_handler(app))

app.include_router(auth_router, prefix="/auth")


@app.get("/")
async def root():
    return {"message": "Hello World"}



# Placeholders for future expansion
# TODO: Add database integration
# TODO: Add user management
# TODO: Add task scheduling endpoints

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

