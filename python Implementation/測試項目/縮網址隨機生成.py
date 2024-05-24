from unicodedata import normalize
from concurrent.futures import *
from multiprocessing import *
from urllib.parse import *
from lxml import etree
import threading
import keyboard
import requests
import random
import string
import json
import time
import os

"""
可隨機生成網址的程式
(基本上網址後為 6 個上下的 , 英 大+小 + 數字 , 都可以嘗試)
再更多字元的機率就很低了 , 雖然還是有可能 , 但就是等吧

功能

[+] 自訂生成格式
[+] 自訂生成數量
[+] 選擇排除網域

(有特別處理驗證可用性)
! 支援網域 (其他的也是可以 , 只是可用性就不能保證)
reurl.cc
ppt.cc
files.catbox.moe

! 排除網域的功能 , 並不是 100 % 成功的
原本採取 queue 去處理
這能保證數據的處理
但是速度會慢很多
因此為了速度捨去了處理準確性
(開啟二次驗證精準度會提高,但處理速度會變慢)

"""

class UrlGenerator:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        # 舊版隨機盒 self.RandomBox = [[65,90],[97,122],[48,57],[[65,90],[97,122]],[[65,90],[97,122],[48,57]]]
        self.RandomBox = [string.ascii_uppercase, string.ascii_lowercase, string.digits, string.ascii_letters, string.ascii_letters+string.digits]
        self.SupportDomain = ["reurl.cc","ppt.cc","files.catbox.moe"]
        # 判斷類變數
        self.build_status = True
        self.support = None
        # 設置類變數
        self.Tail = None
        self.DeBug = None
        self.DomainName = None
        self.CharNumber = None
        self.CharFormat = None
        self.FilterDomains = None
        self.GeneratedNumber = None
        self.Whitelistdomains = None
        self.SecondVerification = None
        # 保存類變數
        self.SuccessCount = 0
        self.SaveBox = {}
        # 宣告
        self.save = threading.Thread(target=self.save_json)

    def get_data(self,url):
        request = self.session.get(url, headers=self.headers)
        return etree.HTML(request.text), request.url

    def get_conversion_data(self, url):
        request = self.session.head(url, headers=self.headers)
        status = request.status_code
        if status == 200:
            return request.url, status
        else:
            return False, status

    def save_json(self):
        if len(self.SaveBox) > 0:
            with open("可用網址.json", "w", encoding="utf-8") as file:
                file.write(json.dumps(self.SaveBox, indent=4, separators=(",", ":")))

    def generate_settin(self, 
            domain: str,
            charnumber: int,
            generatednumber: int,
            charformat: int = 0,
            tail: str = None,
            secondverification: bool = False,
            filterdomains: list = [],
            Whitelistdomains: list = [],
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
            * secondVerification 啟用時會對生成的網址 , 進行二次驗證是否可以用 , 排除 404 (整體速度會減慢)
            * filterDomains 將要排除的網域名稱傳遞 , 就會將獲取的網址中 , 包含該網域的排除
            * Whitelistdomains 白名單網域 , 將可以跳過驗證
            * debug 會顯示生成的網址樣式
            """
            try:
                self.DeBug = debug
                self.DomainName = domain
                self.CharNumber = charnumber
                self.FilterDomains = filterdomains
                self.GeneratedNumber = generatednumber
                self.Whitelistdomains = Whitelistdomains
                self.SecondVerification = secondverification

                if charformat >= 0 and charformat <= 4: # 判斷生成格式設置 , 是否符合規範
                    self.CharFormat = charformat
                else:
                    print("charformat 的範圍是 0 ~ 4")
                    raise Exception()

                self.Tail = tail if tail is not None else ""

                try:
                    self.support = self.SupportDomain.index(urlparse(domain).netloc) # 域名解析與判斷
                except:
                    self.support = 9999

            except:
                os._exit(0)

    def generator(self):
        try:
            Format = self.RandomBox[self.CharFormat]
            stop = threading.Thread(target=self.Forced_stop)
            stop.daemon = True
            stop.start()
            
            def gen():
                while len(self.SaveBox) < self.GeneratedNumber and self.build_status:
                    gen_char = "".join(random.choice(Format) for _ in range(self.CharNumber))
                    yield f"{self.DomainName}{gen_char}{self.Tail}"

            with ThreadPoolExecutor(max_workers=(cpu_count() * 30)) as executor:
                for link in gen():
                    executor.submit(self.Data_Processing, link)
                    time.sleep(0.001)

            self.save.start()
            self.save.join()
        except:
            os.system("cls")
            print("請先使用 generate_settin() 進行設置後, 再進行生成")

    def Data_Processing(self, link):
        if self.DeBug:
            print(f"\r{link}", end="", flush=True)

        try:
            # 第一重驗證 (開發支援)
            if self.support == 0:
                tree, C_url = self.get_data(link)
                url = unquote(tree.xpath("//span[@class='lead']/text()")[0])
                title = tree.xpath("//span[@class='text-muted']/text()")[0].replace(","," ")

            elif self.support == 1:
                tree, C_url = self.get_data(link)
                C_url = unquote(C_url)
                # 簡單驗證一下
                if C_url.find(self.SupportDomain[1]) != -1:
                    raise Exception()
                else:
                    url = C_url
                    title = tree.xpath("//title/text()")[0]

            elif self.support == 2:
                url = link
                title = ""
            
            # 進階驗證函數
            def Advanced_verification(url):
                # 將請求回來的的 Url, 請求狀態碼驗證
                if self.SecondVerification:
                    url, status = self.get_conversion_data(url)
                    if not url or status != 200:
                        raise Exception()

                # 域名排除
                if bool(self.FilterDomains):
                    for domain in self.FilterDomains:
                        if url.find(domain) != -1:
                            raise Exception()
                        
            if bool(self.Whitelistdomains):
                for White in self.Whitelistdomains:
                    if url.find(White) == -1:
                        Advanced_verification(url)
            else:
                Advanced_verification(url)

            self.SaveBox[link.split("+")[0]] = normalize("NFKC", title).encode("ascii", "ignore").decode("ascii").strip()
            self.SuccessCount += 1
            print(f"\n成功生成總數 : {self.SuccessCount} [{link.split('+')[0]}]")
        except:
            pass

    def Forced_stop(self):
        print("在中途按下 Ctrl + E 可以強制停止程式 , 並輸出結果 =>")
        keyboard.wait("ctrl+e")

        self.build_status = False
        self.save.start()
        self.save.join()

        print("\n生成完畢...")
        os._exit(1)

if __name__ == "__main__":
    url = UrlGenerator()

    """ ___ 設定檔 ___ """

    url.generate_settin(
        domain = "https://reurl.cc/",
        generatednumber = 10,
        charnumber = 6,
        charformat = 4,
        tail = "+",
        secondverification=True,
        filterdomains=[
            "google.com","bing.com","youtube.com","facebook.com","microsoft.com",
            "line.me","sharepoint.com","taobao.com","shopee.tw","wikipedia.org",
            "udn.com","wikipedia.org","msn.com","shop2000.com","mirrormedia.mg",
            "opdws.fjuh.fju.edu.tw"
        ],
        Whitelistdomains=[
            "mega.nz"
        ], debug = True
    )

    # url.generate_settin(
    #     domain = "https://ppt.cc/",
    #     generatednumber = 10,
    #     charnumber = 6,
    #     charformat = 4,
    #     secondverification=True,
    #     filterdomains=[
    #         "google.com","bing.com","youtube.com","facebook.com","line.me",
    #         "sharepoint.com","taobao.com","shopee.tw"
    #     ],
    # )

    # url.generate_settin(
        # domain = "https://files.catbox.moe/",
        # generatednumber = 10,
        # charnumber = 6,
        # charformat = 4,
        # tail= ".mp4",
        # secondverification=True,
    # )

    """ ___ 主要生成 ____ """

    #? 自動調用開始生成
    url.generator()

    #? 輸入網址測試處理
    # url.Data_Processing("")


""" 待開發

正確 : https://pse.is/52ucfr
錯誤 : https://pse.is/51ucfr

正確 : https://tinyurl.com/preview/mukr6h7p
錯誤 : https://tinyurl.com/preview/mukr8h7p

正確 : https://rb.gy/zay86
錯誤 : https://rb.gy/zay76

"""