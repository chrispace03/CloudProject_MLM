import os, time, uuid, json
import boto3

REGION  = os.getenv("AWS_REGION", "ap-southeast-2")
BUCKET  = os.environ["RECEIPTS_BUCKET"]
PREFIX  = os.getenv("RECEIPTS_PREFIX", "receipts")

user_id  = "n11099496"
filename = "test.txt"
key = f"{PREFIX}/{user_id}/{time.strftime('%Y/%m/%d')}/{uuid.uuid4()}-{filename}"

s3 = boto3.client("s3", region_name=REGION)

put_url = s3.generate_presigned_url(
    "put_object",
    Params={"Bucket": BUCKET, "Key": key, "ContentType": "text/plain"},
    ExpiresIn=300
)
get_url = s3.generate_presigned_url(
    "get_object",
    Params={"Bucket": BUCKET, "Key": key},
    ExpiresIn=300
)

print(json.dumps({"key": key, "put_url": put_url, "get_url": get_url}, indent=2))
