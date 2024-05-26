from fastapi import APIRouter

from .schemas import DispatchRequest

router = APIRouter()


@router.post("/dispatch")
def read_bill(request: DispatchRequest):
    response = {
        "billId": request.billId,
        "amount": 250000,
        "action": request.action,
        "provider_transaction_id": 2000,
        "provider_transaction_state": "success",
        "provider_client_id": 31245,
    }
    return response
