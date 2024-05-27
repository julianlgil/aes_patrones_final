from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from .database import get_session
from .models import Transaction

router = APIRouter()


@router.post("/transactions/")
def create_client(transaction: Transaction, session: Session = Depends(get_session)):
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction


@router.get("/transactions/{transaction_id}")
def read_client(transaction_id: int, session: Session = Depends(get_session)):
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.get("/transactions/", response_model=list[Transaction])
def read_all_clients(
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    bills = session.exec(select(Transaction).offset(offset).limit(limit)).all()
    return bills
