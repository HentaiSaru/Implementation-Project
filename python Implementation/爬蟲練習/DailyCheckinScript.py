from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from multiprocessing import Process
from urllib.parse import unquote
from tkinter import messagebox
from selenium import webdriver
from bs4 import BeautifulSoup
import threading
import datetime
import shutil
import random
import pickle
import json
import time
import pytz
import os

# 取得登入資料相關接口
class Login:

    def Get_login_information():
        global UserInformation

        try:
            with open("UserInformation.json","r") as User:
                UserInformation = json.load(User)
        except:
            messagebox.showerror("沒有找到設置", "當前路徑不存在UserInformation.json\n已在當前目錄下創建")
            Format = [
                {
                    "domain": "null",
                    "expirationDate": "null",
                    "hostOnly": "null",
                    "httpOnly": "null",
                    "name": "null",
                    "path": "null",
                    "sameSite": "null",
                    "secure": "null",
                    "session": "null",
                    "storeId": "null",
                    "value": "null"
                },
                {
                    "account":"null",
                    "password":"null"
                }
            ]
            OutFormat = json.dumps(Format, indent=4 , separators=(',',': '))
            with open("UserInformation.json","w") as User:
                User.write(OutFormat)
            pass

    def Get_login(key):
        Login.Get_login_information()
        login = []
        global UserInformation

        try:
            match key:
                case "wuyong":
                    login.append(UserInformation[0])
                    return login
                case "Genshin":
                    return UserInformation[1]
                case _:
                    return None
        except:
            pass

# 計算等待秒數
def WaitingTime():
    TaipeiTimezone = pytz.timezone('Asia/Taipei')
    TargetTime = datetime.time(hour=0, minute=0, second=0)
    current_time = datetime.datetime.now(TaipeiTimezone).time()
    if current_time < TargetTime:
        seconds_to_wait = (datetime.datetime.combine(datetime.date.today(), TargetTime) - datetime.datetime.combine(datetime.date.today(), current_time)).seconds
    else:
        seconds_to_wait = (datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1), TargetTime) - datetime.datetime.combine(datetime.date.today(), current_time)).seconds
    return seconds_to_wait

# 讀取pkl保存的資料並打印出來
def CookieView(path,pkl):
    with open(f'./{path}/{pkl}.pkl', 'rb') as f:
        cookies = pickle.load(f)
    print(cookies)

# 創建的數據檔名獲取
def databases(web):
    return web+"default"

# 隨機端口分配   
def RandomPort(web):
    match web:
        case "wuyong":
            port = random.randint(1024, 2048)
            return port
        case "miaoaaa":
            port = random.randint(2049, 4096)
            return port
        case "Genshin":
            port = random.randint(4097, 8194)
            return port
        case "black":
            port = random.randint(8195, 16390)
            return port

# selenium創建 相關設置
def add(page):
    Settings = Options()
    # 在完整輸入每個網站的登入狀態前,可以先都開啟窗口測試,也就是把headless註解掉
    #Settings.add_argument("--headless")
    Settings.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36')
    Settings.add_argument('--remote-debugging-address=0.0.0.0')
    # 為了要同時多開窗口操作,Port和配置檔,不能是一樣的
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

def Open_Wuyong(Sc):
    Wuyongdriver = webdriver.Chrome(options=add("wuyong"))
    Wuyongdriver.get("https://wuyong.fun/")
    Wuyongdriver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')

    if not os.path.isfile("./Wuyongdefault/wuyongCookies.pkl"):
        for cookie in Login.Get_login("wuyong"):
            Wuyongdriver.add_cookie(cookie)  
        Wuyongdriver.refresh()

    Wuyongbutton = WebDriverWait(Wuyongdriver,1).until(EC.element_to_be_clickable((By.XPATH, "//i[@class='b2font b2-gift-2-line ']")))
    Wuyongbutton.click()

    time.sleep(Sc)
    pickle.dump(Wuyongdriver.get_cookies(), open("./Wuyongdefault/wuyongCookies.pkl","wb"))
    Wuyongdriver.quit()

def Open_miaoaaa(Sc):

    miaoaaadriver = webdriver.Chrome(options=add("miaoaaa"))
    miaoaaadriver.get("https://www.miaoaaa.com/sites/530.html")
    miaoaaadriver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')

    miaoaaabutton = WebDriverWait(miaoaaadriver,0).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='btn btn-arrow mr-2']")))
    miaoaaabutton.click()

    """ 保存cookie 並 重新載入保存的 , 可用於記住登入狀態
    pickle.dump(driver.get_cookies(), open("./default/cookies.pkl","wb"))
    cookies = pickle.load(open("./default/MiaCookies.pkl", "rb"))
    for cookie in cookies:
            driver.add_cookie(cookie)
    """
    
    time.sleep(Sc)
    pickle.dump(miaoaaadriver.get_cookies(), open("./miaoaaadefault/MiaCookies.pkl","wb"))
    miaoaaadriver.quit()

