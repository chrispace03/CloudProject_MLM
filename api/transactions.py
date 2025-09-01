from typing import List, Optional, Literal
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from api.security import get_current_user
from storage.transactions_csv import list_for_user, add_txn, update_txn, delete_txn, count_for_user

router = APIRouter(prefix="/transactions", tags=["transactions"])

class TxnIn(BaseModel):
    date: str
    amount: float
    category: str
    note: str = ""

class TxnOut(TxnIn):
    id: str

class TxnListOut(BaseModel):
    items: List[TxnOut]
    total: int
    limit: Optional[int] = None
    offset: int
    next_offset: Optional[int] = None
    sort: Optional[str] = None
    category: Optional[str] = None

SortKey = Literal["date", "-date", "amount", "-amount", "category", "-category"]

@router.get("", response_model=TxnListOut)
def list_txns(
    category: Optional[str] = None,
    limit: Optional[int] = None,
    offset: int = 0,
    sort: SortKey = "-date",
    user=Depends(get_current_user),
):
    total = count_for_user(user["user_id"], category)
    items = list_for_user(user["user_id"], category, limit, offset, sort)
    next_off = None
    if limit is not None and (offset + limit) < total:
        next_off = offset + limit
    return TxnListOut(
        items=items, total=total, limit=limit, offset=offset,
        next_offset=next_off, sort=sort, category=category
    )

@router.post("", response_model=TxnOut, status_code=201)
def create_txn(body: TxnIn, user=Depends(get_current_user)):
    return add_txn(user["user_id"], body.date, body.amount, body.category, body.note)

class TxnPatch(BaseModel):
    date: Optional[str] = None
    amount: Optional[float] = None
    category: Optional[str] = None
    note: Optional[str] = None

@router.put("/{tx_id}", response_model=TxnOut)
def update(tx_id: str, body: TxnPatch, user=Depends(get_current_user)):
    patched = {k: v for k, v in body.model_dump().items() if v is not None}
    row = update_txn(user["user_id"], tx_id, patched)
    if not row:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return row

@router.delete("/{tx_id}", status_code=204)
def delete(tx_id: str, user=Depends(get_current_user)):
    ok = delete_txn(user["user_id"], tx_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Transaction not found")
