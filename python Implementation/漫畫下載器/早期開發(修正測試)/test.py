from concurrent.futures import ThreadPoolExecutor , ProcessPoolExecutor
from multiprocessing import process , Pool
import undetected_chromedriver as uc
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

def browser():
    return uc.Chrome(
        options=settings(),
    )

def main():
    driver = browser()
    driver.get(url)
    time.sleep(3)
    driver.close()


def manga_page_data_processing(url):
    print("當前處理:", url)

if __name__ == '__main__':
    """ [Pool 線程池]
        num_processes = 10
        pool = Pool(processes=num_processes)

        STime = time.time()

        results = []
        for url in range(10000):
            result = pool.apply_async(manga_page_data_processing, args=(url,))
            results.append(result)

        pool.close()
        pool.join()

        ETime = time.time()
        print(ETime-STime)
    """

    STime = time.time()

    with ProcessPoolExecutor(max_workers=10) as executor:
        for url in range(10000):
            executor.submit(manga_page_data_processing,url)

    print(time.time()-STime)