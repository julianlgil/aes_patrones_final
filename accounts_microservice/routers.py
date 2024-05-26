from fastapi import APIRouter

from .schemas import ReadAccountResponse, UpdateAccountRequest, UpdateAccountResponse

router = APIRouter()

# @router.post("/bill/pay")
# def pay_bill(bill: PayBillRequest):
#     data_bill = query_bill(billId=bill.billId)
#     data_bill = ReadBillResponse(**data_bill.json())
#     return data_bill


@router.get("/account/{account_id}")
def read_account(account_id: int):
    data_account = ReadAccountResponse(
        **{"client_id": 1, "account_id": account_id, "balance": 999999999}
    )
    return data_account


@router.patch("/account/{account_id}")
def update_account(account_id: int, request: UpdateAccountRequest):
    # Si recibe balance, se actualiza el balance
    # Si recibe state, se actualiza el state (block o unblock)
    response = UpdateAccountResponse(**{"status": "success"})
    return response
