from packaging.version import Version
from tqdm import tqdm
import subprocess
import requests
import os

""" Versions 1.0.0

- 進階版檢測

1. 直接運行就好了 (自動下載)
2. 有更新會自動更新

"""

class Read_web_page:
    def __init__(self):
        Location = os.path.expanduser("~")
        self.Location = os.path.join(Location,"AppData\Local\\temporary.bat")
        
        self.url = "https://raw.githubusercontent.com/TenshinoOtoKafu/Implementation-Project/Main/Command%20Prompt/System-Cleaning.bat"
        self.content = None
        self.process = None

    def Data_request(self):
        reques = requests.get(self.url)
        self.content = reques.text.split('\n')

    def Write_cache(self):
        self.Data_request()

        with open(self.Location ,"w",encoding="utf-8") as f:
            for content in self.content:
                f.write(content + "\n")

    def Clean_run(self):
        if os.path.exists(self.Location) != True:
            self.Write_cache()
        else:
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

        subprocess.call(self.Location, shell=True)

if __name__ == "__main__":
   read = Read_web_page()
   read.Clean_run()