import os, uuid
from fastapi import APIRouter, UploadFile, File, Depends
from api.security import get_current_user
from common.config import UPLOADS_DIR

router = APIRouter(tags=["uploads"])

@router.post("/receipts")
def upload_receipt(file: UploadFile = File(...), user=Depends(get_current_user)):
    user_dir = os.path.join(UPLOADS_DIR, "receipts", user["user_id"])
    os.makedirs(user_dir, exist_ok=True)
    suffix = file.filename.rsplit("/", 1)[-1].replace("/", "_")
    name = f"{uuid.uuid4()}_{suffix}"
    dest_path = os.path.join(user_dir, name)
    with open(dest_path, "wb") as f:
        f.write(file.file.read())
    return {"stored_as": os.path.relpath(dest_path)}
