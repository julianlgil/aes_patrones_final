from fastapi import FastAPI, HTTPException

from providers_dispatcher.dispatcher import Dispatcher
from providers_dispatcher.schemas import Bill, BillBase

app = FastAPI()


@app.get("/providers/bill/{bill_reference}", response_model=Bill)
async def get_bill(bill_reference: str):
    try:
        dispatcher = Dispatcher()
        provider_id = bill_reference[0:4]
        json_data = {
            "bill_reference": bill_reference
        }
        return dispatcher.do_request(provider_id, 'get_bill', json_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/providers/bill/{bill_reference}", response_model=Bill)
async def pay_bill(bill_reference: str, payment: BillBase):
    try:
        dispatcher = Dispatcher()
        provider_id = bill_reference[0:4]
        json_data = {
            "bill_reference": bill_reference,
            "payment_amount": payment.amount,
            "paid": payment.paid
        }
        return dispatcher.do_request(provider_id, 'pay_bill', json_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8011)
