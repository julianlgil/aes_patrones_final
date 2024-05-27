import os
from typing import Dict, Optional

import requests

from providers_dispatcher.jslt.jslt_jsonata import transform_json
from providers_dispatcher.schemas import Bill
from providers_dispatcher.web_service_clients.models import RequestInfo
from providers_dispatcher.web_service_clients.supported_webservice_clients import SupportedWebserviceClients


def get_provider(provider_id) -> Dict:
    url = os.getenv('PROVIDERS_HOST') + provider_id
    response = requests.get(url)
    return response.json()


class Dispatcher:

    def __init__(self):
        pass

    def do_request(self, provider_id: str, operation: str, payload: Optional[Dict]):
        provider = get_provider(provider_id=provider_id)
        print(f"Provider: {provider}")
        webservice_type = provider['service_type']
        contract = provider['contract']
        template = provider['jsl']
        request_data = transform_json(input_json=payload, template=template)
        client = SupportedWebserviceClients[webservice_type].get_client_instance(
            contract=contract,
        )
        response = client.do_request(operation=operation, request_info=RequestInfo.parse_obj(request_data.get(
            f'{operation}_request')))
        transformed_response = transform_json(input_json=response, template=template)
        result = transformed_response.get(f'{operation}_response')
        result.update({
            "provider_id": provider_id,
            "operation": operation,
            "provider_account_id": provider.get('account_id')
        })
        print(f"Result: {result}")
        return Bill(**result)
