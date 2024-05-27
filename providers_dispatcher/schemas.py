from pydantic import BaseModel


class BillBase(BaseModel):
    amount: float
    paid: bool


class Bill(BillBase):
    bill_reference: str
    provider_id: str
    provider_account_id: int
    operation: str
