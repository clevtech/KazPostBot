import requests
import xml.dom.minidom

url="http://89.218.48.181:8080/altsmsgate/altsmsgate.wsdl"
headers = {'content-type': 'text/xml'}

with open("./request.xml", "r") as file:
    req = file.read()

response = requests.post(url, data=req, headers=headers)

pretyy = xml.dom.minidom.parseString(response.content)
pretty_xml_as_string = pretyy.toprettyxml()
print(pretty_xml_as_string)

