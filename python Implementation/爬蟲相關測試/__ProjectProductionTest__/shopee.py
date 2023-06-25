import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import random
import time
import os
dir = os.path.dirname(os.path.abspath("R:/"))
os.chdir(dir)

def add():
    Settings = uc.ChromeOptions()
    Settings.add_argument("--headless")
    Settings.add_argument(f"--remote-debugging-port={random.randint(1024,65535)}")
    Settings.add_argument('--disable-cache')
    Settings.add_argument('--disk-cache-size=0')
    Settings.add_argument('--media-cache-size=0')
    Settings.add_argument('--disable-application-cache')
    Settings.add_argument('--disable-browser-side-navigation')
    Settings.add_argument('--disable-offline-load-stale-cache')
    Settings.add_argument('--disable-browser-side-navigation')
    return Settings

def shopee(search):
    driver = uc.Chrome(options=add())
    driver.get(f"https://shopee.tw/search?keyword={search}")
    driver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')

    for i in range(2,7):
        SCROLL_INCREMENT = i*700
        time.sleep(1)
        driver.execute_script(f"window.scrollTo(0,{SCROLL_INCREMENT});")

    bs4 = BeautifulSoup(driver.page_source, "html.parser")

    data = bs4.select("div.col-xs-2-4.shopee-search-item-result__item")

    for data in data:
        All = data.find("div" , class_="KMyn8J")
        print(All.text)

    time.sleep(1)
    driver.quit()
shopee(input("搜尋: "))