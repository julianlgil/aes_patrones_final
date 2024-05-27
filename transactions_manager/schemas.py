from decimal import Decimal

from pydantic import BaseModel, Field


class ProcessPaymentRequest(BaseModel):
    billId: int
    amount: Decimal
    client_account_id: int
    provider_account_id: int


class DispatchPayBillRequest(BaseModel):
    amount: Decimal
    paid: bool = False


class DispatchPayBillResponse(BaseModel):
    paid: bool
    provider_account_id: int


class ProcessPaymentResponse(BaseModel):
    billId: int
    amount: Decimal = Field(..., gte=0)
    action: str
    provider_transaction_id: str
    provider_transaction_state: str
    client_id: int
