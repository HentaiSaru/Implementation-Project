from unicodedata import normalize
import requests

session = requests.Session()
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

url = "https://files.catbox.moe/dz64k5.mp4"
filterdomains=["google.com","bing.com","youtube.com","facebook.com","line.me","sharepoint.com","taobao.com","shopee.tw"]

#data = session.get(url, headers=headers)
data = session.head(url , headers=headers)

# if data.url == url:
    # print("錯誤的")

print(data.status_code)
print(data.url)