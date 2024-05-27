from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, constr


class ReadAccountResponse(BaseModel):
    client_id: int
    account_id: int
    balance: Decimal = Field(..., gte=0)
    state: str


class BalanceRequest(BaseModel):
    action: str = Field(..., regex="^(add|substract)$")
    amount: Decimal


class AccountAction(BaseModel):
    state: str = Field(..., regex="^(block|unblock)$")


class UpdateAccountRequest(BaseModel):
    balance: Optional[BalanceRequest]
    state: Optional[constr(regex="^(block|unblock)$")] = None


class UpdateAccountResponse(BaseModel):
    status: str = Field(..., regex="^(success|failed)$")
