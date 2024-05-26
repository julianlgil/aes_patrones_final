from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from .database import get_session
from .models import Client

router = APIRouter()


@router.post("/clients/")
def create_client(client: Client, session: Session = Depends(get_session)):
    session.add(client)
    session.commit()
    session.refresh(client)
    return client


@router.get("/clients/{client_id}")
def read_client(client_id: int, session: Session = Depends(get_session)):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.get("/clients/", response_model=list[Client])
def read_all_clients(
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    bills = session.exec(select(Client).offset(offset).limit(limit)).all()
    return bills


@router.put("/clients/{client_id}")
def update_client(client_id: int, client: Client, session: Session = Depends(get_session)):
    db_bill = session.get(Client, client_id)
    if not db_bill:
        raise HTTPException(status_code=404, detail="Client not found")
    for key, value in client.dict().items():
        if not value:
            continue
        setattr(db_bill, key, value)
    session.commit()
    session.refresh(db_bill)
    return db_bill


@router.delete("/clients/{client_id}")
def delete_client(client_id: int, session: Session = Depends(get_session)):
    db_bill = session.get(Client, client_id)
    if not db_bill:
        raise HTTPException(status_code=404, detail="Client not found")
    session.delete(db_bill)
    session.commit()
    return {"message": "Client deleted"}
