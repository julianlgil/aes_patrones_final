from sqlmodel import Field, SQLModel


class Bill(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    amount: float
