from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/protected-endpoint")
async def read_protected_data(current_user: User = Depends(get_current_user)):
    # Endpoint logic here. The code below this line will only execute if the token is valid.
    return {"data": "This is protected data"}