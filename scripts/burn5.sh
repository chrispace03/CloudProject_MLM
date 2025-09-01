#!/usr/bin/env bash
# Usage: ./scripts/burn5.sh http://<host>:3000/api/v1/forecast/run 10
URL=${1:-http://127.0.0.1:3000/api/v1/forecast/run}
PARALLEL=${2:-10}
END=$((SECONDS+300))
while [ $SECONDS -lt $END ]; do
  for s in $(seq 1 "$PARALLEL"); do
    curl -s -X POST "$URL" -H 'Content-Type: application/json'       -d '{"n_paths": 400000, "horizon_months": 36, "repeats": 3}' >/dev/null &
  done
  wait
done
echo "done"
