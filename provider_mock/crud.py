from typing import Optional

from .schemas import Bill, BillUpdate

# Simulated in-memory database
bills = [
    {"id": "12341", "amount": 100.0, "paid": False},
    {"id": "12342", "amount": 150.0, "paid": True},
    {"id": "12343", "amount": 200.0, "paid": False},
    {"id": "12344", "amount": 300.0, "paid": False},
    {"id": "12345", "amount": 400.0, "paid": False},
    {"id": "12346", "amount": 500.0, "paid": False},
    {"id": "12347", "amount": 600.0, "paid": False},
    {"id": "12348", "amount": 700.0, "paid": False},
    {"id": "12349", "amount": 800.0, "paid": False},
    {"id": "123410", "amount": 900.0, "paid": False},
    {"id": "98761", "amount": 100.0, "paid": False},
    {"id": "98762", "amount": 150.0, "paid": True},
    {"id": "98763", "amount": 200.0, "paid": False},
]


def get_bill(bill_id: str) -> Optional[Bill]:
    for bill in bills:
        if bill["id"] == bill_id:
            return Bill(**bill)
    return None


def update_bill(bill_id: str, bill_update: BillUpdate) -> Optional[Bill]:
    for bill in bills:
        if bill["id"] == bill_id:
            bill["paid"] = bill_update.paid
            return Bill(**bill)
    return None
