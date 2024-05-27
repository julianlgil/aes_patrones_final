from decimal import Decimal
from typing import Optional

from pydantic import Field as PydanticField
from sqlmodel import Field, SQLModel
from typing_extensions import Annotated


class Transaction(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)

    source_account: Annotated[int, PydanticField(ge=1)]
    target_account: Annotated[int, PydanticField(ge=1)]
    amount: Annotated[Decimal, PydanticField(gt=0)]
    description: Annotated[Optional[str], PydanticField(strip_whitespace=True, max_length=250)] = (
        None
    )
