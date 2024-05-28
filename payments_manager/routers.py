from fastapi import APIRouter, HTTPException

from .rabbit import send_rabbit_message
from .schemas import MessageToProcessPayment, PayBillRequest, ReadBillResponse
from .utils import get_account_data, query_bill

router = APIRouter()


@router.post("/bill/pay")
def pay_bill(bill: PayBillRequest):
    bill_data = query_bill(billId=bill.billId)
    amount_bill = bill_data.get("amount", 0)
    account_data = get_account_data(account_id=bill.client_account_id)
    balance = account_data.get("balance", 0)

    has_enough_money = balance > amount_bill

    client_id = account_data.get("client_id", None)

    if client_id != bill.client_account_id:
        raise HTTPException(status_code=404, detail="Client not found")
    if int(bill_data.get("bill_reference", 0)) != bill.billId:
        raise HTTPException(status_code=404, detail="Bill not found")
    if not has_enough_money:
        raise HTTPException(status_code=404, detail="Not enough money")

    message = MessageToProcessPayment(
        billId=bill.billId,
        amount=amount_bill,
        client_account_id=client_id,
        provider_account_id=bill_data.get("provider_account_id"),
    ).dict()

    # Publicar mensaje en la cola
    send_rabbit_message(message)

    return {"transaction_state": "pending"}


@router.get("/bill/{billId}")
def read_bill(billId: int):
    data_bill = query_bill(billId=billId)

    data_bill = ReadBillResponse(
        **{"amount": data_bill.get("amount", None), "billId": data_bill.get("bill_reference", None)}
    )
    return data_bill
