import requests

link_list = [
    "https://raw.githubusercontent.com/TenshinoOtoKafu/Implementation-Project/Main/python%20Implementation/測試項目/SourceCode_URL_Conversion.py",
    "https://raw.githubusercontent.com/TenshinoOtoKafu/Implementation-Project/Main/python%20Implementation/ExperimentalBrowser/TestBrowser.py",
]

namespace = {}

def link_request(url,name):
    response = requests.get(url)
    code = response.text
    exec(code,name)

for link in link_list:
    link_request(link,namespace)

og = namespace['ogcode']()
og.convert("")

# TB = namespace['TestBrowser']()
# TB.Enable_browsing()
# print(TB.get_version())