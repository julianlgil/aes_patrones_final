from enum import Enum
from typing import Optional

from pydantic import EmailStr, Field as PydanticField
from sqlmodel import Field, SQLModel
from typing_extensions import Annotated


class IdentificationType(str, Enum):
    cedula = "cédula"
    nit = "nit"
    tarjeta_identidad = "tarjeta de identidad"


class Client(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)

    name: Annotated[str, PydanticField(strip_whitespace=True, min_length=1, max_length=100)]
    last_name: Annotated[str, PydanticField(strip_whitespace=True, min_length=1, max_length=100)]
    identification_type: IdentificationType
    identification_number: Annotated[
        str, PydanticField(strip_whitespace=True, min_length=1, max_length=50)
    ]
    cellphone: Annotated[str, PydanticField(strip_whitespace=True, pattern=r"^\d{10}$")]
    email: EmailStr
    address: Optional[Annotated[str, PydanticField(strip_whitespace=True, max_length=250)]] = None
    neighborhood: Optional[Annotated[str, PydanticField(strip_whitespace=True, max_length=100)]] = (
        None
    )
    city: Annotated[str, PydanticField(strip_whitespace=True, min_length=1, max_length=100)]
    state: Annotated[str, PydanticField(strip_whitespace=True, min_length=1, max_length=100)]
    country: Annotated[str, PydanticField(strip_whitespace=True, min_length=1, max_length=100)]
    zip_code: Optional[Annotated[str, PydanticField(strip_whitespace=True, max_length=20)]] = None
    dane_code: Optional[Annotated[str, PydanticField(strip_whitespace=True, max_length=20)]] = None
