from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tkinter import messagebox
from selenium import webdriver
from bs4 import BeautifulSoup
from lxml import etree
import threading
import datetime
import random
import pickle
import json
import time
import pytz
import sys
import re
import os
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

# 清除非正常關閉時遺留的垃圾
def TrashRemoval():
    os.system('for /d %d in ("C:\Program Files\chrome_BITS*") do rd /s /q "%d" >nul 2>&1')
    os.system('for /d %d in ("C:\Program Files (x86)\scoped_dir*") do rd /s /q "%d" >nul 2>&1')

class Login:
    def __init__(self):
        self.UserInformation = None

    # 讀取登入資料檔案 和 創建登入資料檔案格式
    def Get_login_information(self):

        try:
            with open("UserInformation.json","r") as User:
                self.UserInformation = json.load(User)
        except:
            messagebox.showerror("沒有找到設置", "當前路徑不存在UserInformation.json\n已在當前目錄下創建\n請填寫數據後再次運行",parent=None)
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
                    "Genshin_account":"null",
                    "Genshin_password":"null"
                },
                {
                    "StarRail_account":"null",
                    "StarRail_password":"null"
                }
            ]
            OutFormat = json.dumps(Format, indent=4 , separators=(',',': '))
            with open("UserInformation.json","w") as User:
                User.write(OutFormat)
            os._exit(0)

    # 取得登入資料
    def Get_login(self,key):
        Login.Get_login_information()
        login = []

        try:
            match key:
                case "wuyong":
                    login.append(self.UserInformation[0])
                    return login
                case "Genshin":
                    return self.UserInformation[1]
                case "StarRail":
                    return self.UserInformation[2]
                case _:
                    return None
        except:
            pass
Login = Login()
class GetParametric():
    def __init__(self):
        self.count = 0
        self.port = 1024

    # 計算等待秒數
    def WaitingTime(self):
        TaipeiTimezone = pytz.timezone('Asia/Taipei')
        TargetTime = datetime.time(hour=0, minute=0, second=0)
        current_time = datetime.datetime.now(TaipeiTimezone).time()
        if current_time < TargetTime:
            seconds_to_wait = (datetime.datetime.combine(datetime.date.today(), TargetTime) - datetime.datetime.combine(datetime.date.today(), current_time)).seconds
        else:
            seconds_to_wait = (datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1), TargetTime) - datetime.datetime.combine(datetime.date.today(), current_time)).seconds
        
        if seconds_to_wait > 120:
            return 5
        else:
            return seconds_to_wait

    # 讀取pkl保存的資料並打印出來
    def CookieView(self,path,pkl):
        
        with open(f'./{path}/{pkl}.pkl', 'rb') as f:
            cookies = pickle.load(f)
        print(cookies)

    # 創建的數據檔名獲取
    def databases(self,web):
        return web+"default"
    
    def datacreation(self,cookies,path,name):
        pickle.dump(cookies, open(f"{path}/{name}.pkl","wb"))

    # 隨機端口分配
    def RandomPort(self):
        self.count += 1

        if self.port <= 65535:
            if self.count == 1:
                return random.randint(self.port, self.port*1.5)
            elif self.count > 1:
                self.port *= 1.5 + 1
                return random.randint(self.port, self.port*1.5)
        else:return random.randint(1024,65535) # 先隨便寫個

# selenium創建 相關設置
def add(page):
    Settings = Options()
    # 在完整輸入每個網站的登入狀態前,可以先都開啟窗口測試,也就是把headless註解掉
    # Settings.add_argument("--headless")
    Settings.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36')
    Settings.add_argument('--remote-debugging-address=0.0.0.0')
    # 為了要同時多開窗口操作,Port和配置檔,不能是一樣的
    Settings.add_argument("--no-sandbox")
    Settings.add_argument('--log-level=3')
    Settings.add_argument('--start-maximized') # 開啟最大化
    Settings.add_argument('--disk-cache-dir=R:/caching')
    Settings.add_argument(f"user-data-dir={GetParametric().databases(page)}")
    Settings.add_argument(f"--remote-debugging-port={GetParametric().RandomPort()}")
    Settings.add_argument('--disable-notifications')
    Settings.add_argument('--disable-popup-blocking')
    Settings.add_argument('--ignore-certificate-errors')
    Settings.add_experimental_option('excludeSwitches', ['enable-logging'])
    Settings.add_experimental_option('excludeSwitches', ['enable-automation'])
    Settings.add_experimental_option('useAutomationExtension', False)
    return Settings

