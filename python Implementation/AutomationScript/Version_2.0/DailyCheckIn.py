from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from Script.Parameters import paramet
from Script.Dataio import DO , DI
from selenium import webdriver
from lxml import etree
import threading
import time
import re

class AutomaticCheckin:
    def __init__(self):   
        self.exist = False
        self.offdelay = 5
    
    def login_Confirm(self, link: str, webname: str, timeout: int, element: str, imset: bool = True, headless: bool = False, trylogin: bool = True):
        """
        * link = 開啟的網址
        * webname = 網頁名稱
        * timeout = 等待超時
        * element = 等待元素
        * imset = 導入設置參數
        * headless = 使用無頭啟用
        * trylogin = 嘗試使用 Cookie 登入
        """
        
        if imset:
            driver = webdriver.Chrome(options=paramet.AddSet(webname, headless))
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
                input(f"網站 : {webname} , 自行登入完成後 => \n按下 (Enter) 確認 : ")
                DO.json_cookie(driver.get_cookies(), webname)
            
        # DO.pkl_cookie(driver.get_cookies(), webname)
        
        if imset:
            return driver
        else:
            time.sleep(timeout)
            driver.quit()
    
    def Wuyong_Checkin(self):
        Wuyongdriver = self.login_Confirm(
            "https://wuyong.fun/",
            "wuyong",
            5,
            "//img[@class='avatar b2-radius']",
        )
        
        Wuyongbutton = WebDriverWait(Wuyongdriver,3).until(EC.element_to_be_clickable((By.XPATH, "//i[@class='b2font b2-gift-2-line ']")))
        Wuyongbutton.click()
        
        time.sleep(self.offdelay)
        Wuyongdriver.quit()
    
    def Black_Checkin(self):
        blackdriver = self.login_Confirm(
            "https://black.is-best.site/plugin.php?id=gsignin:index",
            "black",
            5,
            "//div[@class='avt y']",
        )
        
        time.sleep(paramet.WaitingTime() + 0.7)
        blackdriver.refresh()
        
        for _ in range(3): # 新版測試
            blackbutton = WebDriverWait(blackdriver,3).until(EC.element_to_be_clickable((By.XPATH,"//a[@class='right']")))
            blackbutton.click()
            blackdriver.refresh()
        
        time.sleep(self.offdelay)
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
            imset=False,
            headless = True
        )
    
    def Genshin_Checkin(self):
        Genshin = self.login_Confirm(
            "https://act.hoyolab.com/ys/event/signin-sea-v3/index.html?act_id=e202102251931481",
            "Genshin",
            5,
            "//div[@class='mhy-hoyolab-account-block__avatar']" # 驗證元素待修正
        )
        
        # 關閉彈出窗口,如果有的話
        try:
            Genshinbutton = WebDriverWait(Genshin,3).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='components-home-assets-__sign-guide_---guide-close---2VvmzE']")))
            Genshinbutton.click()
        except:pass
        
        try: # 某確認框
            Genshinbutton = WebDriverWait(Genshin,3).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='mihoyo-cookie-tips__button mihoyo-cookie-tips__button--hk4e']")))
            Genshinbutton.click()
        except:pass
        
        # 取得 cookie 來判斷登入狀態
        cookies = Genshin.get_cookies()
        for cookie in cookies:
            if cookie["name"] == "account_id":
                self.exist = True
     
        # 這邊嘗試使用 cookie 狀態來判斷登入 , 與否
        if not self.exist: #! 測試
            # 第一次 嘗試 cookie 登入
            try:
                for cookie in DI.get_website_cookie("Genshin"):
                    Genshin.add_cookie(cookie)
                Genshin.refresh()
            except:pass
            
            time.sleep(2)
            tree = etree.fromstring(Genshin.page_source, etree.HTMLParser())
            login = tree.xpath("//img[@class='mhy-hoyolab-account-block__avatar-icon']")[0].get("src")
            
            # 二次確認登入狀態
            if re.match(r"data:image/png;base64,.*", login):
                try:
                    Genshinbutton = WebDriverWait(Genshin,5).until(EC.element_to_be_clickable((By.XPATH, "//img[@class='mhy-hoyolab-account-block__avatar-icon']")))
                    Genshinbutton.click()

                    # 使用Twitter 登入 div[1] = Google ... div[4] == Twitter
                    Genshinbutton = WebDriverWait(Genshin,5).until(EC.element_to_be_clickable((By.XPATH, "//div[4][@class='account-sea-third-party-login-item']//img[@class='account-sea-login-icon']")))
                    Genshinbutton.click()

                    # 獲取當前開啟的窗口名稱
                    handles = Genshin.window_handles
                    for handle in handles:
                        Genshin.switch_to.window(handle)
                        if "Twitter / 授權應用程式" in Genshin.title:
                            break
                        
                    # 取得保存的帳號,密碼
                    Acc = DI.get_acc()
                    acc = Acc["Genshin_account"]
                    pas = Acc["Genshin_password"]

                    # 輸入帳號
                    accountbutton = WebDriverWait(Genshin, 3).until(EC.element_to_be_clickable((By.XPATH,"//input[@class='text']")))
                    accountbutton.click()
                    accountbutton.send_keys(acc)

                    # 輸入密碼
                    passwordbutton = WebDriverWait(Genshin, 3).until(EC.element_to_be_clickable((By.XPATH,"//input[@class='password text']")))
                    passwordbutton.click()
                    passwordbutton.send_keys(pas)

                    # 送出
                    loginbutton = WebDriverWait(Genshin, 3).until(EC.element_to_be_clickable((By.XPATH,"//input[@class='submit button selected']")))
                    loginbutton.click()


                    input("原神登入完成後 => \n按下 (Enter) 確認 : ")

                    #! 再次切回原窗口 (測試)
                    handles = Genshin.window_handles
                    for handle in handles:
                        Genshin.switch_to.window(handle)
                        if "【原神】每日簽到" in Genshin.title:
                            break

                    DO.json_cookie(cookies , "Genshin")
                except:
                    pass
        
        # 點選簽到位置 (已經簽到的就會找不到, 因此當沒找到時, 要讓他跳過)     
        try:
            Genshinbutton = WebDriverWait(Genshin, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='components-home-assets-__sign-content-test_---red-point---2jUBf9']")))
            for _ in range(3): # 測試
                Genshinbutton.click()
                time.sleep(1)
        except:
            pass

        # DO.pkl_cookie(cookies , "Genshin")
        time.sleep(self.offdelay)
        Genshin.quit()
    
    def StarRail_Checkin(self):
        StarRail = self.login_Confirm(
            "https://act.hoyolab.com/bbs/event/signin/hkrpg/index.html?act_id=e202303301540311&hyl_auth_required=true&hyl_presentation_style=fullscreen&lang=zh-tw&plat_type=pc",
            "StarRail",
            5,
            "//div[@class='mhy-hoyolab-account-block__avatar']" # 無效的登入檢測
        )
        
        try: # 關閉彈出窗口
            StarRailClos = WebDriverWait(StarRail, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='components-pc-assets-__dialog_---dialog-close---3G9gO2']")))
            StarRailClos.click()
        except:pass
        
        # 獲取登入帳戶圖標連結
        tree = etree.fromstring(StarRail.page_source, etree.HTMLParser())
        login = tree.xpath("//img[@class='mhy-hoyolab-account-block__avatar-icon']")[0].get("src")
        
        # 第一次嘗試 cookie 進行登入 (匹配成功代表未登入)
        if re.match(r"data:image/png;base64,.*", login):
            try:
                for cookie in DI.get_website_cookie("StarRail"):
                    StarRail.add_cookie(cookie)
                StarRail.refresh()
            except:pass
        
            # 第二次再檢測如果未登入 , 再使用登入操作
            time.sleep(2)
            tree = etree.fromstring(StarRail.page_source, etree.HTMLParser())
            login = tree.xpath("//img[@class='mhy-hoyolab-account-block__avatar-icon']")[0].get("src")
            
            if re.match(r"data:image/png;base64,.*", login):
                # 點選登入
                loginclick = WebDriverWait(StarRail, 3).until(EC.element_to_be_clickable((By.XPATH, "//img[@class='mhy-hoyolab-account-block__avatar-icon']")))
                loginclick.click()

                # 使用FaceBook登入 , div[3] 是fb
                loginbutton = WebDriverWait(StarRail, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[3][@class='account-sea-third-party-login-item']//img[@class='account-sea-login-icon']")))
                loginbutton.click()

                Acc = DI.get_acc()
                acc = Acc["StarRail_account"]
                pas = Acc["StarRail_password"]

                time.sleep(2)
                # 切換操作窗口
                handles = StarRail.window_handles
                for handle in handles:
                    StarRail.switch_to.window(handle)

                try: # 嘗試進行輸入帳號登入
                    accountbutton = WebDriverWait(StarRail, 3).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='email']")))
                    accountbutton.click()
                    accountbutton.send_keys(acc)

                    passwordbutton = WebDriverWait(StarRail, 3).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='pass']")))
                    passwordbutton.click()
                    passwordbutton.send_keys(pas)

                    loginbutton = WebDriverWait(StarRail, 3).until(EC.element_to_be_clickable((By.XPATH,"//input[@name='login']")))
                    loginbutton.click()
                except:
                    passwordbutton = WebDriverWait(StarRail, 3).until(EC.element_to_be_clickable((By.XPATH,"//input[@name='pass']")))
                    passwordbutton.click()
                    passwordbutton.send_keys(pas)

                    continuebutton = WebDriverWait(StarRail, 3).until(EC.element_to_be_clickable((By.XPATH,"//label[@class='uiButton uiButtonConfirm uiButtonLarge']")))
                    continuebutton.click()

                while True: # 採用另一種方式切換
                    handles = StarRail.window_handles
                    for handle in handles:
                        StarRail.switch_to.window(handle)
                        if "《崩壞：星穹鐵道》每日簽到" in StarRail.title:
                            break
                        else:
                            time.sleep(0.5)
                    break
                
                #! 等待 (測試)
                input("星鐵登入完成後 => \n按下 (Enter) 確認 : ")
                DO.json_cookie(StarRail.get_cookies() , "StarRail")
        
        while True:
            try:
                # 取得當前簽到時間 + 1
                checkinday = int(tree.xpath("//p[@class='components-pc-assets-__main-module_---day---3Q5I5A day']/span/text()")[0])+1
                # 尋找 + 1 後的天數 , 就是要簽到的時間
                checkin = WebDriverWait(StarRail, 3).until(EC.element_to_be_clickable((By.XPATH, f"//span[@class='components-pc-assets-__prize-list_---no---3smN44'][contains(text(), '第{checkinday}天')]")))
                
                if checkin:
                    checkin.click()
                    break
                time.sleep(0.5)
            except:pass
        
        time.sleep(self.offdelay)
        StarRail.quit()
    
if __name__ == "__main__":
    AC = AutomaticCheckin()
    
    #################################################
    threading.Thread(target=AC.Black_Checkin).start()
    time.sleep(paramet.WaitingTime() + 5)
    threading.Thread(target=AC.Wuyong_Checkin).start()
    time.sleep(5)
    threading.Thread(target=AC.Zero_Checkin).start()
    time.sleep(5)
    threading.Thread(target=AC.Genshin_Checkin).start()
    time.sleep(5)
    threading.Thread(target=AC.StarRail_Checkin).start()