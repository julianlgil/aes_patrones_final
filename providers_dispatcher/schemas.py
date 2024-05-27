from pydantic import BaseModel


class BillBase(BaseModel):
    amount: float
    paid: bool


class Bill(BillBase):
    id: str
    provider_id: str
    provider_account_id: str
    operation: str
