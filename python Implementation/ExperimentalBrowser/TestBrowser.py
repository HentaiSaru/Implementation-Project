from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import threading
import random
import time
class TestBrowser:
    def __init__(self):
        self.Settings = uc.ChromeOptions()
        self.Version = "1.0.0"
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

    def Enable_browsing(self,url:str ="https://www.google.com.tw/"):
        self.driver = uc.Chrome(options=self.Setting_Options())
        self.driver.delete_all_cookies()
        self.driver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')

        self.driver.get(url)

        threading.Thread(target=self.detection).start()

    def get_version(self):
        return self.Version

    def detection(self):
        while True:
            try:
                time.sleep(10)
                WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//title")))
                time.sleep(5)
                WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH, "//body")))
            except:
                self.driver.quit()
                break