import os, json
from typing import Optional, Dict, Any
from common.config import JOBS_DIR

def save_result(job_id: str, payload: Dict[str, Any]) -> None:
    os.makedirs(JOBS_DIR, exist_ok=True)
    path = os.path.join(JOBS_DIR, f"{job_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

def load_result(job_id: str) -> Optional[Dict[str, Any]]:
    path = os.path.join(JOBS_DIR, f"{job_id}.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
