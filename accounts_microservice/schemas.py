from decimal import Decimal

from pydantic import BaseModel, Field


class ReadAccountResponse(BaseModel):
    client_id: int
    account_id: int
    balance: Decimal = Field(..., gte=0)


class BalanceRequest(BaseModel):
    action: str = Field(..., regex="^(add|subtract)$")
    amount: Decimal


class AccountAction(BaseModel):
    state: str = Field(..., regex="^(block|unblock)$")


class UpdateAccountRequest(BaseModel):
    balance: BalanceRequest
    state: AccountAction


class UpdateAccountResponse(BaseModel):
    status: str = Field(..., regex="^(success|failed)$")
