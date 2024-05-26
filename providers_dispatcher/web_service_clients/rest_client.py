from typing import Dict

from requests import Session

from providers_dispatcher.web_service_clients.models import RequestInfo
from providers_dispatcher.web_service_clients.webservice_client import WebserviceClient


class RestClient(WebserviceClient):

    def __init__(self, contract: str, **kwargs: Dict):
        self.host = contract
        self.client = Session()
        super().__init__(**kwargs)

    def do_request(self, operation: str, request_info: RequestInfo):
        response = self.client.request(
            method=request_info.method,
            url=self.host + request_info.path_operation,
            headers=request_info.headers,
            json=request_info.payload
        )
        response = response.json()
        print(response)
        return response
