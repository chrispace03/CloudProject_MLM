from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.routes import router as api_router
from receipts import router as receipts_router     # <-- FastAPI router
from config_loader import get_param, get_secret_json

app = FastAPI(title="Finance API", version="1.0.0")

API_BASE = get_param("/finance/api_base_url", "http://localhost:5000")
ext = get_secret_json("finance/external_api_key", {"key": "demo-123"})
EXTERNAL_API_KEY = ext["key"]

# Versioned API
app.include_router(api_router, prefix="/api/v1")
app.include_router(receipts_router, prefix="/api/v1")   # <-- add this

@app.get("/")
def root():
    return {"message": "Finance API v1. See /docs, /api/v1/health, or /web"}

app.mount("/web", StaticFiles(directory="web", html=True), name="web")
