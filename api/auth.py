from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from api.security import create_access_token, USERS

router = APIRouter()

class LoginIn(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(body: LoginIn):
    user = USERS.get(body.username)
    if not user or user["password"] != body.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(sub=body.username, role=user["role"], uid=user["user_id"])
    return {"access_token": token, "token_type": "bearer"}
