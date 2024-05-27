from pydantic import BaseModel


class ProviderBase(BaseModel):
    name: str
    contract: str
    jsl: str
    service_type: str
    account_id: str


class ProviderCreate(ProviderBase):
    pass


class Provider(ProviderBase):
    id: int

    class Config:
        orm_mode = True
