from packaging.version import Version
from tkinter import messagebox
from tqdm import tqdm
import subprocess
import requests
import socket
import os
    
class Read_web_page:
    def __init__(self):
        Location = os.path.expanduser("~")
        self.Location = os.path.join(Location,"AppData\Local\\Temp\\self_tools.bat")

        self.url = "https://raw.githubusercontent.com/TenshinoOtoKafu/Implementation-Project/Main/Command%20Prompt/SelfTools/Personally-used.bat"
        self.content = None

    @staticmethod
    def check_internet_connection():
        try:
            socket.create_connection(("www.github.com", 80))
            return True
        except (socket.error, OSError):
            return False
        
    def Data_request(self):
        reques = requests.get(self.url)
        self.content = reques.text.split('\n')
        
    def Write_cache(self):
        self.Data_request()

        with open(self.Location ,"w",encoding="utf-8") as f:
            for content in self.content:
                f.write(content + "\n")

    def Enable_Tool(self):
        try:
            if self.check_internet_connection():
                if os.path.exists(self.Location):
                    self.Data_request()

                    Web_Version = self.content[0].split(" ")[3]

                    with open(self.Location ,"r",encoding="utf-8") as f:
                        Local_Version = f.readline().split(" ")[3]

                    if Version(Web_Version) > Version(Local_Version):
                        pbar = tqdm(total=len(self.content),ncols=80,desc="更新 ",bar_format="{l_bar}{bar}")

                        with open(self.Location,"w",encoding="utf-8") as f:
                            for text in self.content:
                                f.write(text + "\n")
                                pbar.update(1)
                            pbar.clear()
                else:
                    self.Write_cache()

                subprocess.call(self.Location, shell=True)
                
            else:
                messagebox.showerror("連線失敗","請確認網路連線\n嘗試無驗證運行",parent=None)

                if os.path.exists(self.Location):
                    subprocess.call(self.Location, shell=True)
                else:
                    messagebox.showerror("嘗試失敗","請重新連接網路後運行",parent=None)

        except:
            messagebox.showerror("異常!","發生異常無法運行",parent=None)

if __name__ == "__main__":
    read = Read_web_page()
    read.Enable_Tool()