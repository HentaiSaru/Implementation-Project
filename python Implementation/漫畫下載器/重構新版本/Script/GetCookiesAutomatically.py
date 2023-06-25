import undetected_chromedriver as uc
import random
import json
import time
import os

class AutomationRequest:
    def __init__(self):
        self.cookie = {}
        self.driver = None
        self.timeout = 0
        self.Settings = uc.ChromeOptions()

    def browser_reset(self):
        """
    !   注意
    *   此重置方法將會關閉 Google 瀏覽器
    *   接著會重裝相關依賴庫
        """
        print("重置中請稍後...")
        # 關閉 Google
        os.system('wmic process where name="chrome.exe" delete >nul 2>&1')
        # 刪除 undetected_chromedriver
        os.system("pip uninstall undetected_chromedriver -y >nul 2>&1")
        # 安裝 undetected_chromedriver
        os.system("pip install undetected_chromedriver >nul 2>&1")
        # 更新 Python 和 pip
        os.system("python.exe -m pip install --upgrade pip >nul 2>&1")
        os.system("pip install --upgrade setuptools >nul 2>&1")
        os.system("pip install --upgrade wheel >nul 2>&1")
        print("重置完成...")

    def __Setting_Options(self):
        self.Settings.add_argument("--headless")
        self.Settings.add_argument("--incognito")
        self.Settings.add_argument('--no-sandbox')
        self.Settings.add_argument('--log-level=3')
        self.Settings.add_argument('--no-first-run')
        self.Settings.add_argument('--disable-infobars')
        self.Settings.add_argument("--disable-extensions")
        self.Settings.add_argument('--no-service-autorun')
        self.Settings.add_argument("--disable-file-system")
        self.Settings.add_argument("--disable-geolocation")
        self.Settings.add_argument("--disable-web-security")
        self.Settings.add_argument('--password-store=basic')
        self.Settings.add_argument('--disable-notifications')
        self.Settings.add_argument("--disable-popup-blocking") 
        self.Settings.add_argument('--no-default-browser-check')
        self.Settings.add_argument("--profile-directory=Default")
        self.Settings.add_argument("--ignore-certificate-errors")
        self.Settings.add_argument("--disable-plugins-discovery")
        self.Settings.add_argument('--remote-debugging-address=0.0.0.0')
        self.Settings.add_argument('--disable-blink-features=AutomationControlled')
        self.Settings.add_argument(f"--remote-debugging-port={random.randint(1024,65535)}")
        return self.Settings
    
    def Request_Cookie(self,url: str,json: str):
        """
    >>> 請求參數
    *   url  請求的連結
    *   json 請求成功後創建的 .json 名稱 (不需要打.json)
    
    *   回傳 True / False 為請求成功狀態
    *   預設有 15 秒的超時時間 , 超過這時間沒有請求到 , 將會回傳 False
    *   [請求成功後的 , 錯誤操作指令警告 , 待方法修復]
        """
        print("嘗試獲取Cookie...")
        try:
            if json.find(".json") != -1:
                json = json.rsplit(".", 1)[0]

            self.driver = uc.Chrome(options=self.__Setting_Options(),version_main=114)
            self.driver.get(url)

            while True:
                cookies = self.driver.get_cookies()    
                for index in range(len(cookies)):
                    name = cookies[index]['name']
                    value = cookies[index]["value"]
                    self.cookie[name] = value

                
                if len(self.cookie) > 1:
                    self.__OutputCookie(json)
                    return True
                else:
                    self.timeout += 1
                    time.sleep(1)

                    # 超時 15 秒退出
                    if self.timeout >= 15: 
                        raise Exception()
        except:
            return False

    def __OutputCookie(self,name):
        with open(f"{name}.json" , "w") as file:
            file.write(json.dumps(self.cookie, indent=4, separators=(',',':')))
 
Get = AutomationRequest()