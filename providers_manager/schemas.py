from pydantic import BaseModel


class ProviderBase(BaseModel):
    name: str
    contract: str
    jsl: str
    service_type: str
    account_id: int
    client_id: int


class Provider(ProviderBase):
    id: str

    class Config:
        orm_mode = True


class ProviderCreate(Provider):
    pass
