from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from Script.Parameters import paramet
from Script import paramet, DO , DI
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
import threading
import string
import random
import math
import time
import os

class JKF:
    def __init__(self):
        self.driver = None

    def click_operate(self, Driver, Xpath, Wait=10):
        button =  WebDriverWait(Driver, Wait).until(EC.element_to_be_clickable((By.XPATH, Xpath)))
        button.click()

    def JKF_Login_Confirm(self, Jump):
        self.driver = webdriver.Chrome(options=paramet.AddSet("Jkf"))
        self.driver.get("https://www.jkforum.net/forum.php?mod=forum")
        self.driver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')

        try:
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//span[@class='circleHead']/img")))
        except:
            try:
                for cookie in DI.get_website_cookie("jkf"):
                    self.driver.add_cookie(cookie)
                self.driver.refresh()

                WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//span[@class='circleHead']/img")))
            except:
                input("等待自行登入完成(Enter) : ")
                DO.json_cookie(self.driver.get_cookies(), "Jkf")

        # 等待文件載入完成
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

        self.driver.get(Jump)

    # 使用藥水
    def jkf_use_props(self):
        self.JKF_Login_Confirm("https://www.jkforum.net/material/my_item")

        #self.driver.execute_script("document.querySelector('.p-3').scrollBy(0, 200)") 滾動
        try:
            WebDriverWait(self.driver, 8).until(EC.presence_of_element_located((By.XPATH, "//a[@class='router-link-active router-link-exact-active block lv-2-tab']")))
        except:
            pass

        Content = self.driver.page_source.encode('utf-8').strip()
        html = BeautifulSoup(Content, 'html.parser')

        try: # 使用小型體力藥水
            self.click_operate(self.driver, "//div[contains(@class, 'item-wrap') and .//div[contains(text(), '小型體力藥水')]]//button[contains(text(), '查看')]")

            SmallPotionQuantity = html.select_one("div.item-wrap:-soup-contains('小型體力藥水') div.text-white.absolute.bottom-0.right-3.CENnO4Uu4CssJR9PLmCG").text
            Quantity = int(SmallPotionQuantity.split("x")[1])

            if Quantity < 1:
                raise Exception()

            for _ in range(Quantity):
                self.click_operate(self.driver, "//div[@class='OvtXIlmLtXEE_eWpy1jH px-4']", 5)
                self.click_operate(self.driver, "//div[@class='OvtXIlmLtXEE_eWpy1jH px-4'][text()='確認']", 5)

        except:pass

        try: # 使用中型藥水
            self.click_operate(self.driver, "//div[contains(@class, 'item-wrap') and .//div[contains(text(), '中型體力藥水')]]//button[contains(text(), '查看')]")

            MediumPotionQuantity = html.select_one("div.item-wrap:-soup-contains('中型體力藥水') div.text-white.absolute.bottom-0.right-3.CENnO4Uu4CssJR9PLmCG").text
            Quantity = int(MediumPotionQuantity.split("x")[1])

            if Quantity < 1:
                raise Exception()

            for _ in range(Quantity):
                self.click_operate(self.driver, "//div[@class='OvtXIlmLtXEE_eWpy1jH px-4']", 5)
                self.click_operate(self.driver, "//div[@class='OvtXIlmLtXEE_eWpy1jH px-4'][text()='確認']", 5)

        except:pass

        self.driver.quit()

    # 挖礦功能
    def jkf_mining(self, Quantity, Point):
        self.JKF_Login_Confirm("https://www.jkforum.net/material/mining")

        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@class='router-link-active router-link-exact-active block lv-2-tab']")))
        except:
            pass
            
        location = {
            "巨龍巢穴": 1,
            "精靈峽谷": 2,
            "廢棄礦坑": 3,
        }
        
        consume = {
            "巨龍巢穴": 10,
            "精靈峽谷": 5,
            "廢棄礦坑": 1,
        }

        # 根據選擇的區域,點選開始挖礦
        self.click_operate(self.driver, f"//div[@class='pt-10'][{location[Point]}] //div[@class='OvtXIlmLtXEE_eWpy1jH YOKk3zC9K8EXQZUZPFiy'][text()='開始挖礦']")

        try:
            # 先點選5次畫布,因為使用相對位置找不到,所以用絕對位置,可能之後需要修改
            mining = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div[1]/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/div/div[2]/canvas")))
            for _ in range(5):
                self.driver.execute_script("arguments[0].click();", mining)

            self.click_operate(self.driver, "//div[@class='OvtXIlmLtXEE_eWpy1jH'][text()='再挖一次']")
            stamina = self.driver.execute_script("return document.querySelector('.inline-block.px-1').nextSibling.textContent")
            Quantity = math.floor(int(stamina) / consume[Point]) if Quantity == 0 else Quantity

            for _ in range(Quantity-1):
                time.sleep(0.3)
                self.click_operate(self.driver, "//div[@class='OvtXIlmLtXEE_eWpy1jH'][text()='再挖一次']")

        except:pass

        self.driver.quit()

    # 探索功能
    def jkf_explore(self, Quantity, Point):
        self.JKF_Login_Confirm("https://www.jkforum.net/material/terrain_exploration")

        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@class='router-link-active router-link-exact-active block lv-2-tab']")))
        except:
            pass

        location = {
            "墮落聖地": 1,
            "焚燒之地": 2,
            "巨木森林": 3,
        }

        consume = {
            "墮落聖地": 10,
            "焚燒之地": 5,
            "巨木森林": 1,
        }

        # 刪除那個會擋到按鈕的白痴NPC
        self.driver.execute_script('document.querySelector("img.w-full.h-auto").remove();')

        self.click_operate(self.driver, f"//div[@class='pt-10'][{location[Point]}] //div[@class='OvtXIlmLtXEE_eWpy1jH YOKk3zC9K8EXQZUZPFiy'][text()='開始探索']")

        try:
            explore = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div[1]/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/div/div[2]/canvas")))
            for _ in range(5):
                self.driver.execute_script("arguments[0].click();", explore)

            self.click_operate(self.driver, "//div[@class='OvtXIlmLtXEE_eWpy1jH'][text()='再挖一次']")
            stamina = self.driver.execute_script("return document.querySelector('.inline-block.px-1').nextSibling.textContent")
            Quantity = math.floor(int(stamina) / consume[Point]) if Quantity == 0 else Quantity

            for _ in range(Quantity-1):
                time.sleep(0.3)
                self.click_operate(self.driver, "//div[@class='OvtXIlmLtXEE_eWpy1jH'][text()='再挖一次']")
                # 如果被NPC元素擋到按鈕元素,可以使用JS的點擊
                # driver.execute_script("arguments[0].click();", again)

        except:pass

        self.driver.quit()

