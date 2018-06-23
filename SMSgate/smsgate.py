import requests
import xml.dom.minidom

url = "http://89.218.48.181:8080/smsgate/?wsdl "
headers = {'content-type': 'text/xml'}

with open("./request.xml", "r") as file:
    req = file.read()

with open("./check.xml", "r") as file:
    req2 = file.read()

response = requests.post(url, data=req2.encode('utf-8'), headers=headers)

pretyy = xml.dom.minidom.parseString(response.content)
pretty_xml_as_string = pretyy.toprettyxml()
print(pretty_xml_as_string)

