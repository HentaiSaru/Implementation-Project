import requests

link_list = [
    "https://raw.githubusercontent.com/TenshinoOtoKafu/Implementation-Project/Main/python%20Implementation/測試項目/SourceCode_URL_Conversion.py",
    # "https://raw.githubusercontent.com/TenshinoOtoKafu/Implementation-Project/Main/python%20Implementation/測試項目/backend.py",
    "https://raw.githubusercontent.com/TenshinoOtoKafu/Implementation-Project/Main/python%20Implementation/ExperimentalBrowser/TestBrowser.py",
]

namespace = {}

def link_request(url,name):
    response = requests.get(url)
    code = response.text
    exec(code,name)

for link in link_list:
    link_request(link,namespace)

# og = namespace['ogcode']()
# print(og.convert(""))

TB = namespace['TestBrowser']()
# print(TB.get_version())
TB.Enable_browsing()

# cal = namespace['calculate']()
# cal.count(input("數字:"),input("運算符:"),input("數字:"))
# result = cal.get_result()
# print(result)