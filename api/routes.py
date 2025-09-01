from fastapi import APIRouter, Depends
from api.controllers import health_check, run_forecast, get_forecast_result
from api.auth import router as auth_router
from api.transactions import router as txn_router
from api.uploads import router as uploads_router
from api.schemas import ForecastRunIn

router = APIRouter()

@router.get("/health")
def health():
    return health_check()

# Auth
router.include_router(auth_router, prefix="/auth", tags=["auth"])

# Transactions and uploads (protected in their own modules)
router.include_router(txn_router)
router.include_router(uploads_router, prefix="/uploads", tags=["uploads"])

# Forecast
@router.post("/forecast/run")
def forecast_run(body: ForecastRunIn):
    return run_forecast(body)

@router.get("/forecast/result/{job_id}")
def forecast_result(job_id: str):
    return get_forecast_result(job_id)
