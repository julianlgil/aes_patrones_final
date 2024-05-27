from fastapi import FastAPI, HTTPException

from provider_mock.crud import get_bill, update_bill
from provider_mock.schemas import Bill, BillUpdate

app = FastAPI()


@app.get("/bills/{bill_id}", response_model=Bill)
def read_bill(bill_id: str):
    bill = get_bill(bill_id)
    if bill is None:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill


@app.post("/bills/{bill_id}/pay", response_model=Bill)
def pay_bill(bill_id: str):
    bill = get_bill(bill_id)
    if bill is None:
        raise HTTPException(status_code=404, detail="Bill not found")

    bill_update = BillUpdate(paid=True)
    updated_bill = update_bill(bill_id, bill_update)
    if updated_bill is None:
        raise HTTPException(status_code=404, detail="Bill not found")
    return updated_bill


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
