from sqlalchemy import Column, Integer, String
from .database import Base


class Provider(Base):
    __tablename__ = "providers"

    id = Column(String, primary_key=True)
    name = Column(String)
    contract = Column(String)
    jsl = Column(String)
    service_type = Column(String)
    account_id = Column(Integer)
    client_id = Column(Integer)
