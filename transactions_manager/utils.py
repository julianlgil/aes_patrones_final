from decimal import Decimal

import requests
from fastapi import HTTPException

from .schemas import DispatchPayBillRequest, DispatchPayBillResponse, ProcessPaymentRequest

default_headers = {
    "Content-Type": "application/json",
    "Cookie": "csrftoken=izpn1IwitshtEXNYIPcRCeZtXDEKmW5e",
}


def is_account_unblocked(account_id):
    """El objetivo es saber si la cuenta esta desbloqueada. Ajustar
    Si esta bloqueada, debe devolver un error"""
    host = "accounts_microservice"
    balance_url = f"http://{host}:8013/accounts/{account_id}"
    balance_headers = default_headers
    response = invoke_get_endpoint(url=balance_url, headers=balance_headers)
    if int(int(response.status_code / 100)) != 2:  # 2xx
        raise HTTPException(status_code=400, detail=f"Error endpoint: {host} ")
    if response.json().get("state") == "unblocked":
        return True, response.json().get("client_id")
    return False, response.json().get("client_id")


def change_block_account(account_id: int, action: str = "block"):
    """El objetivo es bloquear la cuenta. Ajustar"""
    host = "accounts_microservice"
    balance_url = f"http://{host}:8013/accounts/{account_id}"
    balance_headers = default_headers
    payload = {"state": action}
    response = invoke_patch_endpoint(url=balance_url, payload=payload, headers=balance_headers)
    if int(int(response.status_code / 100)) == 2:  # 2xx
        return True
    return False


def create_payment_transaction(source, target, amount, description):
    host = "transactions_microservice"
    balance_url = f"http://{host}:8021/transactions"
    balance_headers = default_headers
    payload = {
        "source_account": source,
        "target_account": target,
        "amount": float(amount),
        "description": description,
    }
    response = invoke_post_endpoint(url=balance_url, payload=payload, headers=balance_headers)
    if int(int(response.status_code / 100)) != 2:  # 2xx
        raise HTTPException(status_code=400, detail=f"Error endpoint: {host} ")
    transaction_id = response.json().get("id")
    return transaction_id


def change_balance_account(account_id, amount, action):
    host = "accounts_microservice"
    balance_url = f"http://{host}:8013/accounts/{account_id}"
    balance_headers = default_headers
    payload = {"balance": {"action": action, "amount": amount}}
    response = invoke_patch_endpoint(url=balance_url, payload=payload, headers=balance_headers)
    if int(int(response.status_code / 100)) != 2:  # 2xx
        raise HTTPException(status_code=400, detail=f"Error endpoint: {host} ")
    return True


def pay_bill(
    source: int,
    target: int,
    amount: Decimal,
    description: str = "bill payment",
):
    transaction_id = create_payment_transaction(source, target, amount, description)
    change_balance_account(source, amount, action="substract")
    change_balance_account(target, amount, action="add")
    return transaction_id


def proccess_payment(data: ProcessPaymentRequest):
    client_account_id = int(data.get("client_account_id", 0))
    is_unblocked, client_id = is_account_unblocked(client_account_id)
    block_account_state = change_block_account(client_account_id, action="block")

    if not is_unblocked:
        raise HTTPException(
            status_code=400, detail=f"Error: account {client_account_id} is blocked"
        )
    if not block_account_state:
        raise HTTPException(
            status_code=400, detail=f"Error: account {client_account_id} could not be blocked"
        )

    billId = int(data.get("billId", 0))
    response_dispatch_pay_bill: DispatchPayBillResponse = dispatch_pay_bill(billId, data)
    transaction_id = pay_bill(
        source=client_account_id,
        target=response_dispatch_pay_bill.provider_account_id,
        amount=data.get("amount"),
        description=f"bill payment {billId}",
    )
    block_account_state = change_block_account(client_account_id, action="unblock")

    data = {
        "billId": billId,
        "amount": data.get("amount"),
        "action": "pay",
        "provider_transaction_id": transaction_id,
        "client_id": client_id,
    }

    return data


def invoke_post_endpoint(
    url: str, payload: dict, headers: dict = default_headers
) -> requests.Response:
    response = requests.post(url=url, headers=headers, json=payload, timeout=5)
    return response


def invoke_get_endpoint(url: str, headers: dict = default_headers) -> requests.Response:
    response = requests.get(url=url, headers=headers, timeout=5)
    return response


def invoke_patch_endpoint(
    url: str, payload: dict, headers: dict = default_headers
) -> requests.Response:
    response = requests.patch(url=url, headers=headers, json=payload, timeout=5)
    return response


def dispatch_query_bill(billId: int):
    host = "payments_dispatcher"
    dispatch_url = f"http://{host}:8011/providers/bill/{billId}"
    distpatch_headers = default_headers
    response = invoke_get_endpoint(url=dispatch_url, headers=distpatch_headers)
    if int(int(response.status_code / 100)) != 2:  # 2xx
        raise HTTPException(status_code=400, detail=f"Error endpoint: {host} ")
    return response.json()


def dispatch_pay_bill(billId: int, data: DispatchPayBillRequest):
    host = "payments_dispatcher"
    dispatch_url = f"http://{host}:8011/providers/bill/{billId}"
    distpatch_payload = {"amount": data.get("amount"), "paid": False}
    distpatch_headers = default_headers
    response = invoke_post_endpoint(
        url=dispatch_url, payload=distpatch_payload, headers=distpatch_headers
    )
    if int(int(response.status_code / 100)) != 2:  # 2xx
        raise HTTPException(status_code=400, detail=f"Error endpoint: {host} ")
    return DispatchPayBillResponse(**response.json())


def get_account_data(account_id):
    host = "accounts_microservice"
    balance_url = f"http://{host}:8013/account/{account_id}"
    balance_headers = default_headers
    response = invoke_get_endpoint(url=balance_url, headers=balance_headers)
    if int(int(response.status_code / 100)) != 2:  # 2xx
        raise HTTPException(status_code=400, detail=f"Error endpoint: {host} ")
    return response.json()
