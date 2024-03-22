from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from Script.Parameters import paramet
from Script import paramet, DO , DI
from selenium import webdriver
from bs4 import BeautifulSoup
import time

class JKF_forum:
    def __init__(self):
        self.driver = webdriver.Chrome(options=paramet.AddSet("Jkf"))

    def Login_Confirm(self):
        self.driver.get("https://www.jkforum.net/forum.php?mod=forum")
        self.driver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')

        try:
            WebDriverWait(self.driver,1).until(EC.presence_of_element_located((By.XPATH, "//span[@class='circleHead']/img")))
        except:
            try:
                for cookie in DI.get_website_cookie("jkf"):
                    self.driver.add_cookie(cookie)
                self.driver.refresh()
            except:
                input("等待自行登入完成(Enter) : ")
                DO.json_cookie(self.driver.get_cookies(), "Jkf")

    # 使用藥水
    def jkf_use_props(self):
        self.Login_Confirm()
        self.driver.get("https://www.jkforum.net/material/my_item")

        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@class='router-link-active router-link-exact-active block lv-2-tab']")))
        except:
            pass

        Content = self.driver.page_source.encode('utf-8').strip()
        html = BeautifulSoup(Content,'html.parser')

        try: # 使用小型體力藥水
            smallpotion = WebDriverWait(self.driver,5).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'item-wrap') and .//div[contains(text(), '小型體力藥水')]]//button[contains(text(), '查看')]")))
            smallpotion.click()

            SmallPotionQuantity = html.select_one("div.item-wrap:-soup-contains('小型體力藥水') div.text-white.absolute.bottom-0.right-3.CENnO4Uu4CssJR9PLmCG").text
            Quantity = int(SmallPotionQuantity.split("x")[1])

            if Quantity < 1:
                raise Exception()

            for _ in range(Quantity):

                potionuse = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='OvtXIlmLtXEE_eWpy1jH px-4']")))
                potionuse.click()

                confirm = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='OvtXIlmLtXEE_eWpy1jH px-4'][text()='確認']")))
                confirm.click()
        except:pass

        try: # 使用中型藥水
            mediumpotion = WebDriverWait(self.driver,5).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'item-wrap') and .//div[contains(text(), '中型體力藥水')]]//button[contains(text(), '查看')]")))
            mediumpotion.click()

            MediumPotionQuantity = html.select_one("div.item-wrap:-soup-contains('中型體力藥水') div.text-white.absolute.bottom-0.right-3.CENnO4Uu4CssJR9PLmCG").text
            Quantity = int(MediumPotionQuantity.split("x")[1])

            if Quantity < 1:
                raise Exception()

            for _ in range(Quantity):
                potionuse = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='OvtXIlmLtXEE_eWpy1jH px-4']")))
                potionuse.click()

                confirm = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='OvtXIlmLtXEE_eWpy1jH px-4'][text()='確認']")))
                confirm.click()
        except:pass

        self.driver.quit()

    # 挖礦功能
    def jkf_mining(self, Quantity, Location):
        self.Login_Confirm()
        self.driver.get("https://www.jkforum.net/material/mining")

        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@class='router-link-active router-link-exact-active block lv-2-tab']")))
        except:
            pass

        match Location:
            case "巨龍巢穴":Location = 1
            case "精靈峽谷":Location = 2
            case "廢棄礦坑":Location = 3

        # 根據選擇的區域,點選開始挖礦
        startmining =  WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH, f"//div[@class='pt-10'][{Location}] //div[@class='OvtXIlmLtXEE_eWpy1jH YOKk3zC9K8EXQZUZPFiy'][text()='開始挖礦']")))
        startmining.click()

        try:
            # 先點選5次畫布,因為使用相對位置找不到,所以用絕對位置,可能之後需要修改
            mining = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div[1]/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/div/div[2]/canvas")))
            for _ in range(5):self.driver.execute_script("arguments[0].click();", mining)

            # 按再一次
            for _ in range(Quantity-1): # 因為上面執行過一遍,這邊-1
                time.sleep(0.1)
                again = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='OvtXIlmLtXEE_eWpy1jH'][text()='再挖一次']")))
                again.click()
        except:pass

        self.driver.quit()

    # 探索功能
    def jkf_explore(self, Quantity, Location):
        self.Login_Confirm()
        self.driver.get("https://www.jkforum.net/material/terrain_exploration")

        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@class='router-link-active router-link-exact-active block lv-2-tab']")))
        except:
            pass

        match Location:
            case "墮落聖地":Location = 1
            case "焚燒之地":Location = 2
            case "巨木森林":Location = 3

        # 刪除那個會擋到按鈕的白痴NPC
        self.driver.execute_script('document.querySelector("img.w-full.h-auto").remove();')

        startexplore = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH, f"//div[@class='pt-10'][{Location}] //div[@class='OvtXIlmLtXEE_eWpy1jH YOKk3zC9K8EXQZUZPFiy'][text()='開始探索']")))
        startexplore.click()

        try:
            explore = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div[1]/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/div/div[2]/canvas")))
            for _ in range(5):self.driver.execute_script("arguments[0].click();", explore)

            for _ in range(Quantity-1): # 因為上面執行過一遍,這邊-1
                time.sleep(0.1)
                again = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='OvtXIlmLtXEE_eWpy1jH'][text()='再挖一次']")))
                again.click()
                # 如果被NPC元素擋到按鈕元素,可以使用JS的點擊
                #driver.execute_script("arguments[0].click();", again)
        except:pass

        self.driver.quit()

