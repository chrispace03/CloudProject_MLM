import csv, os, uuid, tempfile
from typing import List, Dict, Optional
from common.config import TXN_CSV

FIELDS = ["id", "user_id", "date", "amount", "category", "note"]

def _read_all() -> List[Dict[str, str]]:
    if not os.path.exists(TXN_CSV):
        return []
    with open(TXN_CSV, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def _write_all(rows: List[Dict[str, str]]) -> None:
    os.makedirs(os.path.dirname(TXN_CSV), exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(TXN_CSV))
    os.close(fd)
    with open(tmp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    os.replace(tmp, TXN_CSV)

def count_for_user(user_id: str, category: Optional[str] = None) -> int:
    rows = [r for r in _read_all() if r["user_id"] == user_id]
    if category:
        rows = [r for r in rows if r["category"] == category]
    return len(rows)

def list_for_user(user_id: str, category: Optional[str] = None,
                  limit: Optional[int] = None, offset: int = 0,
                  sort: str = "-date") -> List[Dict[str, str]]:
    rows = [r for r in _read_all() if r["user_id"] == user_id]
    if category:
        rows = [r for r in rows if r["category"] == category]

    reverse = sort.startswith("-")
    key = sort.lstrip("-")
    if key == "amount":
        rows.sort(key=lambda r: float(r["amount"]), reverse=reverse)
    elif key == "date":
        rows.sort(key=lambda r: r["date"], reverse=reverse)
    elif key == "category":
        rows.sort(key=lambda r: r["category"], reverse=reverse)

    if offset:
        rows = rows[offset:]
    if limit is not None:
        rows = rows[:max(0, limit)]
    return rows

def add_txn(user_id: str, date: str, amount: float, category: str, note: str) -> Dict[str, str]:
    rows = _read_all()
    row = {"id": str(uuid.uuid4()), "user_id": user_id, "date": date,
           "amount": f"{amount}", "category": category, "note": note}
    rows.append(row)
    _write_all(rows)
    return row

def update_txn(user_id: str, tx_id: str, patch: Dict[str, str]) -> Optional[Dict[str, str]]:
    rows = _read_all()
    found = None
    for r in rows:
        if r["id"] == tx_id and r["user_id"] == user_id:
            r.update({k: (f"{v}" if k=="amount" else v) for k, v in patch.items()
                      if k in FIELDS and k not in ("id","user_id")})
            found = r
            break
    if found:
        _write_all(rows)
    return found

def delete_txn(user_id: str, tx_id: str) -> bool:
    rows = _read_all()
    new_rows = [r for r in rows if not (r["id"] == tx_id and r["user_id"] == user_id)]
    if len(new_rows) == len(rows):
        return False
    _write_all(new_rows)
    return True
