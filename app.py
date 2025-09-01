from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.routes import router as api_router

app = FastAPI(title="Finance API", version="1.0.0")

# Versioned API
app.include_router(api_router, prefix="/api/v1")

# Simple landing & static web client
@app.get("/")
def root():
    return {"message": "Finance API v1. See /docs, /api/v1/health, or /web"}

app.mount("/web", StaticFiles(directory="web", html=True), name="web")