class Hoyoverse: 
    def Login_Confirm(self, timeout: int, webname: str, link: str, xpath: str) -> webdriver:
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

    # 原神使用兌換碼
    def Genshin_Impact_Gift(self, gift: list):
        Genshin = self.Login_Confirm(
            8,
            "Genshin",
            "https://genshin.hoyoverse.com/zh-tw/gift",
            "//span[@class='cdkey__user-btn']"
        )

        # 選取伺服器位置到亞洲
        select = WebDriverWait(Genshin, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='cdkey-select__btn']")))
        select.click()

        asia = WebDriverWait(Genshin, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='cdkey-select__menu']/div[3]")))
        asia.click()
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
            receive = WebDriverWait(Genshin, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='cdkey-form__submit']")))
            receive.click()

            # 點選兌換
            close = WebDriverWait(Genshin, 5).until(EC.element_to_be_clickable((By.XPATH, "//img[@class='cdkey-result__close']")))
            close.click()

            time.sleep(5)

        Genshin.quit()
        
    def Star_Rail(self, gift: list):
        StarRail = self.Login_Confirm(
            8,
            "StarRail",
            "https://hsr.hoyoverse.com/gift",
            "//span[@class='web-cdkey-user__btn']"
        )

        select = WebDriverWait(StarRail, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='web-cdkey-form__select--toggle']")))
        select.click()

        asia = WebDriverWait(StarRail, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='web-cdkey-form__select--menu cdkey-scrollbar']/div[3]")))
        asia.click()
        time.sleep(1)

        for key in gift:
            cdkey = WebDriverWait(StarRail, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='web_cdkey_code']")))
            cdkey.click()

            cdkey.clear()
            cdkey.send_keys(key)

            receive = WebDriverWait(StarRail, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='web-cdkey-form__submit']")))
            receive.click()

            close = WebDriverWait(StarRail, 5).until(EC.element_to_be_clickable((By.XPATH, "//img[@class='closeBtn']")))
            close.click()

            time.sleep(5)

        StarRail.quit()

if __name__ == "__main__":    
    # jkf = JKF_forum()

    #? Jkf論壇使用體力藥水(此腳本就是藥水全部都用完)
    # jkf.jkf_use_props()

    #? Jkf論壇自動挖礦(次數 , 地點)
    #? 地點 : "巨龍巢穴" "精靈峽谷" "廢棄礦坑"
    # jkf.jkf_mining(10, "廢棄礦坑")

    #? Jkf論壇自動探索(次數 , 地點)
    #? 地點 : "墮落聖地" "焚燒之地" "巨木森林"
    # jkf.jkf_explore(10, "巨木森林")

    """===================="""

    hoyo = Hoyoverse()

    #? 原神輸入兌換碼
    # hoyo.Genshin_Impact_Gift([
    # ])

    #? 崩鐵輸入兌換碼
    hoyo.Star_Rail([
    ])