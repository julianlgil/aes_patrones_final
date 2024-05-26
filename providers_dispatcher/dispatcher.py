import json
import os
from typing import Dict, Optional

import requests

from providers_dispatcher.jslt.jslt_jsonata import transform_json
from web_service_clients.models import RequestInfo
from web_service_clients.supported_webservice_clients import SupportedWebserviceClients


def get_provider(provider_id) -> Dict:
    # with open("transformation_config.json") as f:
    #     transform_config = f.read()
    # with open("transformation_config_rest.json") as f:
    #     transform_config_rest = f.read()
    # if provider_id == 2:
    #     return {
    #         'service_type': 'SOAP',
    #         'contract': 'https://www.crcind.com/csp/samples/SOAP.Demo.CLS?WSDL=1',
    #         'template': transform_config
    #     }
    # else:
    #     return {
    #         'service_type': 'REST',
    #         'contract': 'https://api.restful-api.dev',
    #         'template': transform_config_rest
    #     }
    url = os.getenv('PROVIDERS_HOST') + provider_id
    response = requests.get(url)
    return response.json()


class Dispatcher:

    def __init__(self):
        pass

    def do_request(self, provider_id: str, operation: str, payload: Optional[Dict]):
        provider = get_provider(provider_id=provider_id)
        webservice_type = provider['service_type']
        contract = provider['contract']
        template = provider['template']
        request_data = transform_json(input_json=payload, template=template)
        client = SupportedWebserviceClients[webservice_type].get_client_instance(
            contract=contract,
        )
        response = client.do_request(operation=operation, request_info=RequestInfo.parse_obj(request_data.get(
            f'{operation}_request')))
        transformed_response = transform_json(input_json=response, template=template)
        return transformed_response.get(f'{operation}_response')


json_data = {
    "invoice_reference": 7,
    "payment_amount": 10000
}

