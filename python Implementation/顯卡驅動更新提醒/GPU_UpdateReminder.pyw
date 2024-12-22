from tkinter import messagebox
import textwrap
import GPUtil
import httpx
import os

"""
Versions 1.0.3

! 簡單的獲取, 不做例外處理

1. 修改資訊排版
2. 更新請求邏輯

"""
class Check:
    def __init__(self, CheckUrl):
        self.Space = " " * 8
        self.Client = httpx.Client(http2=True)

        self.GpuName = self.GPUDriver = None
        self.RemoteVersion = self.ReleaseTime = self.DetailsUrl = self.DownloadUrl = None

        # 獲取一個 Json 數據, 轉成 dict
        self.Request_info = lambda: self.Client.get(
            CheckUrl, headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"}
        ).json()

        self.Analyze_info()

    # 解析獲取資訊
    def Analyze_info(self):
        # 取得線上資訊
        info = self.Request_info()

        # 顯卡資訊取得
        for Information in GPUtil.getGPUs():
            self.GpuName = Information.name.lstrip("NVIDIA GeForce")
            self.GPUDriver = Information.driver

        #! 解析遠端資訊 (不做例外處理)
        downloadInfo = info['IDS'][0]['downloadInfo']
        self.RemoteVersion = downloadInfo['Version']
        self.ReleaseTime = downloadInfo['ReleaseDateTime']
        self.DetailsUrl = f"https://www.nvidia.com/zh-tw/drivers/details/{downloadInfo['ID']}/"
        self.DownloadUrl = downloadInfo['DownloadURL']

        # 呼叫比對
        self.Comparison_info()

    # 比對版本
    def Comparison_info(self):
        if float(self.GPUDriver) < float(self.RemoteVersion):

            display_info = textwrap.dedent(f"""
            \r顯卡型號: {self.GpuName}

            \r舊驅動版本: {self.GPUDriver}
            \r新驅動版本: {self.RemoteVersion}
            \r發布日期: {self.ReleaseTime}
            \r驅動詳情: {self.DetailsUrl}

            \r您是否要下載?
            """)

            choose = messagebox.askquestion("發現新版本", display_info, parent=None)

            if choose == "yes":
                os.system(f"start {self.DownloadUrl}")
        else:
            display_info = textwrap.dedent(f"""
            \r顯卡型號: {self.GpuName}

            \r當前驅動版本: {self.GPUDriver}
            \r發布日期: {self.ReleaseTime}
            \r驅動詳情: {self.DetailsUrl}
            """)
            
            messagebox.showinfo("已是最新版本", display_info, parent=None)

if __name__ == "__main__":
    Check("https://gfwsl.geforce.com/services_toolkit/services/com/nvidia/services/AjaxDriverService.php?func=DriverManualLookup&psid=120&pfid=942&osID=57&languageCode=1028&beta=0&isWHQL=1&dch=1&sort1=1&numberOfResults=1")