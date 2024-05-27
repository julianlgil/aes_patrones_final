from decimal import Decimal

from pydantic import BaseModel, Field


class ReadBillResponse(BaseModel):
    billId: int
    amount: Decimal = Field(..., gte=0)


class PayBillRequest(BaseModel):
    billId: int
    client_account_id: int


class MessageToProcessPayment(BaseModel):
    billId: int
    amount: Decimal
    client_account_id: int
    provider_account_id: int
