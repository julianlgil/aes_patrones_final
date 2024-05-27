from enum import Enum
from typing import Optional

from pydantic import Field
from sqlmodel import Field, SQLModel
from typing_extensions import Annotated


class AccountType(str, Enum):
    ahorros = "ahorros"
    corriente = "corriente"


class AccountState(str, Enum):
    blocked = "blocked"
    unblocked = "unblocked"


class Account(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    account_type: AccountType
    client_id: Annotated[int, Field()]
    state: AccountState = Field(default=AccountState.unblocked)
    balance: Optional[float] = Field(default=0.0)
