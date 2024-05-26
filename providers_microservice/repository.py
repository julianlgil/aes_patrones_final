from sqlalchemy.orm import Session

from providers_microservice.models import Provider
from providers_microservice.schemas import ProviderCreate


def get_provider(db: Session, provider_id: str):
    return db.query(Provider).filter(Provider.id == provider_id).first()


def get_providers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Provider).offset(skip).limit(limit).all()


def create_provider(db: Session, provider: ProviderCreate):
    db_provider = Provider(**provider.dict())
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)
    return db_provider


def update_provider(db: Session, provider_id: str, provider: ProviderCreate):
    db_provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if db_provider is None:
        return None
    for key, value in provider.dict().items():
        setattr(db_provider, key, value)
    db.commit()
    db.refresh(db_provider)
    return db_provider


def delete_provider(db: Session, provider_id: str):
    db_provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if db_provider:
        db.delete(db_provider)
        db.commit()
    return db_provider
