from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from common.config import JWT_SECRET, JWT_ALGORITHM

security = HTTPBearer(auto_error=True)

# Hard-coded users for A01 (anti-criteria compliant)
USERS = {
    "alice": {"user_id": "u1", "password": "alice123", "role": "admin"},
    "bob":   {"user_id": "u2", "password": "bob123",   "role": "user"},
}

def create_access_token(sub: str, role: str, uid: str) -> str:
    from datetime import datetime, timedelta, timezone
    payload = {
        "sub": sub,
        "role": role,
        "uid": uid,
        "iat": int(datetime.now(timezone.utc).timestamp()),
        "exp": int((datetime.now(timezone.utc) + timedelta(hours=2)).timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(security)):
    token = creds.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"username": payload.get("sub"), "role": payload.get("role"), "user_id": payload.get("uid")}
