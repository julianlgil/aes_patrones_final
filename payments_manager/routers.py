from fastapi import APIRouter

from .utils import query_bill

router = APIRouter()


# @router.post("/bills/")
# def create_bill(bill: Bill):
#     return bill


@router.get("/bill/{billId}")
def read_bill(billId: int):
    response = query_bill(billId=billId)
    return response
