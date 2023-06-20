from unicodedata import normalize
from concurrent.futures import *
from urllib.parse import *
from lxml import etree
import threading
import keyboard
import requests
import random
import json
import time
import os

"""
可隨機生成縮網址的程式

目前支援類型
reurl.cc
ppt.cc

功能

[+] 自訂生成格式
[+] 自訂生成數量
[+] 選擇排除網域

! 排除網域的功能 , 並不是 100 % 成功的
原本採取 queue 去處理
這能保證數據的處理
但是速度會慢很多
因此為了速度捨去了處理準確性
(開啟二次驗證精準度會提高)

"""

class UrlGenerator:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
        self.RandomBox = [[65,90],[97,122],[48,57],[[65,90],[97,122]],[[65,90],[97,122],[48,57]]]
        self.SupportDomain = ["reurl.cc","ppt.cc"]
        # 判斷類變數
        self.build_status = True
        self.filter_trigger = False
        self.support = None
        # 設置類變數
        self.Tail = None
        self.DeBug = None
        self.DomainName = None
        self.CharNumber = None
        self.CharFormat = None
        self.FilterDomains = None
        self.GeneratedNumber = None
        self.SecondVerification = None
        # 保存類變數
        self.SuccessCount = 0
        self.SaveBox = {}

    def get_data(self,url):
        request = self.session.get(url, headers=self.headers)
        return etree.fromstring(request.content , etree.HTMLParser())
    
    def get_conversion_data(self,url):
        request = self.session.get(url, headers=self.headers)
        tree = etree.fromstring(request.content , etree.HTMLParser())
        if request.status_code == 200:
            try:
                title = tree.xpath("//title/text()")[0]
            except:
                title = "無取得標題"
            return request.url , title
        else:
            return False , request.status_code
    
    def save_json(self):
        if len(self.SaveBox) > 0:
            with open("可用網址.json" , "w" , encoding="utf-8") as file:
                file.write(json.dumps(self.SaveBox, indent=4, separators=(',',':')))

    def generate_settin(self, 
            domain: str,
            charnumber: int,
            generatednumber: int,
            charformat: int = 0,
            tail: str = None,
            secondverification: bool = False,
            filterdomains: list = [],
            debug: bool= False
        ):
            """
            >>> 必傳參數
            * domain 就是網址域名
            * charnumber 是要生成的隨機數 , 數量(也就是域名後要跟幾個字符)
            * generatednumber 是總共要生成的網址數量
            >>> 選擇傳遞
            * charformat 填寫 0 ~ 4 (0英文(大), 1英文(小), 2(數字), 3英文(大+小), 4英文(大+小)+數字)
            * tail 要在生成網址最後加上得符號
            * SecondVerification 啟用時會對生成的網址 , 進行二次驗證是否可以用 , 排除 404 (整體速度會減慢)
            * FilterDomains 將要排除的網域名稱傳遞 , 就會將獲取的網址中 , 包含該網域的排除
            * debug 會顯示生成的網址樣式
            """
            try:
                self.DeBug = debug
                self.DomainName = domain
                self.CharNumber = charnumber
                self.FilterDomains = filterdomains
                self.GeneratedNumber = generatednumber
                self.SecondVerification = secondverification

                self.support = self.SupportDomain.index(urlparse(domain).netloc) # 域名解析與判斷

                if charformat >= 0 and charformat <= 4: # 判斷生成格式設置 , 是否符合規範
                    self.CharFormat = charformat
                else:
                    print("charformat 的範圍是 0 ~ 4")
                    raise Exception()
                
                if len(self.FilterDomains) > 0: # 判斷是否使用排除
                    self.filter_trigger = True

                if tail != None:
                    self.Tail = tail
                else:
                    self.Tail = ""
            except:
                os._exit(0)

    def generator(self):
        try:
            Format = self.RandomBox[self.CharFormat]

            stop = threading.Thread(target=self.Forced_stop)
            stop.daemon = True
            stop.start()

            save = threading.Thread(target=self.save_json)

            with ThreadPoolExecutor(max_workers=300) as executor:
                while len(self.SaveBox) < self.GeneratedNumber and self.build_status:
                    gen_char = ""

                    for _ in range(self.CharNumber):
                        if self.CharFormat == 3:
                            mat = Format[random.randint(0,1)]
                        elif self.CharFormat == 4:
                            mat = Format[random.randint(0,2)]
                        else:
                            mat = Format
                        gen_char += chr(random.randint(mat[0],mat[1]))

                    link = f"{self.DomainName}{gen_char}{self.Tail}"
                    if self.DeBug:
                        print(link)
                    
                    executor.submit(self.Data_Processing, link)
                    time.sleep(0.008)

            save.start()
            save.join()
            print("生成完畢...")

        except:
            print("請先使用 generate_settin() 進行設置後 , 再進行生成")

    def Data_Processing(self,link):
        try:
            if self.support == 0:
                tree = self.get_data(link)
                url = unquote(tree.xpath("//span[@class='lead']/text()")[0])
                title = tree.xpath("//div[@class='col-md-4 text-center mt-5 mb-5']/span/text()")[1].replace(","," ")
            elif self.support == 1:
                url = unquote(self.get_url(link))
                if url.find(self.SupportDomain[1]) != -1:
                    raise Exception()
                else:
                    title = url
            
            if self.SecondVerification:
                url , title = self.get_conversion_data(url)
                # 測試雙重驗證確保精準度
                if url == False or title != 200:
                    raise Exception()
            
            if self.filter_trigger:
                for domain in self.FilterDomains:
                    if url.find(domain) != -1:
                        raise Exception()
            
            self.SaveBox[link.split('+')[0]] = normalize('NFKC', title).encode('ascii', 'ignore').decode('ascii').strip()
            self.SuccessCount += 1
            print(f"成功生成總數 : {self.SuccessCount}")
        except:
            pass

    def Forced_stop(self):
        print("在中途按下 ALT + S 可以強制停止程式 , 並輸出結果")
        while True:
            if keyboard.is_pressed("alt+s"):
                self.build_status = False
                while keyboard.is_pressed("alt+s"):
                    pass
            time.sleep(0.03)

if __name__ == "__main__":
    url = UrlGenerator()

    url.generate_settin(
        domain = "https://reurl.cc/",
        generatednumber = 100,
        charnumber = 6,
        charformat = 4,
        tail= "+",
        secondverification=True,
        filterdomains=["google.com","bing.com","youtube.com","facebook.com","line.me","sharepoint.com","taobao.com","shopee.tw","wikipedia.org"],
    )

    # url.generate_settin(
    #     domain = "https://ppt.cc/",
    #     generatednumber = 10,
    #     charnumber = 6,
    #     charformat = 3,
    #     secondverification=True,
    #     filterdomains=["google.com","bing.com","youtube.com","facebook.com","line.me","sharepoint.com","taobao.com","shopee.tw"],
    # )

    url.generator()

""" 待開發

正確 : https://pse.is/52ucfr
錯誤 : https://pse.is/51ucfr

正確 : https://tinyurl.com/preview/mukr6h7p
錯誤 : https://tinyurl.com/preview/mukr8h7p

正確 : https://rb.gy/zay86
錯誤 : https://rb.gy/zay76

"""