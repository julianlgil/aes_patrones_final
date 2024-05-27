from typing import List, Optional
from .schemas import Bill, BillCreate, BillUpdate

# Simulated in-memory database
bills = [
    {"id": 1, "amount": 100.0, "paid": False},
    {"id": 2, "amount": 150.0, "paid": True},
    {"id": 3, "amount": 200.0, "paid": False},
]


def get_bill(bill_id: int) -> Optional[Bill]:
    for bill in bills:
        if bill["id"] == bill_id:
            return Bill(**bill)
    return None


def update_bill(bill_id: int, bill_update: BillUpdate) -> Optional[Bill]:
    for bill in bills:
        if bill["id"] == bill_id:
            bill["paid"] = bill_update.paid
            return Bill(**bill)
    return None
