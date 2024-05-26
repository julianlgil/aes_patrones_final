from typing import Dict

from zeep import Client
from zeep.plugins import HistoryPlugin

from web_service_clients.models import RequestInfo
from web_service_clients.webservice_client import WebserviceClient


class SoapClient(WebserviceClient):

    def __init__(self, contract: str, **kwargs: Dict):
        self.wsdl = contract
        history = HistoryPlugin()
        self.client = Client(wsdl=self.wsdl, plugins=[history])
        super().__init__(**kwargs)

    def do_request(self, operation: str, request_info: RequestInfo):
        with self.client.settings(strict=False):
            response = self.client.service.__getitem__(request_info.path_operation)(**request_info.payload,
                                                                                    _soapheaders=request_info.headers)
            print(response)
