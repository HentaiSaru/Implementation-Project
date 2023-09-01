from concurrent.futures import ThreadPoolExecutor , ProcessPoolExecutor
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from multiprocessing import process , Pool
import undetected_chromedriver as uc
from lxml import etree
import cloudscraper
import pyperclip
import threading
import requests
import keyboard
import random
import time
import re
import os
dir = os.path.abspath("R:/") # 可更改預設路徑
os.chdir(dir)

url = "https://www.google.com.tw/"

def settings():
    Settings = uc.ChromeOptions()
    Settings.add_argument("--headless")
    Settings.add_argument("--incognito")
    Settings.add_argument('--no-sandbox')
    Settings.add_argument('--log-level=3')
    Settings.add_argument('--no-first-run')
    Settings.add_argument('--disable-infobars')
    Settings.add_argument("--disable-extensions")
    Settings.add_argument('--no-service-autorun')
    Settings.add_argument("--disable-file-system")
    Settings.add_argument("--disable-geolocation")
    Settings.add_argument("--disable-web-security")
    Settings.add_argument('--password-store=basic')
    Settings.add_argument('--disable-notifications')
    Settings.add_argument("--disable-popup-blocking") 
    Settings.add_argument('--no-default-browser-check')
    Settings.add_argument("--profile-directory=Default")
    Settings.add_argument("--ignore-certificate-errors")
    Settings.add_argument("--disable-plugins-discovery")
    Settings.add_argument('--remote-debugging-address=0.0.0.0')
    Settings.add_argument('--disable-blink-features=AutomationControlled')
    Settings.add_argument(f"--remote-debugging-port={random.randint(1024,65535)}")
    return Settings

def request(url):
    # 創建 CloudScraper 實例
    scraper = cloudscraper.create_scraper()
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
    cookie = {}
    req = scraper.get(url, headers=headers, cookies=cookie)
    return req.text
    return etree.fromstring(req.content , etree.HTMLParser())

def calculate(Pages):
    home_pages = Pages / 20
    remainder_pages = Pages % 20
     
    if remainder_pages > 0:
        total_pages = int(home_pages + 1)
    else:
        total_pages = int(home_pages) 
        
    return total_pages
        
if __name__ == '__main__':
    Filter = r'[^\d.-]'
    #print(re.sub(Filter, "", "名稱"))