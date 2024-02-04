from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import threading
import random
import time
import os

class Settings:
    def __init__(self) -> None:
        self.User = os.path.expandvars("%LOCALAPPDATA%/Google/Chrome/User Data").replace("\\", "/")
        self.Options = Options()
        self.Generate_Port = []
        self.Port = 1024

        self.Cookie = [
            {"name":"scratchcsrftoken","value":"#"},
            {"name":"scratchsessionsid","value":'#'}
        ]

    def RandomPort(self) -> int:
        port = random.randint(self.Port, 65535)
        if port not in self.Generate_Port:
            self.Generate_Port.append(port)
            return port
        else:
            return self.RandomPort()

    def Option(self) -> object:
        self.Options.add_argument("--no-sandbox")
        self.Options.add_argument("--log-level=3")
        self.Options.add_argument("--start-maximized")
        self.Options.add_argument("--disable-web-security")
        self.Options.add_argument("--disable-notifications")
        self.Options.add_argument("--disable-popup-blocking")
        self.Options.add_argument("--no-default-browser-check")
        self.Options.add_argument("--ignore-certificate-errors")
        self.Options.add_argument(f"--profile-directory=Default")
        self.Options.add_argument(f"--user-data-dir={self.User}")
        self.Options.add_argument("--remote-debugging-address=0.0.0.0")
        self.Options.add_argument("--safebrowsing-disable-download-protection")
        self.Options.add_argument(f"--remote-debugging-port={self.RandomPort()}")

        self.Options.add_experimental_option("useAutomationExtension", False)
        self.Options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.Options.add_experimental_option("excludeSwitches", ["enable-automation"])
        return self.Options

class Browser(Settings):
    def __init__(self) -> None:
        super().__init__()
        self.Driver = None

    def Enable_Browsing(self, Url1, Url2):
        self.Driver = webdriver.Chrome(self.Option())
        self.Driver.get(Url1)
        self.Driver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')

        WebDriverWait(self.Driver, 120).until(EC.presence_of_element_located((By.XPATH, "//li[@class='logo']")))

        for cookie in self.Cookie:
            self.Driver.add_cookie(cookie)
        self.Driver.refresh()

        WebDriverWait(self.Driver, 120).until(EC.presence_of_element_located((By.XPATH, "//a[@class='ignore-react-onclickoutside user-info']")))

        self.Driver.get(Url2)

        threading.Thread(target=self.Detection).start()

    def Detection(self):
        try:
            while True:
                if not self.Driver.window_handles:
                    self.Driver.quit()
                    break
                time.sleep(5)
        except:
            pass

if __name__ == "__main__": 
    Bro = Browser()
    Bro.Enable_Browsing(
        "#",
        "#"
    )