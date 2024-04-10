from fastapi import APIRouter, Depends, HTTPException, status
from app.core.auth import verify_user, create_access_token, update_token, get_current_user
from app.models.auth import LoginRequest

router = APIRouter()


@router.post("/login")
async def login_for_access_token(login_request: LoginRequest):
    user = await verify_user(login_request.username, login_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user}
    )
    await update_token(user, access_token)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def get_username(current_user: str = Depends(get_current_user)):
    return {"user": current_user}
