import os, time, uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import boto3

router = APIRouter(prefix="/receipts", tags=["receipts"])

REGION = os.getenv("AWS_REGION", "ap-southeast-2")
BUCKET = os.getenv("RECEIPTS_BUCKET")
PREFIX = os.getenv("RECEIPTS_PREFIX", "receipts")

session = boto3.Session(profile_name=os.getenv("AWS_PROFILE")) if os.getenv("AWS_PROFILE") else boto3.Session()
s3 = session.client("s3", region_name=REGION)

class UploadReq(BaseModel):
    user_id: str
    filename: str
    content_type: str = "application/octet-stream"

class UploadResp(BaseModel):
    upload_url: str
    key: str

class DownloadReq(BaseModel):
    key: str

class DownloadResp(BaseModel):
    download_url: str

def _key_for(user_id: str, filename: str) -> str:
    ts = time.strftime("%Y/%m/%d")
    return f"{PREFIX}/{user_id}/{ts}/{uuid.uuid4()}-{filename}"

@router.post("/presign-upload", response_model=UploadResp)
def presign_upload(req: UploadReq):
    if not BUCKET:
        raise HTTPException(status_code=500, detail="Missing RECEIPTS_BUCKET")
    key = _key_for(req.user_id or "anon", req.filename)
    url = s3.generate_presigned_url(
        "put_object",
        Params={"Bucket": BUCKET, "Key": key, "ContentType": req.content_type},
        ExpiresIn=300
    )
    return {"upload_url": url, "key": key}

@router.post("/presign-download", response_model=DownloadResp)
def presign_download(req: DownloadReq):
    if not BUCKET:
        raise HTTPException(status_code=500, detail="Missing RECEIPTS_BUCKET")
    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET, "Key": req.key},
        ExpiresIn=300
    )
    return {"download_url": url}