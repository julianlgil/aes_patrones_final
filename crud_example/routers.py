from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from .database import get_session
from .models import Bill

router = APIRouter()


@router.post("/bills/")
def create_bill(bill: Bill, session: Session = Depends(get_session)):
    session.add(bill)
    session.commit()
    session.refresh(bill)
    return bill


@router.get("/bills/{bill_id}")
def read_bill(bill_id: int, session: Session = Depends(get_session)):
    bill = session.get(Bill, bill_id)
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill


@router.get("/bills/", response_model=list[Bill])
def read_all_bills(
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    bills = session.exec(select(Bill).offset(offset).limit(limit)).all()
    return bills


@router.put("/bills/{bill_id}")
def update_bill(bill_id: int, bill: Bill, session: Session = Depends(get_session)):
    db_bill = session.get(Bill, bill_id)
    if not db_bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    for key, value in bill.dict().items():
        if not value:
            continue
        setattr(db_bill, key, value)
    session.commit()
    session.refresh(db_bill)
    return db_bill


@router.delete("/bills/{bill_id}")
def delete_bill(bill_id: int, session: Session = Depends(get_session)):
    db_bill = session.get(Bill, bill_id)
    if not db_bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    session.delete(db_bill)
    session.commit()
    return {"message": "Bill deleted"}
