from concurrent.futures import ThreadPoolExecutor , ProcessPoolExecutor
import undetected_chromedriver as uc
import multiprocessing
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


class Test:
    def __init__(self):
        self.manager = multiprocessing.Manager()
        self.Queue = self.manager.Queue()
        self.CpuCore = multiprocessing.cpu_count()
        self.comic_link_box = ["a", 'b', 'c', "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n"]

    def ran1(self):
        with ProcessPoolExecutor(max_workers=self.CpuCore, initializer=self.initialize_queue, initargs=(self.Queue,)) as executor:
            for url in self.comic_link_box:
                executor.submit(self.ran2, url)

    @staticmethod
    def initialize_queue(queue):
        Test.Queue = queue

    @staticmethod
    def ran2(url):
        t = Test()
        t.Queue.put(url)
        
        # 从队列中获取数据
        data = t.Queue.get()
        print(data)

if __name__ == '__main__':
    t = Test()
    t.ran1()