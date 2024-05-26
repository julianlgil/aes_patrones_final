import requests

from .schemas import ReadBillResponse

default_headers = {
    "Content-Type": "application/json",
    "Cookie": "csrftoken=izpn1IwitshtEXNYIPcRCeZtXDEKmW5e",
}


def invoke_post_endpoint(
    url: str, payload: dict, headers: dict = default_headers
) -> requests.Response:
    response = requests.post(url=url, headers=headers, json=payload, timeout=5)
    return response


def query_bill(billId):
    dispatch_url = "http://payments_dispatcher:8011/dispatch"
    distpatch_payload = {"billId": billId, "action": "query"}
    distpatch_headers = {"Content-Type": "application/json"}
    response = invoke_post_endpoint(
        url=dispatch_url, payload=distpatch_payload, headers=distpatch_headers
    )
    if response.status_code != 200:
        return None
    response = ReadBillResponse(**response.json())
    return response
