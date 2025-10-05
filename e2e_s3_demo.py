import os, time, uuid, json, requests, boto3

REGION  = os.getenv("AWS_REGION", "ap-southeast-2")
BUCKET  = os.getenv("RECEIPTS_BUCKET")
PREFIX  = os.getenv("RECEIPTS_PREFIX", "receipts")

user_id  = "n11099496"
filename = "test.txt"
key = f"{PREFIX}/{user_id}/{time.strftime('%Y/%m/%d')}/{uuid.uuid4()}-{filename}"

session = boto3.Session(profile_name=os.getenv("AWS_PROFILE")) if os.getenv("AWS_PROFILE") else boto3.Session()
s3 = session.client("s3", region_name=REGION)

put_url = s3.generate_presigned_url(
    "put_object",
    Params={"Bucket": BUCKET, "Key": key, "ContentType": "text/plain"},
    ExpiresIn=1200  # 20 minutes
)
get_url = s3.generate_presigned_url(
    "get_object",
    Params={"Bucket": BUCKET, "Key": key},
    ExpiresIn=1200
)

data = b"Hello via E2E presigned PUT"
r_put = requests.put(put_url, data=data, headers={"Content-Type":"text/plain"})
r_get = requests.get(get_url)

print(json.dumps({
  "key": key,
  "put_status": r_put.status_code,
  "get_status": r_get.status_code,
  "get_body_preview": r_get.text[:80]
}, indent=2))
