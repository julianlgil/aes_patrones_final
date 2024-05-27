from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from .database import get_session
from .models import Account
from .schemas import ReadAccountResponse, UpdateAccountRequest, UpdateAccountResponse

router = APIRouter()


@router.post("/accounts/")
def create_account(account: Account, session: Session = Depends(get_session)):
    session.add(account)
    session.commit()
    session.refresh(account)
    return account


@router.get("/accounts/{account_id}/client/{client_id}")
def read_account(account_id: int, client_id: int, session: Session = Depends(get_session)):
    statement = select(Account).where(Account.id == account_id, Account.client_id == client_id)
    results = session.exec(statement)
    account = results.first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    data_account = ReadAccountResponse(
        client_id=account.client_id,
        account_id=account.id,
        balance=account.balance,
        state=account.state,
    )
    return data_account


@router.get("/accounts/{account_id}")
def read_account(account_id: int, session: Session = Depends(get_session)):
    account = session.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="account not found")
    data_account = ReadAccountResponse(
        **{
            "client_id": account.client_id,
            "account_id": account.id,
            "balance": account.balance,
            "state": account.state,
        }
    )
    return data_account


@router.get("/accounts/", response_model=list[Account])
def read_all_accounts(
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    bills = session.exec(select(Account).offset(offset).limit(limit)).all()
    return bills


@router.delete("/accounts/{account_id}")
def delete_account(account_id: int, session: Session = Depends(get_session)):
    db_bill = session.get(Account, account_id)
    if not db_bill:
        raise HTTPException(status_code=404, detail="account not found")
    session.delete(db_bill)
    session.commit()
    return {"message": "account deleted"}


@router.patch("/accounts/{account_id}")
def update_account(
    account_id: int, request: UpdateAccountRequest, session: Session = Depends(get_session)
):
    account = session.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="account not found")

    if request.balance:
        if request.balance.action == "add":
            total = account.balance + float(request.balance.amount)
            setattr(account, "balance", total)
        elif request.balance.action == "substract":
            total = account.balance - float(request.balance.amount)
            if total < 0:
                raise HTTPException(status_code=400, detail="balance not enough")
            setattr(account, "balance", total)
    if request.state:
        if request.state == "block":
            setattr(account, "state", "blocked")
        elif request.state == "unblock":
            setattr(account, "state", "unblocked")
    session.commit()
    session.refresh(account)
    response = UpdateAccountResponse(**{"status": "success"})
    return response
