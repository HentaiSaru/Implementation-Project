from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import random
import json
import os

class AutomationRequest:
    def __init__(self):
        self.cookie = {}
        self.driver = None
        self.Settings = uc.ChromeOptions()

        self.NHUrl = "https://nhentai.net/"

    def browser_reset(self):
        """
    !   注意
    *   此重置方法將會關閉 Google 瀏覽器
    *   接著會重裝相關依賴庫
        """
        print("重置中請稍後...")
        # 關閉 Google
        os.system('wmic process where name="chrome.exe" delete >nul 2>&1')
        # 刪除 selenium
        os.system("pip uninstall selenium -y >nul 2>&1")
        # 刪除 undetected_chromedriver
        os.system("pip uninstall undetected_chromedriver -y >nul 2>&1")
        # 安裝 selenium
        os.system("pip install selenium >nul 2>&1")
        # 安裝 undetected_chromedriver
        os.system("pip install undetected_chromedriver >nul 2>&1")
        # 更新 Python 和 pip
        os.system("python.exe -m pip install --upgrade pip >nul 2>&1")
        os.system("pip install --upgrade setuptools >nul 2>&1")
        os.system("pip install --upgrade wheel >nul 2>&1")
        print("重置完成...")

    def Setting_Options(self):
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
    
    def Request_NHCookie(self):
        try:
            self.driver = uc.Chrome(options=self.Setting_Options(),version_main=114)
            self.driver.get(self.NHUrl)

            WebDriverWait(self.driver,60).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='container index-container']")))
            cookies = self.driver.get_cookies()    

            for index in range(len(cookies)):
                name = cookies[index]['name']
                value = cookies[index]["value"]
                self.cookie[name] = value

            if len(self.cookie) == 2:
                self.driver.close()
                self.OutputCookie()
                return True
            else:
                raise Exception()
        except:
            print("請求失敗 , 請重新嘗試")

    def OutputCookie(self):
        with open("NHCookies.json" , "w") as file:
            file.write(json.dumps(self.cookie, indent=4, separators=(',',':')))
            
Get = AutomationRequest()
print(Get.Request_NHCookie())