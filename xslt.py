
from lxml import etree
from zeep import Client

# Cargar el JSON desde un archivo

# JSON de entrada
json_data = {
    "AddIntegerRequest": {
      "Arg1": 10,
      "Arg2": 5
    }

}


def json_to_xml(json_data):
  def build_xml(element, data):
    if isinstance(data, dict):
      for key, value in data.items():
        sub_element = etree.SubElement(element, key)
        build_xml(sub_element, value)
    elif isinstance(data, list):
      for item in data:
        build_xml(element, item)
    else:
      element.text = str(data)

  root = etree.Element('AddInteger')
  build_xml(root, json_data)
  return etree.tostring(root, encoding='unicode')

# Transformar el JSON en XML utilizando el XSLT generado
xslt = etree.parse('output2.xsl')
print(etree.tostring(xslt))
transform = etree.XSLT(xslt)
xml_in = json_to_xml(json_data)
xml_data = transform(etree.fromstring(xml_in))
print(etree.tostring(xml_data))

# Crear un cliente Zeep para hacer la solicitud al servicio web
wsdl_url = 'https://www.crcind.com/csp/samples/SOAP.Demo.CLS?WSDL=1'
client = Client(wsdl=wsdl_url)

# Hacer la solicitud a la operación GetXSDForTypeSystem
response = client.service.AddInteger(xml_data)

# Manejar la respuesta como sea necesario
print(response)