def Open_Genshin(Sc):

    Genshindriver = webdriver.Chrome(options=add("Genshin"))
    Genshindriver.get("https://act.hoyolab.com/ys/event/signin-sea-v3/index.html?act_id=e202102251931481")
    Genshindriver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')

    # 關閉彈出窗口,如果有的話
    try:
        Genshinbutton = WebDriverWait(Genshindriver,3).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='components-home-assets-__sign-guide_---guide-close---2VvmzE']")))
        Genshinbutton.click()
    except:pass

    # 點選簽到位置 (已經簽到的就會找不到,因此當沒找到時,要讓他跳過)
    try:
        Genshinbutton = WebDriverWait(Genshindriver,5).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='components-home-assets-__sign-content_---red-point---3lkHfJ']")))
        Genshinbutton.click()
    except:pass

    # 如果沒有登入的話,幫你點推特登入
    try:
        # 使用Twitter 登入 div[1] = Google
        Genshinbutton = WebDriverWait(Genshindriver,5).until(EC.element_to_be_clickable((By.XPATH, "//div[4][@class='account-sea-third-party-login-item']//img[@class='account-sea-login-icon']")))
        Genshinbutton.click()

        # 普通的操作切窗無法
        # 獲取當前開啟的窗口名稱
        handles = Genshindriver.window_handles
        for handle in handles:
            Genshindriver.switch_to.window(handle)
            if "Twitter / 授權應用程式" in Genshindriver.title:
                break

        # 取得保存的帳號,密碼
        acc , pas  = Login.Get_login("Genshin").values()
        
        # 輸入帳號
        accountbutton = WebDriverWait(Genshindriver,3).until(EC.element_to_be_clickable((By.XPATH,"//input[@class='text']")))
        accountbutton.click()
        accountbutton.send_keys(acc)

        # 輸入密碼
        passwordbutton = WebDriverWait(Genshindriver,3).until(EC.element_to_be_clickable((By.XPATH,"//input[@class='password text']")))
        passwordbutton.click()
        passwordbutton.send_keys(pas)

        # 送出
        loginbutton = WebDriverWait(Genshindriver,3).until(EC.element_to_be_clickable((By.XPATH,"//input[@class='submit button selected']")))
        loginbutton.click()

        # ... 當然帳號需要授權碼的自己輸入w

        # 再次切回原窗口
        handles = Genshindriver.window_handles
        for handle in handles:
            Genshindriver.switch_to.window(handle)
            if "【原神】每日簽到" in Genshindriver.title:
                break

        # 點選簽到位置
        Genshinbutton = WebDriverWait(Genshindriver,5).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='components-home-assets-__sign-content_---red-point---3lkHfJ']")))
        Genshinbutton.click()
    except:pass

    time.sleep(Sc)
    pickle.dump(Genshindriver.get_cookies(), open("./Genshindefault/GenshinCookies.pkl","wb"))
    Genshindriver.quit()

# 這邊就沒有做Cookie和登入的部份,就手動登入按保存吧
def Open_black(Sc):
    blackdriver = webdriver.Chrome(options=add("black"))
    blackdriver.get("https://black.is-best.site/plugin.php?id=gsignin:index")

    # 等待到指定時間才運行
    time.sleep(WaitingTime()+1) # 延遲測試
    blackdriver.refresh()
    blackbutton = WebDriverWait(blackdriver,3).until(EC.element_to_be_clickable((By.XPATH,"//a[@class='right']")))
    blackbutton.click()

    time.sleep(Sc)
    pickle.dump(blackdriver.get_cookies(), open("./blackdefault/blackCookies.pkl","wb"))
    blackdriver.quit()


def Open_hgamefree(Sc):
   "https://hgamefree.info/"


# 後方的 args 是用於傳遞 tuple 內的數值,將其設置為窗口關閉的延遲時間
threading.Thread(target=Open_black,args=(5,)).start()
time.sleep(WaitingTime()+10)
threading.Thread(target=Open_Wuyong,args=(5,)).start()
time.sleep(1)
threading.Thread(target=Open_miaoaaa,args=(10,)).start()
time.sleep(1)
threading.Thread(target=Open_Genshin,args=(5,)).start()

# 輸出Cookie內容的方法 資料位置 , 要開啟的Cookie檔案名
#CookieView("blackdefault","blackCookies")