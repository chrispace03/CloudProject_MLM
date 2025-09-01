import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = BASE_DIR / "uploads"
REPORTS_DIR = BASE_DIR / "reports"
JOBS_DIR = DATA_DIR / "jobs"
TXN_CSV = DATA_DIR / "transactions.csv"

# Ensure directories exist
for d in (DATA_DIR, UPLOADS_DIR, REPORTS_DIR, JOBS_DIR):
    d.mkdir(parents=True, exist_ok=True)

# Security
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
JWT_ALGORITHM = "HS256"
