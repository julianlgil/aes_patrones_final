from decimal import Decimal

from pydantic import BaseModel, Field


class ReadBillResponse(BaseModel):
    billId: int
    amount: Decimal = Field(..., gte=0)
