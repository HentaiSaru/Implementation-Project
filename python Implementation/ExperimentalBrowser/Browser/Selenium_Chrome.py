from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import threading
import random
import time

class Settings:
    def __init__(self) -> None:
        self.Options = Options()
        self.Generate_Port = []
        self.Port = 1024
        
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
        self.Options.add_argument("--profile-directory=Default")
        self.Options.add_argument("--ignore-certificate-errors")
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
        self.Version = "1.0.0"
        
    def Get_Version(self) -> str:
        return self.Version
    
    def Enable_Browsing(self, Url:str ="https://www.google.com.tw/"):
        self.Driver = webdriver.Chrome(self.Option())
        self.Driver.get(Url)
        
        self.Driver.delete_all_cookies()
        self.Driver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')
        
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