from pydantic import BaseModel


class BillBase(BaseModel):
    amount: float | None = None
    paid: bool


class Bill(BillBase):
    bill_reference: str
    provider_id: str
    provider_account_id: int
    operation: str
