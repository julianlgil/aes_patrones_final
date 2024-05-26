from enum import Enum
from typing import Any

from providers_dispatcher.web_service_clients.rest_client import RestClient
from providers_dispatcher.web_service_clients.soap_client import SoapClient
from providers_dispatcher.web_service_clients.webservice_client import WebserviceClient


class SupportedWebserviceClients(Enum):

    SOAP = 'SOAP'
    REST = 'REST'

    def __init__(self, client_type: str) -> None:
        self.client_type = client_type
        self.__creators = {
            'SOAP': SoapClient,
            'REST': RestClient
        }

    def get_client_instance(self, **config: Any) -> WebserviceClient:
        return self.__creators[self.client_type](**config)