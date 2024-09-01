from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from Script import paramet, DO , DI
from concurrent.futures import *
from selenium import webdriver
from lxml import etree
import threading
import inspect
import time
import re

class AutomaticCheckin:
    def __init__(self):
        self.tree = None
        self.offdelay = 5
        self.Alone = threading.local()

    # 等待網頁載入完成
    def LoadWait(self, driver, waittime):
        WebDriverWait(driver, 20).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        time.sleep(waittime / 2) # 某些用 Ajex 生成的, 目前沒很好的檢測方法

    # 等待可點擊元素出現 (開啟頁面, 等待時間, 等待元素)
    def ClickWait(self, driver, timeout: int, xpath: str):
        Element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return Element

    # icon 的驗證函數 (開啟頁面, 查找 icon 元素的 xpath)
    def IconVerify(self, element: str) -> bool:
        login = self.tree.xpath(element)[0].get("src")
        # 當匹配成功是預設 base64 貼圖, 代表沒有登入成功
        return not re.match(r"data:image/png;base64,.*", login)

    # Cookie 的驗證函數 (開啟頁面, 驗證 是否存在的類型)
    def CookieVerify(self, driver, value: str) -> bool:
        return any(cookie["name"] == value for cookie in driver.get_cookies())

    # 驗證回傳數據是否同源
    def NotSameOrigin(self, origin: str) -> bool:
        return not (origin == inspect.stack()[1].function)

    # 驗證登入
    def Login_Confirm(self,
        webname: str,
        link: str,
        verify_method: dict,
        needset: bool = True,
        headless: bool = False,
        trylogin: bool = True
    ):
        """
        * webname = 網頁名稱
        * link = 開啟的連結
        * verify_method (沒有寫對於參數錯誤的驗證):
        {"type": "", "value": "", "waittime": 5}
        type 可以傳入的類型, icon | xpath | cookie, value 驗證搭配值, waittime 等待時間
        * needset = 使否導入設置參數
        * headless = 使用無頭啟用
        * trylogin = 嘗試使用 Cookie 登入
        """
        
        [Type, value, waittime] = [ # 解構驗證參數
            verify_method.get("type"), verify_method.get("value"), verify_method.get("waittime")
        ]

        if needset:
            driver = webdriver.Chrome(options=paramet.AddSet(webname, headless))
            driver.get(link)
            self.LoadWait(driver, waittime)
            self.tree = etree.fromstring(driver.page_source, etree.HTMLParser())
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        else:
            driver = link

        verify = { # 驗證方法的類型 (寫在這裡並沒有很好, 但我懶得傳參數給 lambda)
            "icon": lambda: self.IconVerify(value),
            "xpath": lambda: WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.XPATH, value))),
            "cookie": lambda: self.CookieVerify(driver, value),
        }

        try:
            if not verify[Type.lower()](): raise Exception("驗證失敗")
        except:
            try:
                if trylogin:
                    for cookie in DI.get_website_cookie(webname):
                        driver.add_cookie(cookie)
                    driver.refresh()
                    self.LoadWait(driver, waittime)
                    if not verify[Type.lower()](): raise Exception("驗證失敗")
                else: raise Exception("無嘗試登入")
            except:
                input(f"網站 : {webname} , 自行登入完成後 => \n按下 (Enter) 確認 : ")

        DO.json_cookie(driver.get_cookies(), webname)

        if needset:
            return driver, inspect.stack()[1].function # 回傳操作的驅動, 與調用他的函數名稱
        else:
            time.sleep(waittime)
            driver.quit()

    def Wuyong(self):
        self.Alone.driver, Caller = self.Login_Confirm(
            "wuyong",
            "https://wuyong.fun/#google_vignette",
            {
                "type": "xpath",
                "value": "//img[@class='avatar b2-radius']",
                "waittime": 8
            }
        )

        if self.NotSameOrigin(Caller):
            print(f"錯誤數據來自: {Caller}\n禁止非同原操作")
            self.Alone.driver.quit()

        # 關閉額外彈窗
        self.Alone.driver.execute_script("setInterval(() => {document.querySelector('#dismiss-button')?.click()}, 800);")
        # 使用 Js 方式點擊簽到 (避免被擋住)
        CheckinButton = self.ClickWait(self.Alone.driver, 3, "//i[@class='b2font b2-gift-2-line ']")
        self.Alone.driver.execute_script("arguments[0].click();", CheckinButton)

        time.sleep(self.offdelay)
        self.Alone.driver.quit()

    def TwApk(self):
        self.Alone.driver, Caller = self.Login_Confirm(
            "TwApk",
            "https://apk.tw/forum.php",
            {
                "type": "xpath",
                "value": "//div[@class='avt y']",
                "waittime": 8
            }
        )

        if self.NotSameOrigin(Caller):
            print(f"錯誤數據來自: {Caller}\n禁止非同原操作")
            self.Alone.driver.quit()

        try: # 已經簽到的會報錯
            CheckinButton = self.ClickWait(self.Alone.driver, 5, "//a[@id='my_amupper']")
            CheckinButton.click()
        except:pass

        time.sleep(self.offdelay)
        self.Alone.driver.quit()

    def Zero(self):
        Zero = webdriver.Chrome(options=paramet.AddSet("zero"))
        Zero.get("https://zerobyw.github.io/")
        Zero.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')

        Jump = self.ClickWait(Zero, 5, "//li[@class='layui-timeline-item']//button")
        Jump.click()

        time.sleep(5) # 愚蠢的等待方式
        handles = Zero.window_handles
        Zero.switch_to.window(handles[-1])

        self.Login_Confirm(
            "zero",
            Zero,
            {
                "type": "xpath",
                "value": "//img[@class='user_avatar']",
                "waittime": 8
            },
            needset = False
        )

    def Genshin(self):
        self.Alone.driver, Caller = self.Login_Confirm(
            "Genshin",
            "https://act.hoyolab.com/ys/event/signin-sea-v3/index.html?act_id=e202102251931481",
            {
                "type": "icon",
                "value": "//img[@class='mhy-hoyolab-account-block__avatar-icon']",
                "waittime": 8
            }
        )

        if self.NotSameOrigin(Caller):
            print(f"錯誤數據來自: {Caller}\n禁止非同原操作")
            self.Alone.driver.quit()

        # 關閉彈出窗口,如果有的話
        try:
            GenshinClose = self.ClickWait(self.Alone.driver, 3, "//span[@class='components-home-assets-__sign-guide_---guide-close---2VvmzE']")
            GenshinClose.click()
        except:pass

        try: # 某確認框
            GenshinConfirm = self.ClickWait(self.Alone.driver, 3, "//button[@class='mihoyo-cookie-tips__button mihoyo-cookie-tips__button--hk4e']")
            GenshinConfirm.click()
        except:pass

        # 點選簽到位置 (已經簽到的就會找不到, 因此當沒找到時, 要讓他跳過)
        try:
            while True:
                checkin = self.ClickWait(self.Alone.driver, 3, "//span[@class='components-home-assets-__sign-content-test_---red-point---2jUBf9']")
                if checkin:
                    checkin.click()
                    break
                time.sleep(0.5)
        except:
            pass

        time.sleep(self.offdelay)
        self.Alone.driver.quit()

    def StarRail(self):
        self.Alone.driver, Caller = self.Login_Confirm(
            "StarRail",
            "https://act.hoyolab.com/bbs/event/signin/hkrpg/index.html?act_id=e202303301540311",
            {
                "type": "icon",
                "value": "//img[@class='mhy-hoyolab-account-block__avatar-icon']",
                "waittime": 16
            }
        )

        if self.NotSameOrigin(Caller):
            print(f"錯誤數據來自: {Caller}\n禁止非同原操作")
            self.Alone.driver.quit()

        try: # 關閉彈出窗口
            StarRailClose = self.ClickWait(self.Alone.driver, 3, "//div[@class='components-pc-assets-__dialog_---dialog-close---3G9gO2']")
            StarRailClose.click()
        except:pass

        while True:
            try:
                # 取得當前簽到時間 + 1
                checkinday = int(self.tree.xpath("//p[@class='components-pc-assets-__main-module_---day---3Q5I5A day']/span/text()")[0])+1
                # 尋找 + 1 後的天數 , 就是要簽到的時間
                checkin = WebDriverWait(self.Alone.driver, 3).until(EC.element_to_be_clickable((By.XPATH, f"//span[@class='components-pc-assets-__prize-list_---no---3smN44'][contains(text(), '第{checkinday}天')]")))

                if checkin:
                    checkin.click()
                    break
                time.sleep(0.5)
            except:pass

        time.sleep(self.offdelay)
        self.Alone.driver.quit()

    def ZoneZero(self):
        self.Alone.driver, Caller = self.Login_Confirm(
            "ZoneZero",
            "https://act.hoyolab.com/bbs/event/signin/zzz/e202406031448091.html?act_id=e202406031448091",
            {
                "type": "icon",
                "value": "//img[@class='mhy-hoyolab-account-block__avatar-icon']",
                "waittime": 8
            }
        )

        if self.NotSameOrigin(Caller):
            print(f"錯誤數據來自: {Caller}\n禁止非同原操作")
            self.Alone.driver.quit()

        try: # 關閉彈出窗口
            ZoneZeroClose = self.ClickWait(self.Alone.driver, 3, "//div[@class='components-pc-assets-__dialog_---dialog-close---3G9gO2']")
            ZoneZeroClose.click()
        except:pass

        while True:
            try:
                # 取得當前簽到時間 + 1
                checkinday = int(self.tree.xpath("//p[@class='components-pc-assets-__main-module_---day---3Q5I5A day']/span/text()")[0])+1
                # 尋找 + 1 後的天數 , 就是要簽到的時間
                checkin = self.ClickWait(self.Alone.driver, 3, f"//span[@class='components-pc-assets-__prize-list_---no---3smN44'][contains(text(), '第{checkinday}天')]")

                if checkin:
                    checkin.click()
                    break
                time.sleep(0.5)
            except:pass

        time.sleep(self.offdelay)
        self.Alone.driver.quit()

if __name__ == "__main__":
    AC = AutomaticCheckin()

    # AC.Wuyong()
    # AC.TwApk()
    # AC.Zero()
    # AC.Genshin()
    # AC.StarRail()
    # AC.ZoneZero()

    with ThreadPoolExecutor(max_workers=100) as executor:
        for func, delay in zip([
            AC.Wuyong,
            AC.TwApk,
            AC.Zero,
            AC.Genshin,
            AC.StarRail,
            AC.ZoneZero
        ], [10, 10, 10, 10, 10, 1]): # 延遲設置 (設置太短可能造成資源競爭)
            executor.submit(func)
            time.sleep(delay)