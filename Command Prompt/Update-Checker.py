from packaging.version import Version
from tqdm import tqdm
import subprocess
import requests
import sys
import os

class Check_for_updates:
    def __init__(self):
        # 將 .bat 打包在 exe 內 , 需要使用這邊 , 並且結束後要寫一個 input()
        # Location = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(sys.argv[0]))
        # self.Location = os.path.join(Location,"System-Cleaning.bat")

        self.Location = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),"System-Cleaning.bat")

        # 倉庫網址
        self.url = "https://raw.githubusercontent.com/TenshinoOtoKafu/Implementation-Project/Main/Command%20Prompt/System-Cleaning.bat"
        self.text = None
        self.Web_Version = None
        self.Local_Version = None

    def Get_web(self):
        reques = requests.get(self.url)
        self.text = reques.text.split('\n')
        self.Web_Version = self.text[0].split(" ")[3]

    def Get_local(self):

        with open(self.Location ,"r",encoding="utf-8") as f:
            self.Local_Version = f.readline().split(" ")[3]

    def Update_Comparison(self):

        if Version(self.Web_Version) > Version(self.Local_Version):
            pbar = tqdm(total=len(self.text),ncols=80,desc="更新 ",bar_format="{l_bar}{bar}")
            with open(self.Location,"w",encoding="utf-8") as f:
                for text in self.text:
                    f.write(text + "\n")
                    pbar.update(1)
                pbar.clear()
            subprocess.call(self.Location, shell=True)
        else:
            subprocess.call(self.Location, shell=True)

if __name__ == "__main__":

    check = Check_for_updates()
    check.Get_web()
    check.Get_local()
    check.Update_Comparison()