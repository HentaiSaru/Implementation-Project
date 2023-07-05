from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from Script.Parameters import paramet
from Script.Dataio import DO , DI
from selenium import webdriver
from lxml import etree
import threading
import time
import os

class AutomaticCheckin:
    def __init__(self):   
        self.exist = False
    
    def login_Confirm(self, link: str, webname: str, timeout: int, element: str, newdriver: bool = True, trylogin: bool = True):
        """
        * link = 開啟的網址
        * webname = 網頁名稱
        * timeout = 等待超時
        * element = 等待元素
        * newdriver = 啟動新驅動進行檢測
        * trylogin = 嘗試使用 Cookie 登入
        """
        
        if newdriver:
            driver = webdriver.Chrome(options=paramet.AddSet(webname))
            driver.get(link)
            driver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')
        else:
            driver = link
        
        try:
            WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, element)))
        except:
            try:
                if trylogin:
                    for cookie in DI.get_website_cookie(webname):
                        driver.add_cookie(cookie)
                    driver.refresh()
                else:
                    pass
            except:
                input("自行登入完成後 => \n按下 (Enter) 確認 : ")
                DO.json_cookie(driver.get_cookies(), webname)
            
        DO.pkl_cookie(driver.get_cookies(), webname)
        
        if newdriver:
            return driver
        else:
            time.sleep(timeout)
            driver.quit()
    
    def Wuyong_Checkin(self):
        Wuyongdriver = self.login_Confirm(
            "https://wuyong.fun/",
            "wuyong",
            5,
            "//img[@class='avatar b2-radius']"
        )
        
        Wuyongbutton = WebDriverWait(Wuyongdriver,3).until(EC.element_to_be_clickable((By.XPATH, "//i[@class='b2font b2-gift-2-line ']")))
        Wuyongbutton.click()
        
        Wuyongdriver.quit()
    
    def Black_Checkin(self):
        blackdriver = self.login_Confirm(
            "https://black.is-best.site/plugin.php?id=gsignin:index",
            "black",
            5,
            "//div[@class='avt y']"
        )
        
        time.sleep(paramet.WaitingTime() + 0.7)
        blackdriver.refresh()
        
        for _ in range(3): # 新版測試
            blackbutton = WebDriverWait(blackdriver,3).until(EC.element_to_be_clickable((By.XPATH,"//a[@class='right']")))
            blackbutton.click()
            time.sleep(0.1)
            
        blackdriver.quit()
    
    def Zero_Checkin(self):
        Zerodriver = webdriver.Chrome(options=paramet.AddSet("zero"))
        Zerodriver.get("https://www.miaoaaa.com/sites/530.html")
        Zerodriver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')
        
        miaoaaabutton = WebDriverWait(Zerodriver,0).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='btn btn-arrow mr-2']")))
        miaoaaabutton.click()
        
        time.sleep(3)
        
        handles = Zerodriver.window_handles
        Zerodriver.switch_to.window(handles[-1])
        # url = Zerodriver.current_url
        
        self.login_Confirm(
            Zerodriver,
            "zero",
            8,
            "//div[@class='avt y']",
            newdriver=False,
        )
    
    def Genshin_Checkin(self):
        Genshindriver = self.login_Confirm(
            "https://act.hoyolab.com/ys/event/signin-sea-v3/index.html?act_id=e202102251931481",
            "Genshin",
            5,
            "//div[@class='mhy-hoyolab-account-block__avatar']" # 驗證元素待修正
        )
        
        # 點選簽到元素
        checkin_element = "//span[@class='components-home-assets-__sign-content-test_---red-point---2jUBf9']"
        
        # 關閉彈出窗口,如果有的話
        try:
            Genshinbutton = WebDriverWait(Genshindriver,2).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='components-home-assets-__sign-content-test_---red-point---2jUBf9']")))
            Genshinbutton.click()
        except:pass
        
        try: # 某確認框
            Genshinbutton = WebDriverWait(Genshindriver,2).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='mihoyo-cookie-tips__button mihoyo-cookie-tips__button--hk4e']")))
            Genshinbutton.click()
        except:pass
        
        # 取得 cookie 來判斷登入狀態
        cookies = Genshindriver.get_cookies()
        for cookie in cookies:
            if cookie["name"] == "account_id":
                self.exist = True
        
        # 點選簽到位置 (已經簽到的就會找不到,因此當沒找到時,要讓他跳過)     
        if self.exist:
            try:
                for _ in range(3): # 測試
                    Genshinbutton = WebDriverWait(Genshindriver,5).until(EC.element_to_be_clickable((By.XPATH, checkin_element)))
                    Genshinbutton.click()
            except:
                pass
        else:
            # cookie 登入
            # for cookie in DI.get_website_cookie("Genshin"):
                # Genshindriver.add_cookie(cookie)
            # Genshindriver.refresh()
            
            try:
                Genshinbutton = WebDriverWait(Genshindriver,5).until(EC.element_to_be_clickable((By.XPATH, checkin_element)))
                Genshinbutton.click()

                # 使用Twitter 登入 div[1] = Google ... div[4] == Twitter
                Genshinbutton = WebDriverWait(Genshindriver,5).until(EC.element_to_be_clickable((By.XPATH, "//div[4][@class='account-sea-third-party-login-item']//img[@class='account-sea-login-icon']")))
                Genshinbutton.click()

                # 獲取當前開啟的窗口名稱
                handles = Genshindriver.window_handles
                for handle in handles:
                    Genshindriver.switch_to.window(handle)
                    if "Twitter / 授權應用程式" in Genshindriver.title:
                        break
                    
                # 取得保存的帳號,密碼
                Acc = DI.get_acc()
                acc = Acc["Genshin_account"]
                pas = Acc["Genshin_password"]

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

                input("登入完成後 => \n按下 (Enter) 確認 : ")

                # 再次切回原窗口
                handles = Genshindriver.window_handles
                for handle in handles:
                    Genshindriver.switch_to.window(handle)
                    if "【原神】每日簽到" in Genshindriver.title:
                        break
                
                for _ in range(2):
                    Genshinbutton = WebDriverWait(Genshindriver,5).until(EC.element_to_be_clickable((By.XPATH, checkin_element)))
                    Genshinbutton.click()  

                DO.json_cookie(cookies , "Genshin")
            except:
                pass

        DO.pkl_cookie(cookies , "Genshin")
        Genshindriver.quit()
    
    def StarRail_Checkin(self):
        pass
    
if __name__ == "__main__":
    AC = AutomaticCheckin()
    
    #################################################
    # threading.Thread(target=AC.Black_Checkin).start()
    # time.sleep(paramet.WaitingTime() + 5)
    # threading.Thread(target=AC.Wuyong_Checkin).start()
    # time.sleep(1)
    # threading.Thread(target=AC.Zero_Checkin).start()
    # time.sleep(1)
    # threading.Thread(target=AC.Genshin_Checkin).start()