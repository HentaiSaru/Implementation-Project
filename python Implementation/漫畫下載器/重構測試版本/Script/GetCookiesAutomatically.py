import undetected_chromedriver as uc
import random
import json
import time
import os

class Chrome(uc.Chrome):
    def __del__(self):
        try:
            self.service.process.kill()
            self.quit()
            self.close()
        except:
            pass

class AutomationRequest:
    def __init__(self):
        self.cookie = {}
        self.driver = None
        self.timeout = 0
        self.Settings = uc.ChromeOptions()
        self.hidden = None

        self.show = "."
        self.load = 0

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
        if self.hidden:self.Settings.add_argument("--headless")
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

    def __Loading_Display(self, time: int):
        self.load += 1

        if self.load > 3:
            print(f"\r獲取中[{time}秒]   ", end="", flush=True)
            self.load = 0
        else:
            print(f"\r獲取中[{time}秒]{self.show * self.load}", end="", flush=True)

    def AGCookie(self,url: str,json: str):
        """
    自動請求 Cookie
    >>> 參數

    *   url  請求的連結
    *   json 請求成功後創建的 .json 名稱 (不需要打.json)

    >>> 說明

    *   回傳 True / False 為請求成功狀態
    *   預設有 15 秒的超時時間 , 超過這時間沒有請求到 , 將會回傳 False
        """
        print("嘗試獲取 Cookie ==>")
        self.hidden = True
        try:
            if json.find(".json") != -1:
                json = json.rsplit(".", 1)[0]

            self.driver = Chrome(options=self.__Setting_Options(),version_main=114)
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
                    
                self.__Loading_Display(self.timeout)
        except:
            return False

    def MGCookie(self,url: str,json: str):
        """
    手動請求 Cookie
    >>> 參數

    *   url  請求的連結
    *   json 請求成功後創建的 .json 名稱 (不需要打.json)

    >>> 說明

    *   呼叫後會啟用網頁窗口 , 等待登入後 , 鍵入 y 進行取得
    *   該窗口網站並不會記錄登入狀態 , 所以每次呼叫都要重登
    """
        print("啟動窗口等待獲取 cookie ==>")
        self.hidden = False
        try:
            if json.find(".json") != -1:
                json = json.rsplit(".", 1)[0]

            self.driver = Chrome(options=self.__Setting_Options(),version_main=114)
            self.driver.get(url)

            while True:

                confirm = input("請[登入帳號後]鍵入 (y) 進行獲取 : ")

                if confirm == "y":
                    cookies = self.driver.get_cookies()

                    for index in range(len(cookies)):
                        name = cookies[index]['name']
                        value = cookies[index]["value"]
                        self.cookie[name] = value

                    if len(self.cookie) > 0:
                        self.__OutputCookie(json)
                    else:
                        return False
                    
                    self.driver.close()
                    break
                else:
                    print("請輸入正確的確認鍵\n")
                    continue
        except:
            return False

    def __OutputCookie(self,name):
        with open(f"{name}.json" , "w") as file:
            file.write(json.dumps(self.cookie, indent=4, separators=(',',':')))
 
Get = AutomationRequest()