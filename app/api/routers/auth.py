from fastapi import APIRouter, Depends, HTTPException, status
import app.core.auth as auth
from app.api.schemas.auth import LoginRequest

router = APIRouter()


@router.post("/login", tags=["auth"])
async def login_for_access_token(login_request: LoginRequest):
    user = await auth.verify_user(login_request.username, login_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(
        data={"sub": user}
    )
    await auth.update_token(user, access_token)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/create_user", tags=["auth"])
async def create_user(login_request: LoginRequest):
    await auth.create_user(login_request.username, login_request.password)
    return {"msg": "success"}


@router.get("/me", tags=["auth"])
async def get_username(current_user: str = Depends(auth.get_current_user)):
    return {"user": current_user}
