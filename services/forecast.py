import time
import uuid
import random
from typing import Dict, Any, List, Optional

def _percentile(xs: List[float], p: float) -> float:
    if not xs:
        return 0.0
    ys = sorted(xs)
    k = (len(ys)-1) * (p/100.0)
    f = int(k)
    c = min(f + 1, len(ys)-1)
    if f == c:
        return ys[int(k)]
    d0 = ys[f] * (c - k)
    d1 = ys[c] * (k - f)
    return d0 + d1

def _one_pass(
    start_balance: float,
    horizon_months: int,
    mu_income: float,
    sigma_income: float,
    mu_expense: float,
    sigma_expense: float,
    n_paths: int,
    seed: Optional[int],
):
    if seed is not None:
        random.seed(seed)

    per_month_balances: list[list[float]] = [[] for _ in range(horizon_months)]
    terminal_balances: list[float] = []

    for _ in range(n_paths):
        bal = start_balance
        for m in range(horizon_months):
            income = random.gauss(mu_income, abs(sigma_income))
            expense = random.gauss(mu_expense, abs(sigma_expense))
            bal += (income + expense)
            per_month_balances[m].append(bal)
        terminal_balances.append(bal)

    return per_month_balances, terminal_balances

def run_simulation(
    start_balance: float,
    horizon_months: int,
    mu_income: float,
    sigma_income: float,
    mu_expense: float,
    sigma_expense: float,
    n_paths: int,
    seed: int | None = None,
    repeats: int = 1,
) -> Dict[str, Any]:
    """Monte-Carlo cashflow simulation. Runs `repeats` passes and pools paths."""
    t0 = time.time()

    pooled_per_month: list[list[float]] = [[] for _ in range(horizon_months)]
    pooled_terminal: list[float] = []

    for k in range(repeats):
        pass_seed = None if seed is None else seed + k
        per_month_balances, terminal_balances = _one_pass(
            start_balance, horizon_months,
            mu_income, sigma_income, mu_expense, sigma_expense,
            n_paths, pass_seed
        )
        for m in range(horizon_months):
            pooled_per_month[m].extend(per_month_balances[m])
        pooled_terminal.extend(terminal_balances)

    p5, p50, p95 = [], [], []
    for month_vals in pooled_per_month:
        p5.append(_percentile(month_vals, 5))
        p50.append(_percentile(month_vals, 50))
        p95.append(_percentile(month_vals, 95))

    successes = sum(1 for x in pooled_terminal if x >= 0)
    total_paths = max(1, n_paths * repeats)
    goal_probability = successes / total_paths

    job_id = str(uuid.uuid4())
    t1 = time.time()

    return {
        "job_id": job_id,
        "bands": {"p5": p5, "p50": p50, "p95": p95},
        "goal_probability": goal_probability,
        "run_stats": {
            "n_paths_per_repeat": n_paths,
            "repeats": repeats,
            "total_paths": total_paths,
            "horizon_months": horizon_months,
            "seconds": round(t1 - t0, 3),
        },
        "inputs": {
            "start_balance": start_balance,
            "mu_income": mu_income,
            "sigma_income": sigma_income,
            "mu_expense": mu_expense,
            "sigma_expense": sigma_expense,
            "seed": seed,
        },
    }
