# URL del WSDL
from lxml import etree
from zeep import Client
from zeep.plugins import HistoryPlugin

wsdl = 'https://www.crcind.com/csp/samples/SOAP.Demo.CLS?WSDL=1'

# Crear un cliente Zeep
history = HistoryPlugin()
client = Client(wsdl=wsdl, plugins=[history])

# Definir las estructuras XML para la solicitud y respuesta
add_integer_request = """
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org">
    <soapenv:Header/>
    <soapenv:Body>
        <tem:AddInteger>
            <tem:Arg1>10</tem:Arg1>
            <tem:Arg2>5</tem:Arg2>
        </tem:AddInteger>
    </soapenv:Body>
</soapenv:Envelope>
"""

divide_integer_request = """
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org">
    <soapenv:Header/>
    <soapenv:Body>
        <tem:DivideInteger>
            <tem:Arg1>10</tem:Arg1>
            <tem:Arg2>2</tem:Arg2>
        </tem:DivideInteger>
    </soapenv:Body>
</soapenv:Envelope>
"""

# Convertir las cadenas XML a objetos Element
add_integer_element = etree.fromstring(add_integer_request)
divide_integer_element = etree.fromstring(divide_integer_request)

# # Enviar la solicitud SOAP para AddInteger
# with client.settings(strict=False):
#     add_integer_response = client.service._binding.send(client, None, 'AddInteger', args=add_integer_element, kwargs=None)

# print('AddInteger Response:')
# print(etree.tostring(add_integer_response, pretty_print=True).decode())

# Enviar la solicitud SOAP para DivideInteger
test_data = {
    "Arg1": 10,
    "Arg2": 2
}
with client.settings(strict=False):
    divide_integer_response = client.service.__getitem__('DivideInteger')(**test_data, _soapheaders=None)

test_data = {
    "id": 1
}

with client.settings(strict=False):
    divide_integer_response = client.service.__getitem__('FindPerson')(**test_data, _soapheaders=None)

print('DivideInteger Response:')
print(etree.tostring(divide_integer_response, pretty_print=True).decode())