class EHentai:
    def __init__(self):
        self.driver = None
        self.cache = r"R:\EHentaiCache"
        self.delay = lambda: round(random.uniform(1.1, 2.2), 1)
        self.generate_str = string.digits + string.ascii_letters
        self.clearcache = lambda: os.system(f"rd /s /q {self.cache}")
        
        self.getCookieScript = """
            if (document.body.getAttribute("keydown-getCookie")) return;
            
            const allow = new Set(["igneous", "ipb_member_id", "ipb_pass_hash"]);

            window.addEventListener("keydown", event => {
                if (event.altKey && event.key.toLowerCase() == "g") {
                    event.preventDefault();

                    const cookieDict = document.cookie.split("; ").reduce((acc, cookie) => {
                        const [name, value] = cookie.split("=");
                        allow.has(name) && acc.push({ name, value });
                        return acc;
                    }, []);

                    cookieDict.push({ name: "sl", value: "dm_2" });

                    if (confirm("是否複製 Cookie?")) {
                        const referSort = ["igneous", "ipb_member_id", "ipb_pass_hash", "sl"];
                        const sortedDict = cookieDict.sort((a, b) => {
                            const indexA = referSort.indexOf(a.name);
                            const indexB = referSort.indexOf(b.name);
                            return (indexA === -1 ? Infinity : indexA) - (indexB === -1 ? Infinity : indexB);
                        });

                        navigator.clipboard.writeText(JSON.stringify(sortedDict))
                            .then(() => {
                                alert("Cookie 已複製到剪貼簿！");
                            })
                            .catch(err => {
                                console.error("複製剪貼簿失敗：", err);
                            });
                    }
                }
            });

            document.body.setAttribute("keydown-getCookie", true);
        """

    def start(self, url):
        self.driver = webdriver.Chrome(options=paramet.AddSet("EHentai", userdata=self.cache))
        self.driver.get(url)
        self.driver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')
        
    def end(self):
        print("\n等待關閉中...\n")

        try:
            while self.driver.window_handles:
                try: self.driver.execute_script(self.getCookieScript) # 避免例外影響到正常運作使用 try
                except: pass

                time.sleep(3)
        except Exception as e: # 這邊很奇怪, 上面 quit 會直接跳例外
            self.driver.quit()
            self.clearcache()
            print("清除")

    def generator(self, Type="default"):
        merge = ""

        if Type == "default":
            for _ in range(16):
                merge += random.choice(self.generate_str)
        elif Type == "mail":
            for _ in range(8):
                merge += random.choice(self.generate_str)
            merge += "@gmail.com"

        return merge

    def send_operate(self, Input, Xpath):
        user =  WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, Xpath)))
        user.click()
        time.sleep(self.delay())
        user.send_keys(Input)

    def Regist(self, Save: str):
        """
        Save 設置註冊紀錄的路徑
        """
        self.start("https://forums.e-hentai.org/index.php?act=Reg&CODE=00")

        agree = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='agree_cbox']")))
        agree.click()

        register = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Register']")))
        time.sleep(self.delay())
        register.click()

        # 取得名稱
        name = self.generator()
        # 登入名稱
        self.send_operate(name, "//input[@id='reg-name']")
        # 顯示名稱
        self.send_operate(name, "//input[@id='reg-members-display-name']")

        # 取得密碼
        password = self.generator()
        #密碼
        self.send_operate(password, "//input[@id='reg-password']")
        #確認密碼
        self.send_operate(password, "//input[@id='reg-password-check']")

        # 取得信箱
        mail = self.generator("mail")
        #郵件
        self.send_operate(mail, "//input[@id='reg-emailaddress']")
        #確認郵件
        self.send_operate(mail, "//input[@id='reg-emailaddress-two']")

        input("自行輸入安全碼後確認 : ")

        #提交註冊
        submit =  WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit']")))
        submit.click()

        DO.json_record(Save, "Eh_註冊紀錄", {
            datetime.now().strftime("%Y-%m-%d-%H"): { # 取得時間
                "連線位置": "自行輸入",
                "帳號": name,
                "密碼": password,
                "信箱": mail,
            }
        })
        
        threading.Thread(target=self.end).start()

    def Login(self, Account: dict={}, Cookie: list=[], JumpEx=False):
        """
        Account 傳入一個字典
        格式: {'account': '', 'password': ''}
        
        Cookie 傳入一個列表
        格式: [{"name": "ipb_member_id", "value": ""}, {"name": "ipb_pass_hash", "value": ""}]
        
        JumpEx 自動跳轉到 Ex
        """

        # https://e-hentai.org/ 登入
        self.start("https://e-hentai.org/bounce_login.php?b=d&bt=1-1")

        if bool(Account):
            account = Account.get("account", None)
            password = Account.get("password", None)

            if account and password:
                self.send_operate(account, "//input[@name='UserName']")
                self.send_operate(password, "//input[@name='PassWord']")

                # input("機器人驗證 : ")
                submit =  WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='ipb_login_submit']")))
                submit.click()
            else:
                print("輸入正確的對應值: {'account': '', 'password': ''}")
                self.driver.quit()

        elif bool(Cookie): # 無驗證數據對錯
            for cookie in Cookie:
                self.driver.add_cookie(cookie)
            self.driver.get("https://e-hentai.org/")

        if JumpEx:
            self.driver.get("https://exhentai.org/")

        threading.Thread(target=self.end).start()

