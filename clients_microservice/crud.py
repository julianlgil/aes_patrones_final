from sqlmodel import Session, select

from crud_example.models import Bill


def create_bill(db: Session, bill: Bill) -> Bill:
    db.add(bill)
    db.commit()
    db.refresh(bill)
    return bill


def get_bill(db: Session, bill_id: int) -> Bill:
    return db.get(Bill, bill_id)


def get_bills(db: Session, skip: int = 0, limit: int = 10):
    return db.exec(select(Bill).offset(skip).limit(limit)).all()


def update_bill(db: Session, bill_id: int, bill: Bill) -> Bill:
    db_bill = db.get(Bill, bill_id)
    if db_bill:
        db_bill.amount = bill.amount
        db_bill.description = bill.description
        db.commit()
        db.refresh(db_bill)
    return db_bill


def delete_bill(db: Session, bill_id: int) -> bool:
    db_bill = db.get(Bill, bill_id)
    if db_bill:
        db.delete(db_bill)
        db.commit()
        return True
    return False
