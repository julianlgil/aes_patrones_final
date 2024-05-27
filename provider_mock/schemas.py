from pydantic import BaseModel


class BillBase(BaseModel):
    amount: float
    paid: bool


class BillCreate(BillBase):
    pass


class BillUpdate(BaseModel):
    paid: bool


class Bill(BillBase):
    id: int