class Hoyoverse:
    def Hoyo_Login_Confirm(self, timeout: int, webname: str, link: str, xpath: str) -> webdriver:
        """
        * timeout 等待元素出現的時間
        * webname 網站名稱
        * link 網頁連結
        * xpath 等待元素
        """
        driver = webdriver.Chrome(options=paramet.AddSet(webname))
        driver.get(link)
        driver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')

        try:
            WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        except:
            try:
                for cookie in DI.get_website_cookie(webname):
                    driver.add_cookie(cookie)
                driver.refresh()
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath)))
            except:
                input(f"網站 : {webname} , 自行登入完成後 => \n按下 (Enter) 確認 : ")

        DO.json_cookie(driver.get_cookies(), webname)
        return driver

    def click_operate(self, Driver, Xpath, Wait=10):
        button =  WebDriverWait(Driver, Wait).until(EC.element_to_be_clickable((By.XPATH, Xpath)))
        button.click()

    # 原神使用兌換碼
    def Genshin_Impact_Gift(self, gift: list):
        Genshin = self.Hoyo_Login_Confirm(
            8,
            "Genshin",
            "https://genshin.hoyoverse.com/zh-tw/gift",
            "//span[@class='cdkey__user-btn']"
        )

        # 選取伺服器位置到亞洲
        self.click_operate(Genshin, "//div[@class='cdkey-select__btn']")
        self.click_operate(Genshin, "//div[@class='cdkey-select__menu']/div[3]")
        time.sleep(1)

        for key in gift: #! 懶得寫判斷不是列表的狀況
            cdkey = WebDriverWait(Genshin, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='cdkey__code']")))
            cdkey.click()

            #? 不知道為什麼不能用 clear 清除文字, 只好使用全選刪除後再輸入
            cdkey.send_keys(Keys.CONTROL + "a")
            cdkey.send_keys(Keys.BACKSPACE)
            # 輸入兌換碼
            cdkey.send_keys(key)

            # 關閉兌換成功或失敗窗口
            self.click_operate(Genshin, "//button[@class='cdkey-form__submit']")
            # 點選兌換
            self.click_operate(Genshin, "//img[@class='cdkey-result__close']")

            time.sleep(5)

        Genshin.quit()
        
    def Star_Rail(self, gift: list):
        StarRail = self.Hoyo_Login_Confirm(
            8,
            "StarRail",
            "https://hsr.hoyoverse.com/gift",
            "//span[@class='web-cdkey-user__btn']"
        )

        self.click_operate(StarRail, "//div[@class='web-cdkey-form__select--toggle']")
        self.click_operate(StarRail, "//div[@class='web-cdkey-form__select--menu cdkey-scrollbar']/div[3]")
        time.sleep(1)

        for key in gift:
            cdkey = WebDriverWait(StarRail, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='web_cdkey_code']")))
            cdkey.click()

            cdkey.clear()
            cdkey.send_keys(key)

            self.click_operate(StarRail, "//button[@class='web-cdkey-form__submit']")
            self.click_operate(StarRail, "//img[@class='closeBtn']")

            time.sleep(5)

        StarRail.quit()

