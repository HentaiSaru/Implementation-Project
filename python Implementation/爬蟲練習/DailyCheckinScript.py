from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from multiprocessing import Process
from urllib.parse import unquote
from selenium import webdriver
from bs4 import BeautifulSoup
import threading
import shutil
import random
import pickle
import json
import time
import os

"""
1. 練習以插入Cookie 的方式

2. 練習以自動化操作登入

"""

# 取得登入資料相關接口
class Login:

    def Get_login_information():
        global UserInformation

        try:
            with open("UserInformation.json","r") as User:
                UserInformation = json.load(User)
        except:
            pass

    def Get_login(key):
        Login.Get_login_information()
        login = []
        global UserInformation

        match key:
            case "wuyong":
                login.append(UserInformation[0])
                return login

# 讀取pkl保存的資料並打印出來
def CookieView(path,pkl):
    with open(f'./{path}/{pkl}.pkl', 'rb') as f:
        cookies = pickle.load(f)
    print(cookies)

def databases(web):
    match web:
        case "wuyong":
            return "Wuyongdefault"
        case "miaoaaa":
            return "miaoaaadefault"

# 隨機端口分配   
def RandomPort(web):
    match web:
        case "wuyong":
            port = random.randint(1024, 3072)
            return port
        case "miaoaaa":
            port = random.randint(3073, 9219)
            return port

# 相關設置
def add(page):
    Settings = Options()
    #Settings.add_argument("--headless")
    Settings.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36')
    Settings.add_argument('--remote-debugging-address=0.0.0.0')
    Settings.add_argument(f"user-data-dir={databases(page)}")
    Settings.add_argument(f"--remote-debugging-port={RandomPort(page)}")
    Settings.add_argument('--start-maximized') # 開啟最大化
    Settings.add_argument('--disable-notifications')
    Settings.add_argument('--ignore-certificate-errors')
    Settings.add_argument('--disable-popup-blocking')
    Settings.add_argument('--log-level=3')
    Settings.add_experimental_option('excludeSwitches', ['enable-logging'])
    Settings.add_experimental_option('excludeSwitches', ['enable-automation'])
    Settings.add_experimental_option('useAutomationExtension', False)
    return Settings

def Open_Wuyong():
    Wuyongdriver = webdriver.Chrome(options=add("wuyong"))
    Wuyongdriver.get("https://wuyong.fun/")
    Wuyongdriver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')

    if not os.path.isfile("./Wuyongdefault/wuyongCookies.pkl"):
        for cookie in Login.Get_login("wuyong"):
            Wuyongdriver.add_cookie(cookie)  
        Wuyongdriver.refresh()
        pickle.dump(Wuyongdriver.get_cookies(), open("./Wuyongdefault/wuyongCookies.pkl","wb"))

    checkinbutton = WebDriverWait(Wuyongdriver,1).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='user-w-qd']/div/i[@class='b2font b2-gift-2-line ']")))
    checkinbutton.click()

    time.sleep(5)
    Wuyongdriver.quit()

def Open_miaoaaa():

    miaoaaadriver = webdriver.Chrome(options=add("miaoaaa"))
    miaoaaadriver.get("https://www.miaoaaa.com/sites/530.html")
    miaoaaadriver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')

    checkinbutton = WebDriverWait(miaoaaadriver,0).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='btn btn-arrow mr-2']")))
    checkinbutton.click()

    """ 保存cookie 並 重新載入保存的 , 可用於記住登入狀態
    pickle.dump(driver.get_cookies(), open("./default/cookies.pkl","wb"))
    cookies = pickle.load(open("./default/MiaCookies.pkl", "rb"))
    for cookie in cookies:
            driver.add_cookie(cookie)
    """

    time.sleep(15)
    miaoaaadriver.quit()

threading.Thread(target=Open_miaoaaa).start()
time.sleep(2)
threading.Thread(target=Open_Wuyong).start()
#CookieView("miaoaaadefault","MiaCookies")