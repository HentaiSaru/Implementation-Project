from concurrent.futures import *
from lxml import etree
import threading
import keyboard
import requests
import random
import time
import os

class UrlGenerator:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
        self.RandomBox = [[65,90],[97,122],[48,57],[[65,90],[97,122]],[[65,90],[97,122],[48,57]]]
        self.build_status = True

        self.DomainName = None
        self.CharNumber = None
        self.GeneratedNumber = None
        self.CharFormat = None
        self.Tail = None
        self.DeBug = None

        self.SaveBox = []

    def get_data(self,url):
        request = self.session.get(url, headers=self.headers)
        return etree.fromstring(request.content , etree.HTMLParser())
    
    def save_cvs(self):
        Lsave = len(self.SaveBox)
        with open("可用URL.csv", "w" , encoding="utf-8") as f:
            for index , data in enumerate(self.SaveBox):
                if index == Lsave -1:
                    f.write(data.strip())
                else:
                    f.write(data.strip() + "\n")

    def generate_settin(self, domain: str, charnumber: int, generatednumber: int, charformat: int = 0, tail: str = None, debug: bool= False):
            """
            >>> 必傳參數
            * domain 就是網址域名
            * charnumber 是要生成的隨機數 , 數量(也就是域名後要跟幾個字符)
            * generatednumber 是總共要生成的網址數量
            >>> 選擇傳遞
            * charformat 填寫 0 ~ 4 (0英文(大), 1英文(小), 2(數字), 3英文(大+小), 4英文(大+小)+數字)
            * tail 要在生成網址最後加上得符號
            """
            try:
                self.DomainName = domain
                self.CharNumber = charnumber
                self.GeneratedNumber = generatednumber
                self.DeBug = debug

                if charformat >= 0 and charformat <= 4:
                    self.CharFormat = charformat
                else:
                    print("charformat 的範圍是 0 ~ 4")
                    raise Exception()

                if tail != None:
                    self.Tail = tail
                else:
                    self.Tail = ""
            except:
                os._exit(0)

    def generator(self):
        try:
            Format = self.RandomBox[self.CharFormat]
            threading.Thread(target=self.Forced_stop).start()

            with ThreadPoolExecutor(max_workers=100) as executor:

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

                    executor.submit(self.Reurlcc_checking , link)
                    time.sleep(0.01)

            save = threading.Thread(target=self.save_cvs)
            save.start()
            save.join()
            print("生成完畢...")

            os._exit(0)

        except:
            print("請先使用 generate_settin() 進行設置後 , 再進行生成")

    def Reurlcc_checking(self,link):
        try:
            tree = self.get_data(link)
            data = tree.xpath("//div[@class='col-md-4 text-center mt-5 mb-5']/span/text()")
            title = data[1].replace(","," ")

            self.SaveBox.append(f"{title},{link.split('+')[0]}")
        except:
            pass

    def Forced_stop(self):
        print("在中途按下 ALT + S 可以強制停止程式 , 並輸出結果")
        while True:
            if keyboard.is_pressed("alt+s"):
                self.build_status = False
                while keyboard.is_pressed("alt+s"):
                    pass
            time.sleep(0.05)

if __name__ == "__main__":
    url = UrlGenerator()
    url.generate_settin(
        domain = "https://reurl.cc/",
        charnumber = 6,
        generatednumber = 500,
        charformat = 4,
        tail= "+",
        debug=False
    )
    url.generator()

"""
正確 : https://pse.is/52ucfr
錯誤 : https://pse.is/51ucfr

正確 : https://ppt.cc/fhgP4x
錯誤 : https://ppt.cc/dhaP3x

正確 : https://tinyurl.com/preview/mukr6h7p
錯誤 : https://tinyurl.com/preview/mukr8h7p

正確 : https://rb.gy/zay86
錯誤 : https://rb.gy/zay76

"""