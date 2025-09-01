from typing import Dict, Any
from services.forecast import run_simulation
from storage.jobs import save_result, load_result
from api.schemas import ForecastRunIn

def health_check() -> Dict[str, str]:
    return {"status": "ok"}

def run_forecast(body: ForecastRunIn) -> Dict[str, Any]:
    payload = body.model_dump()
    result = run_simulation(
        start_balance=payload["start_balance"],
        horizon_months=payload["horizon_months"],
        mu_income=payload["mu_income"],
        sigma_income=payload["sigma_income"],
        mu_expense=payload["mu_expense"],
        sigma_expense=payload["sigma_expense"],
        n_paths=payload["n_paths"],
        seed=payload["seed"],
        repeats=payload["repeats"],
    )
    save_result(result["job_id"], result)
    rs = result["run_stats"]
    return {
        "job_id": result["job_id"],
        "summary": {
            "n_paths_per_repeat": rs["n_paths_per_repeat"],
            "repeats": rs["repeats"],
            "total_paths": rs["total_paths"],
            "horizon_months": rs["horizon_months"],
            "goal_probability": result["goal_probability"],
        }
    }

def get_forecast_result(job_id: str) -> Dict[str, Any]:
    data = load_result(job_id)
    if data is None:
        return {"error": f"job_id '{job_id}' not found"}
    return data
