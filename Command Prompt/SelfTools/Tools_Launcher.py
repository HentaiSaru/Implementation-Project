from packaging.version import Version as v
from requests.exceptions import SSLError
from tkinter import messagebox
from datetime import datetime
from tqdm import tqdm
import subprocess
import requests
import socket
import time
import os

""" Versions 1.0.2

- 檢測工具

1. 直接運行就好了 (自動下載)
2. 有更新會自動更新

"""
class Read_web_page:
    def __init__(self, CacheName, CheckLink):
        self.URL = CheckLink
        #self.Location = os.path.join(os.path.expanduser("~"), rf"AppData\Local\Temp\{CacheName}.bat")
        self.Location = rf"{os.environ["TEMP"]}{CacheName}.bat"
        
        self.connection = False

        self.content = None

        self.Web_Version = None
        self.Web_LastEditTime = None

        self.Local_Version = None
        self.Local_LastEditTime = None

    @staticmethod
    def check_internet_connection():
        try:
            socket.create_connection(("www.github.com", 80))
            return True
        except (socket.error, OSError):
            return False

    def Network_request(self):
        reques = requests.get(self.URL)
        if reques.status_code == 200:
            self.connection = True
        self.content = reques.text.split('\n')

        date_processing = self.content[1].split(" ")
        date_processing = f"{date_processing[3]} {date_processing[4]}"

        self.Web_Version = self.content[0].split(" ")[3]
        self.Web_LastEditTime = datetime.strptime(date_processing, "%Y/%m/%d %H:%M")

    def Local_request(self):
        data_box = []
        with open(self.Location ,"r", encoding="utf-8") as f:
            data_box.append(f.readlines())

        date_processing = data_box[0][1].split(" ")
        date_processing = f"{date_processing[3]} {date_processing[4]}"

        self.Local_Version = data_box[0][0].split(" ")[3]
        self.Local_LastEditTime = datetime.strptime(date_processing, "%Y/%m/%d %H:%M")

    def Write_cache(self):
        with open(self.Location, "w", encoding="utf-8") as f:
            for content in self.content:
                f.write(content + "\n")

    def Enable_Tool(self):
        try:
            if self.check_internet_connection():
                self.Network_request()

                if os.path.exists(self.Location):
                    self.Local_request()

                    if v(self.Web_Version) > v(self.Local_Version) or self.Web_LastEditTime > self.Local_LastEditTime:
                        with open(self.Location, "w", encoding="utf-8") as f:
                            for text in tqdm(self.content.items(), ncols=80, desc="更新", bar_format="{l_bar}{bar}"):
                                f.write(text + "\n")
                                time.sleep(0.001)
                else:
                    self.Write_cache()

                subprocess.Popen(self.Location, shell=True)
            else:
                messagebox.showerror("連線失敗", "請確認網路連線\n嘗試無更新驗證運行", parent=None)

                if os.path.exists(self.Location):
                    subprocess.Popen(self.Location, shell=True)
                else:
                    messagebox.showerror("嘗試失敗", "請重新連接網路後運行", parent=None)
        except IndexError:
            if os.path.exists(self.Location) and self.connection:
                os.remove(self.Location)
                self.Enable_Tool()
            else:
                messagebox.showerror("連線失敗", "請下載最新版本啟動器", parent=None)
        except SSLError:
            messagebox.showerror("連線失敗", "錯誤的連線憑證", parent=None)
        except Exception:
            messagebox.showerror("異常狀況", "發生了異常無法運行", parent=None)

if __name__ == "__main__":
    print("更新檢測...")
    read = Read_web_page(
        "r93c440ou9",
        "https://raw.githubusercontent.com/TenshinoOtoKafu/Implementation-Project/Main/Command%20Prompt/SelfTools/Tools.bat"
    )
    read.Enable_Tool()