#(無寫登入方法,需先自行登入)
class forum:
    # 自動使用道具
    def jkf_use_props(Sc):
        jkfdriver = webdriver.Chrome(options=add("Jkf"))
        jkfdriver.get("https://www.jkforum.net/forum.php?mod=forum")
        time.sleep(1)
        jkfdriver.get("https://www.jkforum.net/material/my_item")
        jkfdriver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')

        time.sleep(15) # 這網站加載很慢,等久一點(運行失敗就再加長時間)
        Content = jkfdriver.page_source.encode('utf-8').strip()
        html = BeautifulSoup(Content,'html.parser')

        try: # 使用小型體力藥水
        
            smallpotion = WebDriverWait(jkfdriver,20).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'item-wrap') and .//div[contains(text(), '小型體力藥水')]]//button[contains(text(), '查看')]")))
            smallpotion.click()

            SmallPotionQuantity = html.select_one("div.item-wrap:-soup-contains('小型體力藥水') div.text-white.absolute.bottom-0.right-3.CENnO4Uu4CssJR9PLmCG").text
            Quantity = int(SmallPotionQuantity.split("x")[1])

            for _ in range(Quantity):

                potionuse = WebDriverWait(jkfdriver,10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='OvtXIlmLtXEE_eWpy1jH px-4']")))
                potionuse.click()

                confirm = WebDriverWait(jkfdriver,10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='OvtXIlmLtXEE_eWpy1jH px-4'][text()='確認']")))
                confirm.click()
        except:pass

        try: # 使用中型藥水
            mediumpotion = WebDriverWait(jkfdriver,20).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'item-wrap') and .//div[contains(text(), '中型體力藥水')]]//button[contains(text(), '查看')]")))
            mediumpotion.click()

            MediumPotionQuantity = html.select_one("div.item-wrap:-soup-contains('中型體力藥水') div.text-white.absolute.bottom-0.right-3.CENnO4Uu4CssJR9PLmCG").text
            Quantity = int(MediumPotionQuantity.split("x")[1])

            for _ in range(Quantity):

                    potionuse = WebDriverWait(jkfdriver,10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='OvtXIlmLtXEE_eWpy1jH px-4']")))
                    potionuse.click()

                    confirm = WebDriverWait(jkfdriver,10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='OvtXIlmLtXEE_eWpy1jH px-4'][text()='確認']")))
                    confirm.click()
        except:pass

        time.sleep(Sc)
        pickle.dump(jkfdriver.get_cookies(), open("./Jkfdefault/JkfCookies.pkl","wb"))
        jkfdriver.quit()

    # 挖礦功能
    def jkf_mining(Quantity,Location,Sc):
        jkfdriver = webdriver.Chrome(options=add("Jkf"))
        jkfdriver.get("https://www.jkforum.net/forum.php?mod=forum")
        time.sleep(1)
        jkfdriver.get("https://www.jkforum.net/material/mining")
        jkfdriver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')
        time.sleep(8) # 等待載入,找不到就時間延長

        match Location:
            case "巨龍巢穴":Location = 1
            case "精靈峽谷":Location = 2
            case "廢棄礦坑":Location = 3

        # 根據選擇的區域,點選開始挖礦
        startmining =  WebDriverWait(jkfdriver,10).until(EC.element_to_be_clickable((By.XPATH, f"//div[@class='pt-10'][{Location}] //div[@class='OvtXIlmLtXEE_eWpy1jH YOKk3zC9K8EXQZUZPFiy'][text()='開始挖礦']")))
        startmining.click()

        # 先點選5次畫布,因為使用相對位置找不到,所以用絕對位置,可能之後需要修改
        mining = WebDriverWait(jkfdriver,10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div[1]/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/div/div[2]/canvas")))
        for _ in range(5):jkfdriver.execute_script("arguments[0].click();", mining)
        
        # 按再一次
        for _ in range(Quantity-1): # 因為上面執行過一遍,這邊-1
            time.sleep(0.1)
            again = WebDriverWait(jkfdriver,10).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='OvtXIlmLtXEE_eWpy1jH'][text()='再挖一次']")))
            again.click()

        time.sleep(Sc)
        pickle.dump(jkfdriver.get_cookies(), open("./Jkfdefault/JkfCookies.pkl","wb"))
        jkfdriver.quit()

    # 探索功能
    def jkf_explore(Quantity,Location,Sc):
        jkfdriver = webdriver.Chrome(options=add("Jkf"))
        jkfdriver.get("https://www.jkforum.net/forum.php?mod=forum")
        time.sleep(1)
        jkfdriver.get("https://www.jkforum.net/material/terrain_exploration")
        jkfdriver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')
        time.sleep(8)

        match Location:
            case "墮落聖地":Location = 1
            case "焚燒之地":Location = 2
            case "巨木森林":Location = 3

        # 刪除那個會擋到按鈕的白痴NPC
        jkfdriver.execute_script('document.querySelector("img.w-full.h-auto").remove();')

        startexplore = WebDriverWait(jkfdriver,10).until(EC.element_to_be_clickable((By.XPATH, f"//div[@class='pt-10'][{Location}] //div[@class='OvtXIlmLtXEE_eWpy1jH YOKk3zC9K8EXQZUZPFiy'][text()='開始探索']")))
        startexplore.click()

        explore = WebDriverWait(jkfdriver,10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div[1]/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/div/div[2]/canvas")))
        for _ in range(5):jkfdriver.execute_script("arguments[0].click();", explore)

        for _ in range(Quantity-1): # 因為上面執行過一遍,這邊-1
            time.sleep(0.1)
            again = WebDriverWait(jkfdriver,10).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='OvtXIlmLtXEE_eWpy1jH'][text()='再挖一次']")))
            again.click()
            # 如果被NPC元素擋到按鈕元素,可以使用JS的點擊
            #jkfdriver.execute_script("arguments[0].click();", again)

        time.sleep(Sc)
        pickle.dump(jkfdriver.get_cookies(), open("./Jkfdefault/JkfCookies.pkl","wb"))
        jkfdriver.quit()

