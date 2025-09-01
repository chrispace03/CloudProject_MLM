from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class ForecastRunIn(BaseModel):
    start_balance: float = Field(2500, description="Starting balance")
    horizon_months: int = Field(12, ge=1, le=120)
    mu_income: float = 3200
    sigma_income: float = 400
    mu_expense: float = -2400
    sigma_expense: float = 300
    n_paths: int = Field(5000, ge=1, description="Paths per repeat")
    seed: Optional[int] = Field(None, description="Base RNG seed (repeat k uses seed+k)")
    repeats: int = Field(1, ge=1, le=50, description="Run the sim this many times and pool results")

class ForecastBands(BaseModel):
    p5: List[float]
    p50: List[float]
    p95: List[float]

class ForecastResultOut(BaseModel):
    job_id: str
    bands: ForecastBands
    goal_probability: float
    run_stats: Dict[str, Any]
    inputs: Dict[str, Any]
