from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import random
import time
Settings = Options()
Settings.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36')
Settings.add_argument('--remote-debugging-address=0.0.0.0')
Settings.add_argument(f"--remote-debugging-port={random.randint(1024,65535)}")
Settings.add_argument("user-data-dir=R:/ChromTest")
Settings.add_argument('--start-maximized')
Settings.add_argument('--disable-notifications')
Settings.add_argument('--ignore-certificate-errors')
Settings.add_argument('--disable-popup-blocking')
Settings.add_argument('--log-level=3')
Settings.add_experimental_option('excludeSwitches', ['enable-logging'])
Settings.add_experimental_option('excludeSwitches', ['enable-automation'])
Settings.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=Settings)
driver.get("https://www.google.com.tw/")
driver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')
while True:
    try:
        time.sleep(5)
        status_confirmation = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//title")))
    except:break