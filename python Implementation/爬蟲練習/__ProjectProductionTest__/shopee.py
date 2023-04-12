from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from urllib.parse import unquote
from tkinter import messagebox
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
import random
import uuid
import time
import json
import os
dir = os.path.dirname(os.path.abspath("R:/"))
os.chdir(dir)

def add():
    Settings = Options()
    #Settings.add_argument("--headless")
    Settings.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36')
    Settings.add_argument('--remote-debugging-address=0.0.0.0')
    Settings.add_argument(f"--remote-debugging-port={random.randint(1024,65535)}")
    Settings.add_argument("user-data-dir=R:/ChromTest")
    Settings.add_argument('--disk-cache-dir=R:/caching')
    Settings.add_argument('--start-maximized')
    Settings.add_argument('--disable-notifications')
    Settings.add_argument('--ignore-certificate-errors')
    Settings.add_argument('--disable-popup-blocking')
    Settings.add_argument('--log-level=3')
    Settings.add_experimental_option('excludeSwitches', ['enable-logging'])
    Settings.add_experimental_option('excludeSwitches', ['enable-automation'])
    Settings.add_experimental_option('useAutomationExtension', False)
    return Settings

def shopee(search):
    driver = webdriver.Chrome(options=add())
    driver.get(f"https://shopee.tw/search?keyword={search}")
    driver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')

    for i in range(2,9):
        SCROLL_INCREMENT = i*500
        time.sleep(1)
        driver.execute_script(f"window.scrollTo(0,{SCROLL_INCREMENT});")

    bs4 = BeautifulSoup(driver.page_source, "html.parser")

    data = bs4.select("div.col-xs-2-4.shopee-search-item-result__item")

    for data in data:
        All = data.find("div" , class_="KMyn8J")
        print(All.text)

    time.sleep(5)
    driver.quit()

shopee(input("搜尋: "))