class script:

    def Open_Wuyong(Sc):
        Wuyongdriver = webdriver.Chrome(options=add("wuyong"))
        Wuyongdriver.get("https://wuyong.fun/")
        Wuyongdriver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')

        if not os.path.isfile("Wuyongdefault/wuyongCookies.pkl"):
            for cookie in Login.Get_login("wuyong"):
                Wuyongdriver.add_cookie(cookie)  
            Wuyongdriver.refresh()

        Wuyongbutton = WebDriverWait(Wuyongdriver,1).until(EC.element_to_be_clickable((By.XPATH, "//i[@class='b2font b2-gift-2-line ']")))
        Wuyongbutton.click()

        time.sleep(Sc)
        GetParametric().datacreation(Wuyongdriver.get_cookies(),GetParametric().databases("wuyong"),"wuyongCookies")
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
        GetParametric().datacreation(miaoaaadriver.get_cookies(),GetParametric().databases("miaoaaa"),"MiaCookies")
        miaoaaadriver.quit()

    def Open_Genshin(Sc):

        Genshindriver = webdriver.Chrome(options=add("Genshin"))
        Genshindriver.get("https://act.hoyolab.com/ys/event/signin-sea-v3/index.html?act_id=e202102251931481&hyl_auth_required=true&hyl_presentation_style=fullscreen&lang=zh-tw&bbs_theme=dark&bbs_theme_device=1")
        Genshindriver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')

        # 關閉彈出窗口,如果有的話
        try:
            Genshinbutton = WebDriverWait(Genshindriver,2).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='components-home-assets-__sign-content-test_---red-point---2jUBf9']")))
            Genshinbutton.click()
        except:pass

        try: # 某確認框
            Genshinbutton = WebDriverWait(Genshindriver,2).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='mihoyo-cookie-tips__button mihoyo-cookie-tips__button--hk4e']")))
            Genshinbutton.click()
        except:pass

        # 點選簽到位置 (已經簽到的就會找不到,因此當沒找到時,要讓他跳過)
        try:
            for _ in range(3): # 測試
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
            Genshinbutton = WebDriverWait(Genshindriver,5).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='components-home-assets-__sign-content-test_---red-point---2jUBf9']")))
            Genshinbutton.click()
        except:pass

        time.sleep(Sc)
        GetParametric().datacreation(Genshindriver.get_cookies(),GetParametric().databases("Genshin"),"GenshinCookies")
        Genshindriver.quit()

    def Open_StarRail(Sc):

        StarRail = webdriver.Chrome(options=add("StarRail"))
        StarRail.get("https://act.hoyolab.com/bbs/event/signin/hkrpg/index.html?act_id=e202303301540311&hyl_auth_required=true&hyl_presentation_style=fullscreen&lang=zh-tw&plat_type=pc")
        StarRail.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')

        # 關閉彈出窗口(這個等待時間低於3秒,可能數據會加載錯誤)
        try:
            StarRailClos = WebDriverWait(StarRail,4).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='components-pc-assets-__dialog_---dialog-close---3G9gO2']")))
            StarRailClos.click()
        except:pass

        try:
            # 確認登入狀態
            html = etree.fromstring(StarRail.page_source,etree.HTMLParser())
            login = html.xpath("//img[@class='mhy-hoyolab-account-block__avatar-icon']")[0].get("src")

            if re.match(r"data:image/png;base64,.*",login): 
                loginclick = WebDriverWait(StarRail,3).until(EC.element_to_be_clickable((By.XPATH, "//img[@class='mhy-hoyolab-account-block__avatar-icon']")))
                loginclick.click()

                # 使用FaceBook登入 , [3] 是fb
                loginbutton = WebDriverWait(StarRail,3).until(EC.element_to_be_clickable((By.XPATH, "//div[3][@class='account-sea-third-party-login-item']//img[@class='account-sea-login-icon']")))
                loginbutton.click()

                time.sleep(1.5)
                handles = StarRail.window_handles
                for handle in handles:
                    StarRail.switch_to.window(handle)

                acc , pas  = Login.Get_login("StarRail").values()

                try:

                    accountbutton = WebDriverWait(StarRail,1).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='email']")))
                    accountbutton.click()
                    accountbutton.send_keys(acc)

                    passwordbutton = WebDriverWait(StarRail,1).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='pass']")))
                    passwordbutton.click()
                    passwordbutton.send_keys(pas)

                    loginbutton = WebDriverWait(StarRail,1).until(EC.element_to_be_clickable((By.XPATH,"//input[@name='login']")))
                    loginbutton.click()

                except:

                    passwordbutton = WebDriverWait(StarRail,1).until(EC.element_to_be_clickable((By.XPATH,"//input[@name='pass']")))
                    passwordbutton.click()
                    passwordbutton.send_keys(pas)

                    continuebutton = WebDriverWait(StarRail,1).until(EC.element_to_be_clickable((By.XPATH,"//label[@class='uiButton uiButtonConfirm uiButtonLarge']")))
                    continuebutton.click()

                while True:
                    handles = StarRail.window_handles
                    for handle in handles:
                        StarRail.switch_to.window(handle)
                        if "《崩壞：星穹鐵道》每日簽到" in StarRail.title:break
                        else:time.sleep(0.5)
                    break
        except:pass

        checkinday = int(html.xpath("//p[@class='components-pc-assets-__main-module_---day---3Q5I5A day']/span/text()")[0])+1
        checkin = WebDriverWait(StarRail,60).until(EC.element_to_be_clickable((By.XPATH, f"//div[@class='components-pc-assets-__prize-list_---item---F852VZ']/span[@class='components-pc-assets-__prize-list_---no---3smN44'][contains(text(), '第{checkinday}天')]")))
        
        checkin.click()
        #StarRail.execute_script("arguments[0].click();", checkin)

        time.sleep(Sc)
        GetParametric().datacreation(StarRail.get_cookies(),GetParametric().databases("StarRail"),"StarRailCookies")
        StarRail.quit()

    # 這邊就沒有做Cookie和登入的部份,就手動登入按保存吧
    def Open_black(Sc):
        blackdriver = webdriver.Chrome(options=add("black"))
        blackdriver.get("https://black.is-best.site/plugin.php?id=gsignin:index")

        # 等待到指定時間才運行
        time.sleep(GetParametric().WaitingTime()+0.7) # 成功測試
        for _ in range(3): # 總會有失敗的時候,重複三次
            blackdriver.refresh()
            blackbutton = WebDriverWait(blackdriver,3).until(EC.element_to_be_clickable((By.XPATH,"//a[@class='right']")))
            blackbutton.click()

        time.sleep(Sc)
        GetParametric().datacreation(blackdriver.get_cookies(),GetParametric().databases("black"),"blackCookies")
        blackdriver.quit()

