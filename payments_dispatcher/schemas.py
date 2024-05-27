from pydantic import BaseModel


class DispatchRequest(BaseModel):
    amount: int
    paid: bool
