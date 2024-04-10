from datetime import datetime, timedelta, UTC
from typing import Optional
from jose import JWTError, jwt
from db import get_collection
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "LBYZeHF9N0WQKEGuVJMXUfTmOqnDc83obI4wAh1l6iS7gtjC"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"expire": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def verify_user(username: str, password: str) -> str:
    user_collection = get_collection("user")
    user = await user_collection.find_one({"username": username}, projection={"username": 1, "password": 1})
    if not user:
        return ""
    if not verify_password(password, user['password']):
        return ""
    return user["username"]


async def update_token(username: str, token: str):
    user_collection = get_collection("user")
    await user_collection.update_one({"username": username}, {"$set": {"token": token}})


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user: str = payload.get("sub")
        if not user:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception

