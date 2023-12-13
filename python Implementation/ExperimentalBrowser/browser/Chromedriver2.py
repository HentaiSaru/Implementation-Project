import subprocess
import importlib
import threading
import random
import time
import os

# 檢查使用庫
def Library_installation_detection(lib):
    try:
        importlib.import_module(lib)
    except:
        subprocess.check_call(["pip", "install", lib])
for check in ["undetected_chromedriver2"]:
    Library_installation_detection(check)

import undetected_chromedriver2 as uc

class Chrome(uc.Chrome):
    def __del__(self):
        try:
            self.service.process.kill()
        except:
            pass

class TestBrowser:
    def __init__(self):
        self.driver_path = rf"{os.path.dirname(os.path.abspath(__file__))}\driver\chromedriver.exe"
        self.Settings = uc.ChromeOptions()
        self.Version = "1.0.2"
        self.driver = None

    def Setting_Options(self):
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

    def Enable_browsing(self, url:str ="https://www.google.com.tw/"):
        self.driver = Chrome(
            version_main=120,
            advanced_elements=True,
            options=self.Setting_Options(),
            driver_executable_path=self.driver_path
        )
        self.driver.delete_all_cookies()
        self.driver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')

        self.driver.get(url)

        threading.Thread(target=self.detection).start()

    def get_version(self):
        return self.Version

    def detection(self):
        try:
            while True:
                if not self.driver.window_handles:
                    self.driver.close()
                    break
                time.sleep(5)
        except:
            pass
        
TUC2 = TestBrowser()