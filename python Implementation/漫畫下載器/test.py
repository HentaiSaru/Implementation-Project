import random
from undetected_chromedriver import Chrome, ChromeOptions, install
import multiprocessing
import threading
import requests
import time
import os
dir = os.path.abspath("R:/") # 可更改預設路徑
os.chdir(dir)

header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
}
# chrome_options = ""
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-popup-blocking")
# chrome_options.add_argument("--profile-directory=Default")
# chrome_options.add_argument("--ignore-certificate-errors")
# chrome_options.add_argument("--disable-plugins-discovery")
# chrome_options.add_argument("--incognito")
# chrome_options.add_argument('--no-first-run')
# chrome_options.add_argument('--no-service-autorun')
# chrome_options.add_argument('--no-default-browser-check')
# chrome_options.add_argument('--password-store=basic')
# chrome_options.add_argument('--no-sandbox')

def Download(Path,SaveName,Image_URL,headers):

        ImageData = requests.get(Image_URL, headers=headers)
        if ImageData.status_code == 200:
            with open(SaveName,"wb") as f:
                f.write(ImageData.content)

def test():
    install(path="R:/chromedriver.exe")
    Settings = Chrome.ChromeOptions()
    Settings.add_argument(f"--remote-debugging-port={random.randint(1024,65535)}")
    browser = Chrome.Chrome(Settings)
    browser.get("https://www.google.com.tw/" , executable_path="C:/my_chromedriver.exe")
    time.sleep(10)


# for _ in range(5):
#     threading.Thread(target=test).start()
install(path="R:/chromedriver.exe")