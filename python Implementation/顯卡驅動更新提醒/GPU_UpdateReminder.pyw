from tkinter import messagebox
from lxml import etree
import requests
import GPUtil
import re
import os

"""
Versions 1.0

[+] 顯卡驅動檢測
[+] 抓取最新版本
[+] 更新提醒彈窗
"""
class basic:
    def __init__(self,RequestUrl):
        self.GpuUrl = RequestUrl
    
class Crawl:
    def __init__(self,GpuUrl):
        self.Session = requests.Session()
        self.Header = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
        self.Url = GpuUrl
        self.Space = " " * 6
        self.Download = None
        self.GPUDriver = None
        self.GetVersion = None
        self.ReleaseTime = None
        self.GPU = GPUtil.getGPUs()

    def GetData(self):
        for Information in self.GPU:self.GPUDriver = Information.driver
        Data = self.Session.get(self.Url,headers=self.Header)
        tree = etree.fromstring(Data.content, etree.HTMLParser())
        
        VersionNumber = tree.xpath("//tr[@id='driverList']//td[@class='gridItem']/text()")
        VersionNumber = [re.sub(r'[\n\r\t]+','',d) for d in VersionNumber if d.strip()]

        self.GetVersion = VersionNumber[0]

        # 將獲取的時間反轉處理
        NewReleaseTime = VersionNumber[1].split(".")[::-1]
        self.ReleaseTime = f"{NewReleaseTime[0]}.{NewReleaseTime[1]}.{NewReleaseTime[2]}"
        
        self.Download = "https:{}".format(tree.xpath("//tr[@id='driverList']//a")[0].get('href'))

        self.Comparison()

    def Comparison(self):

        if float(self.GPUDriver) < float(self.GetVersion):
            # 置頂窗口
            choose = messagebox.askquestion("發現新版本", 
            f"您當前的驅動版本:{self.GPUDriver}\n目前有新版本:{self.GetVersion}\n發布日期:{self.ReleaseTime}\n\n{self.Space}您是否要下載",parent=None)
            if choose == "yes":
                os.system(f"start {self.Download}")
        else:
            messagebox.showinfo("沒有新版本",f"您當前的驅動{self.GPUDriver}是最新版本",parent=None)
        
if __name__ == "__main__":
    
    Run = Crawl(basic("https://www.nvidia.com.tw/Download/processFind.aspx?psid=107&pfid=902&osid=135&lid=6&whql=1&lang=tw&ctk=0&qnfslb=00&dtcid=1").GpuUrl)
    Run.GetData()