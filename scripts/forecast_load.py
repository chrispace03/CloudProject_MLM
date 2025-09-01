# Usage: python scripts/forecast_load.py --url http://<host>:3000/api/v1/forecast/run --minutes 5 --parallel 10
import time, argparse, requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def post_once(session, url, payload):
    t0 = time.perf_counter()
    r = session.post(url, json=payload, timeout=300)
    ms = (time.perf_counter() - t0) * 1000
    return r.status_code, ms

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--url', required=True)
    ap.add_argument('--minutes', type=int, default=5)
    ap.add_argument('--parallel', type=int, default=10)
    args = ap.parse_args()

    payload = {"n_paths": 400000, "horizon_months": 36, "repeats": 3}
    end_at = time.time() + args.minutes * 60
    sent = ok = 0
    total_ms = 0.0

    with requests.Session() as s, ThreadPoolExecutor(max_workers=args.parallel) as ex:
        while time.time() < end_at:
            futs = [ex.submit(post_once, s, args.url, payload) for _ in range(args.parallel)]
            for fu in as_completed(futs):
                status, ms = fu.result()
                sent += 1; total_ms += ms
                if 200 <= status < 300:
                    ok += 1

    avg = (total_ms / sent) if sent else 0.0
    print(f"Sent={sent} OK={ok} Avg={avg:.1f}ms")

if __name__ == "__main__":
    main()
