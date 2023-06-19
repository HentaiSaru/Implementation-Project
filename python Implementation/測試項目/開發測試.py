from unicodedata import normalize
import requests

session = requests.Session()
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
url = "https://www.youtube.com/"

filterdomains=["google.com","bing.com","youtube.com","facebook.com","line.me","sharepoint.com","taobao.com","shopee.tw"]

data = session.get(url, headers=headers)

# if data.url == url:
    # print("錯誤的")


test = normalize('NFKC', url).encode('ascii', 'ignore').decode('ascii').strip()
print(test)