import packaging.version as Ver
import requests
import os

class Check_for_updates:
    def __init__(self):
        # 倉庫網址
        self.url = "https://raw.githubusercontent.com/TenshinoOtoKafu/Implementation-Project/Main/Command%20Prompt/System-Cleaning.bat"
        self.Web_Version = None
        self.Local_Version = None

    def Get_web(self):
        reques = requests.get(self.url)
        text = reques.text.split('\n')
        self.Web_Version = text[0].split(" ")[3]

    def Get_local(self):
        # 確保找當前路徑下
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        with open("System-Cleaning.bat","r",encoding="utf-8") as f:
            self.Local_Version = f.readline().split(" ")[3]

    def Update_Comparison(self):

        if float(self.Web_Version) > float(self.Local_Version):
            print("需更新")
        else:
            print("無需更新")

if __name__ == "__main__":
    check = Check_for_updates()
    check.Get_web()
    check.Get_local()
    check.Update_Comparison()