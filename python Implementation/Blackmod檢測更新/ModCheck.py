from packaging.version import Version
from lxml import etree
import requests
import os
import re
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class blackmod:
    def __init__(self,url=None):
        self.url = url
        self.save_box = []

    def single_url(self):
        Crawling(self.url)

    def list_url(self):
        for url in self.url:
            Crawling(url)
    
Session = requests.Session()
class Crawling:
    def __init__(self,url):
        self.header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
        self.tree = etree.fromstring(Session.get(url,headers=self.header).content,etree.HTMLParser())
        self.title = self.tree.xpath("//span[@id='content_app']/text()")[0]
        self.version = self.tree.xpath("//td/text()")[0]
        self.link = self.tree.xpath("//p[@class='free-download mirror-link']/a")[0].get("href")
        self.data = None
        self.Comp = None
        self.GetData()

    def GetData(self):
        self.data = f"{self.title}@v={self.version}"
        processing.Compare(self.data,self.title,self.version,self.link)

class dataprocessing:
    def __init__(self):
        self.exclude = r'^Game APK: | Hack Mod for ANDROID$'
        self.SaveBox = []
        self.titlebox = []
        self.versionbox = []
        self.Record = None
        self.ReadRecord()
        self.result = []

    def ReadRecord(self):
        try:
            with open("Temporary", "rb") as f:
                self.Record = f.read().decode('utf-8').split("\n")
            
            for take in self.Record:
                self.titlebox.append(take.split("@v=")[0].strip())
                self.versionbox.append(take.split("@v=")[1].strip())
        except:
            with open("Temporary", "wb") as f:f.write("空數據創建@v=1.0.0".encode('utf-8'))

    def Compare(self,NewData,title,version,link):

        try:
            if title not in self.titlebox:

                self.SaveBox.append(NewData)

                result_message = f"- 模組名稱: {re.sub(self.exclude,'',title)}\n- 無比對數據 (添加新數據)"
                self.result.append(result_message)

            else:
                for index in range(len(self.Record)):
                    if title == self.titlebox[index]:
                        if Version(version) <= Version(self.versionbox[index]):

                            self.SaveBox.append(self.Record[index].strip())

                            result_message = f"- 模組名稱: {re.sub(self.exclude,'',title)}\n- 當前版本: {self.versionbox[index]}\n- 無須更新"
                            self.result.append(result_message)

                        elif Version(version) > Version(self.versionbox[index]):

                            self.SaveBox.append(NewData)

                            result_message = f"- 模組名稱: {re.sub(self.exclude,'',title)}\n- 更新版本: {packaging.version.Version(version)}\n- 更新連結: {link}"
                            self.result.append(result_message)

            with open("Temporary", "wb") as f:
                for i , item in enumerate(self.SaveBox):
                    if i == len(self.SaveBox) - 1:
                        f.write(f"{item}".encode('utf-8'))
                    else:
                        f.write(f"{item}\n".encode('utf-8'))
        except:
            with open("Temporary", "wb") as f:f.write(f"{NewData}".encode('utf-8'))

    def Result(self):
        return self.result
processing = dataprocessing()

def run(enter):
    if isinstance(enter,list):
        blackmod(enter).list_url()
    elif isinstance(enter,str):
        blackmod(enter).single_url()