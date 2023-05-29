import requests

url = "https://raw.githubusercontent.com/TenshinoOtoKafu/Implementation-Project/Main/python%20Implementation/測試項目/backend.py"
response = requests.get(url)

code = response.text

namespace = {}
exec(code,namespace)

cal = namespace['calculate']()
cal.count(input("數字:"),input("運算符:"),input("數字:"))
result = cal.get_result()

print(result)