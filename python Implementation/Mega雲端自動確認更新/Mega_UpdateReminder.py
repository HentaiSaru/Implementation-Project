from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tkinter import messagebox
from selenium import webdriver
from lxml import etree
import pandas as pd
import threading
import random
import socket
import queue
import time
import json
import ast
import os
import re
dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir)

"""
Versions 1.0

[+] 多網址支援
[+] 可多線程運作

BUG
[!] 當網路有問題 或 使用無頭時 有時候會卡住

使用說明
在創建的json檔案中輸入Mega的網址
將該程式使用工作排程器使用
就可以定期檢測是否有更新

使用注意!!
因為是多線程同時作業
沒有特別作處理 因此延遲別設置太短
會出現數據錯亂
"""

class BasicSettings:
    def __init__(self):
        self.verify = r'^.{8}#.{22}$'
        self.Key = {}
        self.url = []

    def ReadKey(self):
        try:
            with open("Mega.json", "r") as f:
                self.Key = json.load(f)
            self.HandleUrl()
        except:
            messagebox.showerror("沒有找到設置", "當前路徑不存在Mega.json\n已在當前目錄下創建\n請填入網址 (不限制數量)")
            self.CreateSettings()

    def HandleUrl(self):
        KeyList = self.Key["MegaUrl"]
        for key in KeyList:
            if re.match(self.verify, key.split('/')[-1]):
                self.url.append(key)
            else:
                print(f"該連結為錯誤的格式: {key}")

    def CreateSettings(self):
        Format = {
            "MegaUrl":["...","...","..."]  
        }
        OutFormat = json.dumps(Format, indent=4 , separators=(',',': '))
        with open("Mega.json", "w") as f:
            f.write(OutFormat)

settings = BasicSettings()

class DataProcessing:
    def __init__(self):
        self.data = {}
        self.state = None

    def ReadInformation(self,SaveName):
        try:
            df = pd.read_csv(f'{SaveName}.csv').applymap(ast.literal_eval).apply(lambda x: x.tolist())
            self.data = df.to_dict(orient='index')[0]
            self.state = True
        except:
            self.state = False
            pass

    def Comparison(self,SaveName,AllData,url):
        Information = pd.json_normalize(AllData, sep='')
        self.ReadInformation(SaveName)

        if self.state:
            if self.data == AllData:
                print("未發現更新")
                #messagebox.showinfo("沒有新資訊",f"未發現更新")
                pass
            else:
                Information.to_csv(f'{SaveName}.csv', index=False)
                choose = messagebox.askquestion("發現更新", f"發現{SaveName}有新的內容\n是否跳轉到該網頁",parent=None)
                if choose == "yes":
                    os.system(f"start {url}")
        else:
            Information.to_csv(f'{SaveName}.csv', index=False)
            messagebox.showinfo("首次創建",f"沒有可比對數據\n為{SaveName}創建新的數據",parent=None)
SaveData = DataProcessing()         

class RequestData:
    settings.ReadKey()

    def __init__(self):
        self.Header = 'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
        self.AllData = {}
        self.port = 1024
        self.count = 0
        self.SaveName = ""
        self.Work = queue.Queue()
        
    def RandomPort(self):
        self.count += 1
        if self.port <= 65535:
            if self.count == 1:
                port = random.randint(self.port, self.port*1.5)
            elif self.count > 1:
                self.port *= 1.5 + 1
                port = random.randint(self.port, self.port*1.5)
        else:port = random.randint(1024,65535)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) == 0:
                return self.RandomPort()
        return port

    def add(self):
        Settings = Options()
        Settings.add_argument(self.Header)
        Settings.add_argument("--headless")
        Settings.add_argument('--no-console')
        Settings.add_argument('--log-level=3')
        Settings.add_argument('--start-maximized')
        Settings.add_argument('--disable-notifications')
        Settings.add_argument('--disable-popup-blocking')
        Settings.add_argument('--ignore-certificate-errors') 
        Settings.add_experimental_option('useAutomationExtension', False)
        Settings.add_argument(f"--remote-debugging-port={self.RandomPort()}")
        Settings.add_experimental_option('excludeSwitches', ['enable-logging'])
        return Settings

    def GetData(self,url):
        Megadriver = webdriver.Chrome(options=self.add())
        Megadriver.get(url)
        
        FileName = WebDriverWait(Megadriver,60).until(EC.element_to_be_clickable((By.XPATH,"//span[@class='not-loading selectable-txt']"))).text

        time.sleep(1)

        tree = etree.fromstring(Megadriver.page_source, etree.HTMLParser())

        self.AllData.clear()

        for search in tree.xpath("//table[@class='grid-table table-hover fm megaListContainer v-fname v-size v-type v-timeAd v-extras']"):

            NameTag = search.xpath(".//div[@class='arrow name label sprite-fm-mono icon-dropdown desc']/text()")[0]
            self.AllData[FileName+NameTag] = search.xpath(".//span[@class='tranfer-filetype-txt']/text()")

            SizeTag = search.xpath(".//div[@class='arrow size sprite-fm-mono icon-dropdown']/text()")[0]
            self.AllData[FileName+SizeTag] = search.xpath(".//td[@class='size']/text()")

            TypeTag = search.xpath(".//div[@class='arrow type sprite-fm-mono icon-dropdown']/text()")[0]
            self.AllData[FileName+TypeTag] = search.xpath(".//td[@class='type']/text()")

            FinalTaf = search.xpath(".//div[@class='arrow mtime sprite-fm-mono icon-dropdown']/text()")[0]
            self.AllData[FileName+FinalTaf] = search.xpath(".//td[@class='time md']/text()")

            self.SaveName = re.sub(r'[<>:"/\\|?*]', '', FileName)

            self.Work.put((self.SaveName,self.AllData,url))

        Megadriver.quit()
Data = RequestData()

def WorkOrder():
    count = 0

    while True:
        time.sleep(0.1)

        if not Data.Work.empty():
            data = Data.Work.get()
            SaveData.Comparison(data[0],data[1],data[2])

        if threading.active_count() == 2:
            count += 1
        else:count = 0

        if count == 10:
            os._exit(0)

if __name__ == "__main__":
    threading.Thread(target=WorkOrder).start()
    for url in settings.url:
        threading.Thread(target=Data.GetData,args=(url,)).start()
        time.sleep(1)