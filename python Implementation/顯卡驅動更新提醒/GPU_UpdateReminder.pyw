from tkinter import messagebox
from lxml import etree
import requests
import GPUtil
import re
import os

"""
Versions 1.0.2

1. 修改宣告排版
2. 更新請求頭 與 部份處理邏輯
3. 修改下載連結直接取得 檔案

"""
class Check:
    def __init__(self, CheckUrl):
        self.Space = " " * 8
        self.Session = requests.Session()
        self.GpuName = self.GPUDriver = self.GetVersion = self.ReleaseTime = None
        self.Request_info = lambda Url=None: etree.HTML(
            self.Session.get(
                Url or CheckUrl, # 如果 Url 是空的就取 CheckUrl
                headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}
            ).text
        )
        self.Analyze_info()

    # 請求下載資訊
    def Download_info(self, tree):
        tree = self.Request_info("https:{}".format(tree.xpath("//tr[@id='driverList']//a")[0].get("href")))
        return "https://tw.download.nvidia.com{}".format(re.search(r"\?url=(.*?\.exe)", tree.xpath("//a[@id='lnkDwnldBtn']")[0].get("href")).group(1))

    # 解析獲取資訊
    def Analyze_info(self):
        tree = self.Request_info()

        # 顯卡資訊取得
        for Information in GPUtil.getGPUs():
            self.GpuName = Information.name.lstrip("NVIDIA GeForce")
            self.GPUDriver = Information.driver

        # 獲取更新的驅動資訊
        VersionNumber = tree.xpath("//tr[@id='driverList']//td[@class='gridItem']/text()")
        VersionNumber = [re.sub(r"[\n\r\t]+", "", d) for d in VersionNumber if d.strip()]

        # 驅動版本號
        self.GetVersion = VersionNumber[0]

        # 將獲取的驅動發布時間反轉處理
        NewReleaseTime = VersionNumber[1].split(".")[::-1]
        self.ReleaseTime = f"{NewReleaseTime[0]}.{NewReleaseTime[1]}.{NewReleaseTime[2]}"

        # 進行比對更新
        self.Comparison_info(tree)

    # 比對版本
    def Comparison_info(self, tree):
        if float(self.GPUDriver) < float(self.GetVersion):

            choose = messagebox.askquestion(
                "發現新版本",
                f"顯卡型號: {self.GpuName}\n舊驅動版本: {self.GPUDriver}\n\n新驅動版本:{self.GetVersion}\n發布日期:{self.ReleaseTime}\n\n{self.Space}您是否要下載",
                parent=None
            )

            if choose == "yes":
                os.system(f"start {self.Download_info(tree)}")
        else:
            messagebox.showinfo("沒有新版本", f"顯卡型號: {self.GpuName}\n當前驅動: {self.GPUDriver} 是最新版本", parent=None)

if __name__ == "__main__":
    Check("https://www.nvidia.com.tw/Download/processFind.aspx?psid=107&pfid=902&osid=135&lid=6&whql=1&lang=tw&ctk=0&qnfslb=00&dtcid=1")