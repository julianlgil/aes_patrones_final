from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from providers_microservice import database
from providers_microservice.database import Base, get_db
from providers_microservice.repository import get_provider, get_providers
from providers_microservice.schemas import Provider, ProviderCreate

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=database.engine)


# Dependency
@app.post("/providers/", response_model=Provider)
async def create_provider(provider: ProviderCreate, db: Session = Depends(get_db)):
    return create_provider(db=db, provider=provider)


@app.get("/providers/{provider_id}", response_model=Provider)
async def read_provider(provider_id: str, db: Session = Depends(get_db)):
    db_provider = get_provider(db, provider_id=provider_id)
    if db_provider is None:
        raise HTTPException(status_code=404, detail="Provider not found")
    return db_provider


@app.get("/providers/", response_model=list[Provider])
async def read_providers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    providers = get_providers(db, skip=skip, limit=limit)
    return providers


@app.put("/providers/{provider_id}", response_model=Provider)
async def update_provider(provider_id: int, provider: ProviderCreate, db: Session = Depends(get_db)):
    db_provider = update_provider(db, provider_id=provider_id, provider=provider)
    if db_provider is None:
        raise HTTPException(status_code=404, detail="Provider not found")
    return db_provider


@app.delete("/providers/{provider_id}", response_model=Provider)
async def delete_provider(provider_id: int, db: Session = Depends(get_db)):
    db_provider = delete_provider(db, provider_id=provider_id)
    if db_provider is None:
        raise HTTPException(status_code=404, detail="Provider not found")
    return db_provider


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8014)
