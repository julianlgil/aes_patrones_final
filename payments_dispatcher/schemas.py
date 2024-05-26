from pydantic import BaseModel, Field


class DispatchRequest(BaseModel):
    billId: int
    action: str = Field(..., regex="^(query|pay)$")