class Main(JKF, EHentai, Hoyoverse):
    def __init__(self):
        JKF.__init__(self)
        EHentai.__init__(self)
        Hoyoverse.__init__(self)

if __name__ == "__main__":
    main = Main()

    #? Jkf論壇使用體力藥水(此腳本就是藥水全部都用完)
    # main.jkf_use_props()

    #? Jkf論壇自動挖礦(次數 , 地點) 次數 0 = 體力用完
    #? 地點 : "巨龍巢穴" "精靈峽谷" "廢棄礦坑"
    # main.jkf_mining(10, "廢棄礦坑")

    #? Jkf論壇自動探索(次數 , 地點) 次數 0 = 體力用完
    #? 地點 : "墮落聖地" "焚燒之地" "巨木森林"
    # main.jkf_explore(10, "巨木森林")

    """===================="""

    #? 註冊 E-Hentai 與 登入
    # main.Regist("R:/")

    Cookie = DI.get_json(fr"{os.getcwd()}\EhCookie.json")
    # Cookie["鳳凰城"]
    # Cookie["布法羅"]

    # main.Login(Cookie=Cookie["鳳凰城"])

    """===================="""

    #? 原神輸入兌換碼
    # main.Genshin_Impact_Gift([
    # ])

    #? 崩鐵輸入兌換碼
    # main.Star_Rail([
    # ])