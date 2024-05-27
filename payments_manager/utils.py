import requests
from fastapi import HTTPException

default_headers = {
    "Content-Type": "application/json",
    "Cookie": "csrftoken=izpn1IwitshtEXNYIPcRCeZtXDEKmW5e",
}


def invoke_post_endpoint(
    url: str, payload: dict, headers: dict = default_headers
) -> requests.Response:
    response = requests.post(url=url, headers=headers, json=payload, timeout=5)
    return response


def invoke_get_endpoint(url: str, headers: dict = default_headers) -> requests.Response:
    response = requests.get(url=url, headers=headers, timeout=5)
    return response


def query_bill(billId):
    host = "payments_dispatcher"
    dispatch_url = f"http://{host}:8011/dispatch"
    distpatch_payload = {"billId": billId, "action": "query"}
    distpatch_headers = default_headers
    response = invoke_post_endpoint(
        url=dispatch_url, payload=distpatch_payload, headers=distpatch_headers
    )
    if int(int(response.status_code / 100)) != 2:  # 2xx
        raise HTTPException(status_code=400, detail=f"Error endpoint: {host} ")
    return response.json()


def get_account_data(account_id):
    host = "accounts_microservice"
    balance_url = f"http://{host}:8013/account/{account_id}"
    balance_headers = default_headers
    response = invoke_get_endpoint(url=balance_url, headers=balance_headers)
    if int(int(response.status_code / 100)) != 2:  # 2xx
        raise HTTPException(status_code=400, detail=f"Error endpoint: {host} ")
    return response.json()
