import os, json
import boto3
from botocore.exceptions import ClientError

REGION = os.getenv("AWS_REGION", "ap-southeast-2")
_session = boto3.Session(region_name=REGION)

def get_param(name: str, default: str | None = None) -> str | None:
    try:
        ssm = _session.client("ssm")
        r = ssm.get_parameter(Name=name, WithDecryption=False)
        return r["Parameter"]["Value"]
    except ClientError as e:
        # Fallback to env var (convert name to ENV style), then to default
        env_name = name.upper().strip("/").replace("/", "_")
        return os.getenv(env_name, default)

def get_secret(secret_id: str, default: str | None = None) -> str | None:
    try:
        sm = _session.client("secretsmanager")
        r = sm.get_secret_value(SecretId=secret_id)
        if "SecretString" in r:
            return r["SecretString"]
        return r.get("SecretBinary")
    except ClientError:
        # Fallback to ENV var like FINANCE_EXTERNAL_API_KEY_JSON
        env_name = secret_id.upper().replace("/", "_")
        return os.getenv(env_name, default)

def get_secret_json(secret_id: str, default: dict | None = None) -> dict | None:
    raw = get_secret(secret_id)
    if not raw:
        return default
    try:
        return json.loads(raw)
    except Exception:
        return default
