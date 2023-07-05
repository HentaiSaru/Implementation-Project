from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from Script.Parameters import paramet
from Script.Dataio import DO , DI
from selenium import webdriver
from bs4 import BeautifulSoup
import time

class JKF_forum:
    def __init__(self):
        self.jkfdriver = webdriver.Chrome(options=paramet.AddSet("Jkf"))
    
    def login_Confirm(self): 
        self.jkfdriver.get("https://www.jkforum.net/forum.php?mod=forum")
        self.jkfdriver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')
        
        try:
            WebDriverWait(self.jkfdriver,1).until(EC.presence_of_element_located((By.XPATH, "//span[@class='circleHead']/img")))
        except:
            try:
                for cookie in DI.get_website_cookie("jkf"):
                    self.jkfdriver.add_cookie(cookie)
                self.jkfdriver.refresh()
            except:
                input("等待自行登入完成(Enter) : ")
                DO.json_cookie(self.jkfdriver.get_cookies(), "Jkf")
            
        DO.pkl_cookie(self.jkfdriver.get_cookies(), "Jkf")
        
    # 使用藥水
    def jkf_use_props(self):
        self.login_Confirm()
        self.jkfdriver.get("https://www.jkforum.net/material/my_item")

        try:
            WebDriverWait(self.jkfdriver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@class='router-link-active router-link-exact-active block lv-2-tab']")))
        except:
            pass
        
        Content = self.jkfdriver.page_source.encode('utf-8').strip()
        html = BeautifulSoup(Content,'html.parser')

        try: # 使用小型體力藥水
            smallpotion = WebDriverWait(self.jkfdriver,5).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'item-wrap') and .//div[contains(text(), '小型體力藥水')]]//button[contains(text(), '查看')]")))
            smallpotion.click()

            SmallPotionQuantity = html.select_one("div.item-wrap:-soup-contains('小型體力藥水') div.text-white.absolute.bottom-0.right-3.CENnO4Uu4CssJR9PLmCG").text
            Quantity = int(SmallPotionQuantity.split("x")[1])
            
            if Quantity < 1:
                raise Exception()

            for _ in range(Quantity):

                potionuse = WebDriverWait(self.jkfdriver,10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='OvtXIlmLtXEE_eWpy1jH px-4']")))
                potionuse.click()

                confirm = WebDriverWait(self.jkfdriver,10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='OvtXIlmLtXEE_eWpy1jH px-4'][text()='確認']")))
                confirm.click()
        except:pass

        try: # 使用中型藥水
            mediumpotion = WebDriverWait(self.jkfdriver,5).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'item-wrap') and .//div[contains(text(), '中型體力藥水')]]//button[contains(text(), '查看')]")))
            mediumpotion.click()

            MediumPotionQuantity = html.select_one("div.item-wrap:-soup-contains('中型體力藥水') div.text-white.absolute.bottom-0.right-3.CENnO4Uu4CssJR9PLmCG").text
            Quantity = int(MediumPotionQuantity.split("x")[1])
            
            if Quantity < 1:
                raise Exception()

            for _ in range(Quantity):
                potionuse = WebDriverWait(self.jkfdriver,10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='OvtXIlmLtXEE_eWpy1jH px-4']")))
                potionuse.click()

                confirm = WebDriverWait(self.jkfdriver,10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='OvtXIlmLtXEE_eWpy1jH px-4'][text()='確認']")))
                confirm.click()
        except:pass

        self.jkfdriver.quit()
        
    # 挖礦功能
    def jkf_mining(self, Quantity, Location):
        self.login_Confirm()
        self.jkfdriver.get("https://www.jkforum.net/material/mining")
        
        try:
            WebDriverWait(self.jkfdriver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@class='router-link-active router-link-exact-active block lv-2-tab']")))
        except:
            pass

        match Location:
            case "巨龍巢穴":Location = 1
            case "精靈峽谷":Location = 2
            case "廢棄礦坑":Location = 3

        # 根據選擇的區域,點選開始挖礦
        startmining =  WebDriverWait(self.jkfdriver,10).until(EC.element_to_be_clickable((By.XPATH, f"//div[@class='pt-10'][{Location}] //div[@class='OvtXIlmLtXEE_eWpy1jH YOKk3zC9K8EXQZUZPFiy'][text()='開始挖礦']")))
        startmining.click()

        try:
            # 先點選5次畫布,因為使用相對位置找不到,所以用絕對位置,可能之後需要修改
            mining = WebDriverWait(self.jkfdriver,10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div[1]/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/div/div[2]/canvas")))
            for _ in range(5):self.jkfdriver.execute_script("arguments[0].click();", mining)

            # 按再一次
            for _ in range(Quantity-1): # 因為上面執行過一遍,這邊-1
                time.sleep(0.1)
                again = WebDriverWait(self.jkfdriver,10).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='OvtXIlmLtXEE_eWpy1jH'][text()='再挖一次']")))
                again.click()
        except:pass

        self.jkfdriver.quit()

    # 探索功能
    def jkf_explore(self, Quantity, Location):
        self.login_Confirm()
        self.jkfdriver.get("https://www.jkforum.net/material/terrain_exploration")

        try:
            WebDriverWait(self.jkfdriver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@class='router-link-active router-link-exact-active block lv-2-tab']")))
        except:
            pass

        match Location:
            case "墮落聖地":Location = 1
            case "焚燒之地":Location = 2
            case "巨木森林":Location = 3

        # 刪除那個會擋到按鈕的白痴NPC
        self.jkfdriver.execute_script('document.querySelector("img.w-full.h-auto").remove();')

        startexplore = WebDriverWait(self.jkfdriver,10).until(EC.element_to_be_clickable((By.XPATH, f"//div[@class='pt-10'][{Location}] //div[@class='OvtXIlmLtXEE_eWpy1jH YOKk3zC9K8EXQZUZPFiy'][text()='開始探索']")))
        startexplore.click()

        try:
            explore = WebDriverWait(self.jkfdriver,10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div[1]/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/div/div[2]/canvas")))
            for _ in range(5):self.jkfdriver.execute_script("arguments[0].click();", explore)

            for _ in range(Quantity-1): # 因為上面執行過一遍,這邊-1
                time.sleep(0.1)
                again = WebDriverWait(self.jkfdriver,10).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='OvtXIlmLtXEE_eWpy1jH'][text()='再挖一次']")))
                again.click()
                # 如果被NPC元素擋到按鈕元素,可以使用JS的點擊
                #jkfdriver.execute_script("arguments[0].click();", again)
        except:pass

        self.jkfdriver.quit()

if __name__ == "__main__":    
    jkf = JKF_forum()

    # Jkf論壇使用體力藥水(此腳本就是藥水全部都用完)
    # jkf.jkf_use_props()

    # Jkf論壇自動挖礦(次數 , 地點)
    # 地點 : "巨龍巢穴" "精靈峽谷" "廢棄礦坑"
    # jkf.jkf_mining(10,"廢棄礦坑")

    # Jkf論壇自動探索(次數 , 地點)
    # 地點 : "墮落聖地" "焚燒之地" "巨木森林"
    jkf.jkf_explore(10,"巨木森林")