if __name__ == "__main__":

    # ===== 網站簽到 =====
    # 後方的 args 是用於傳遞 tuple 內的數值 , 設置窗口關閉的延遲時間
    threading.Thread(target=script.Open_black,args=(5,)).start()
    time.sleep(GetParametric().WaitingTime()+10)
    threading.Thread(target=script.Open_Wuyong,args=(5,)).start()
    time.sleep(1)
    threading.Thread(target=script.Open_miaoaaa,args=(15,)).start()
    time.sleep(1)
    threading.Thread(target=script.Open_Genshin,args=(10,)).start()
    time.sleep(1)
    threading.Thread(target=script.Open_StarRail,args=(10,)).start()

    """反覆操作預計之後使用scapy進行封包修改操作"""
    # Jkf論壇使用體力藥水(此腳本就是藥水全部都用完)
    #forum.jkf_use_props(5)

    # Jkf論壇自動挖礦(次數,地點,運行完停留時間)
    # 地點 : "巨龍巢穴" "精靈峽谷" "廢棄礦坑"
    #forum.jkf_mining(10,"廢棄礦坑",5)

    # Jkf論壇自動探索(次數,地點,運行完停留時間)
    # 地點 : "墮落聖地" "焚燒之地" "巨木森林"
    #forum.jkf_explore(10,"巨木森林",5)

    # 輸出Cookie內容的方法 資料位置 , 要開啟的Cookie檔案名
    #GetParametric().CookieView("blackdefault","blackCookies")

    # 刪除 selenium 非正常關閉時,的遺留資料夾
    # TrashRemoval()