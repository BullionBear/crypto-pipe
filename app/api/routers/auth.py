from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from app.api.dependencies.token import create_access_token, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.auth import LoginRequest

router = APIRouter()



@router.post("/login")
async def login_for_access_token(login_request: LoginRequest):
    user = authenticate_user(fake_users_db, login_request.username, login_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
