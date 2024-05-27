from fastapi import APIRouter

from .schemas import DispatchRequest

router = APIRouter()


@router.post("/providers/bill/{bill_reference}")
def pay_bill(bill_reference: str, request: DispatchRequest):
    response = {
        "amount": 250000,
        "paid": True,
        "id": bill_reference,
        "provider_id": "698465",
        "provider_account_id": "1",
        "operation": "pay_bill",
    }
    return response


@router.get("/providers/bill/{bill_reference}")
def read_bill(bill_reference: str):
    response = {
        "amount": 250000,
        "paid": False,
        "id": bill_reference,
        "provider_id": "698465",
        "provider_account_id": "1",
        "operation": "get_bill",
    }
    return response
