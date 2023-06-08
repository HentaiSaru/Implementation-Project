from tkinter import messagebox
from lxml import etree
import requests
import re
import os

class GetNew:
    def __init__(self):
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
        self.url = "https://cmake.org/files/LatestRelease/"
        self.request = requests.Session()
        self.Fromat = r'[\xa0]|  -'
        self.win64 = r'cmake-.+-windows-x86_64\.msi'

        self.Timestamp = []
        self.Version = []
        self.Date = []

        self.count = 0

    def New(self):
        data = self.request.get(self.url,headers=self.headers)
        tree = etree.fromstring(data.content, etree.HTMLParser())

        for data in tree.xpath("//tr/td/text()"):
            if re.match(self.Fromat,data):
                continue
            else:
                if self.count % 2 == 0: # 只獲取 年-月-日
                    self.Timestamp.append(data.strip().split(" ")[0])
                self.count += 1
        
        for index , data in enumerate(tree.xpath("//tr/td/a/text()")):
            if re.match(self.win64,data):
                self.Version.append(f"https://cmake.org/files/LatestRelease/{data}")
                self.Date.append(self.Timestamp[index-1])

        choose = messagebox.askquestion("最新版本下載", f"發布日期 : {self.Date[-1]}\n\n下載連結{self.Version[-1]}" , parent=None)
        if choose == "yes":
            os.system(f"start {self.Version[-1]}")

if __name__ == "__main__":
    get = GetNew()
    get.New()