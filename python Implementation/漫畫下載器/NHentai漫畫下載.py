from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import chromedriver_autoinstaller
from lxml import etree
from tqdm import tqdm
import cloudscraper
import threading
import pyperclip
import requests
import keyboard
import random
import time
import sys
import re
import os
dir = os.path.abspath("R:/") # 可更改預設路徑
os.chdir(dir)

"""
    * 使用說明
    
    爬蟲適用網站 : https://nhentai.net/
    !! 下載速度慢是正常的 , 他是模擬人類操作 , 一頁一頁去下載圖片

    * 開發說明

    該網站的反爬機制,無法使用免費版的cloudscraper進行繞過,因此使用自動化操作
    有時候會被機器人驗證卡住 , 需要重新啟動 , 啟動無效可啟用 reset 方法

    一般的selenium自動化 , 無法繞過該網站的機器人驗證
    這邊使用的是 undetected_chromedriver , 這個雖然可通過驗證
    但個人對該庫的應用並不熟 , 無法使用多線程多開 , 故此當前是每一本都一個一個操作
    當批量下載時 , 速度會很感人

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Versions 1.0.0

    [+] 單本漫畫下載
    [+] 搜尋頁面下載
    [+] 自動擷取複製

    後續開發預想

    [*] 漫畫Tag分類
    [*] 指定Tag分類排除
    [*] GUI操作介面

"""

# 重置方法
def reset():
    print("重置中請稍後...")
    UserData = os.path.join(dir,"Data")
    os.system(f"RD /s /q {UserData} >nul 2>&1")
    os.system('wmic process where name="chrome.exe" delete >nul 2>&1')
    os.system("pip uninstall undetected_chromedriver -y >nul 2>&1")
    os.system("pip install undetected_chromedriver >nul 2>&1")
    os.system("python.exe -m pip install --upgrade pip >nul 2>&1")
    os.system("pip install --upgrade setuptools >nul 2>&1")
    os.system("pip install --upgrade wheel >nul 2>&1")
    print("重置完成...")
# 取得自動化操作設置
class Automation:
    def __init__(self,head):
        self.configuration = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),"drive")
        self.drivepath = os.path.join(self.configuration,'112','chromedriver.exe')
        self.UserData = os.path.join(dir,"Data")
        
        # 選項設置
        self.Settings = uc.ChromeOptions()
        if head:self.Settings.add_argument("--headless")
        self.Settings.add_argument(f"--remote-debugging-port={random.randint(1024,65535)}")
        self.Settings.add_argument("--disable-extensions")
        self.Settings.add_argument('--no-first-run --no-service-autorun --password-store=basic')

    # 創建驅動路徑(這樣後續開啟會比較快)
    def driver_creation(self):
        try:
            os.mkdir(self.configuration)
            chromedriver_autoinstaller.install(path=self.configuration)
        except:
            chromedriver_autoinstaller.install(path=self.configuration)

    # 當沒有找到驅動時會創建在當前路徑
    def browser(self):
        try:
            return uc.Chrome(
                version_main=112,
                options=self.Settings,
                driver_executable_path=self.drivepath,
                user_data_dir=self.UserData
            )
        except:
            self.driver_creation()
            return uc.Chrome(
                version_main=112,
                options=self.Settings,
                driver_executable_path=self.drivepath,
                user_data_dir=self.UserData
            )
# 漫畫主頁處理
class Verify:
    def __init__(self,enter,pages,head):
        self.search = r"https://nhentai\.net/.*"
        self.mangapage = r"https://nhentai\.net/g/\d+"
        self.correctbox = []
        self.pages = pages
        self.head = head
        
        print("開始操作請稍後...\n")
        if isinstance(enter,list):

            print("成功匹配...\n")
            # 將錯誤的網址格式排除
            for data in enter:
                if re.match(self.mangapage,data):
                    self.correctbox.append(data)
                else:pass

            # 將正確的網址導入請求
            if len(self.correctbox) != 0:
                self.run(self.correctbox)
            else:pass

        else:
            # 匹配搜尋頁面
            if re.match(self.search,enter):
                print("成功匹配...\n")

                Auto = Automation(self.head)
                browser = Auto.browser()

                if enter.find("?page") != -1:url = f"{enter.split('?page=')[0]}?page=1"
                else:url = f"{enter}?page=1"
                
                # 首次開啟
                browser.get(url)

                # 延遲載入
                WebDriverWait(browser,30).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='container index-container']")))

                html = etree.fromstring(browser.page_source,etree.HTMLParser())
                page = html.xpath("//a[@class='page']/text()")[-1]

                if self.pages > int(page):self.pages = int(page)

                for a in html.xpath("//a[@class='cover']"):
                    self.correctbox.append(rf"https://nhentai.net{a.get('href')}")

                if self.pages > 1:
                    pbar = tqdm(total=self.pages,desc="正在處理批量網址")
                    for page in range(2,self.pages+1): 
                        browser.get(f"{url.split('?page=')[0]}?page={page}")
                        WebDriverWait(browser,30).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='container index-container']")))
                        html = etree.fromstring(browser.page_source,etree.HTMLParser())

                        for a in html.xpath("//a[@class='cover']"):
                            self.correctbox.append(rf"https://nhentai.net{a.get('href')}")

                        if page == self.pages:pbar.update(2)
                        else:pbar.update(1)
                    pbar.close()
                
                if len(self.correctbox) != 0:
                    browser.quit()
                    self.run(self.correctbox)
            else:pass
            
    # 開始請求
    def run(self,url):
        for deal in url:download.Data_Request(deal)
class ComicsHomePage:
    def __init__(self):
        self.head = True    # 判斷是否隱藏窗口
        self.title = ""     # 漫畫名稱
        self.labelbox = {}  # 保存標籤數據
        self.Home = None    # 主頁Html存放
        self.pages = 1      # 下載頁數
        self.SaveNameFormat = 1
        self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
        self.UserData = os.path.join(dir,"Data")

    def enter(self,Url: str,pages: int=None,head: bool=True):
        if pages != None:self.pages = pages
        if head == False:self.head = head

        os.system(f"RD /s /q {self.UserData} >nul 2>&1")
        Verify(Url,self.pages,self.head)
    
    def Data_Request(self,Url):
        Auto = Automation(self.head)
        self.browser = Auto.browser()

        # 開啟漫畫主頁
        self.browser.get(Url)

        try: # 測試點選機器人認證
            human = WebDriverWait(self.browser,1).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox']")))
            human.click()
        except:pass
        
        # 測試延遲處理
        WebDriverWait(self.browser,30).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='thumbs']")))

        # 取得主頁代碼,並呼叫處理
        self.Home = etree.fromstring(self.browser.page_source,etree.HTMLParser())
        self.Data_Processing()

        # 處理完成後,獲取總共頁數,和創建資料夾
        Pages = self.labelbox['Pages'][0]
        self.Folder_Creation(self.title)

        print(f"{self.title}\n開始下載 ==>")
        # 創建進度條
        pbar = tqdm(total=int(Pages))
        
        for page in range(1,int(Pages)+1):
            self.browser.get(f"{Url}/{page}/")
            ImgUrl = etree.fromstring(self.browser.page_source,etree.HTMLParser()).xpath("//section[@id='image-container']/a/img")[0].get('src')
            
            if int(Pages) >= 100:SaveName = f"{self.SaveNameFormat:03d}.{ImgUrl.split('.')[-1]}"
            else:SaveName = f"{self.SaveNameFormat:02d}.{ImgUrl.split('.')[-1]}"

            threading.Thread(target=self.Download,args=(os.path.join(dir,self.title),SaveName,ImgUrl,self.headers)).start()
            
            self.SaveNameFormat += 1
            pbar.update(1)

        self.SaveNameFormat = 1
        pbar.close()
        self.browser.quit()

    # 處理主頁數據
    def Data_Processing(self):
        try:
            title = self.Home.xpath("//h2[@class='title']")[0]
            self.title = re.sub(r'[<>:"/\\|?*]', '', "".join(title.xpath(".//text()")).strip())
            
            labelbox = self.Home.xpath("//section[@id='tags']")[0]
            for index , tag in enumerate(labelbox.xpath(".//div")):
                if index == 4 or index == 6 or index == 8:continue # 這邊是排除不需要的數據
                else:self.labelbox[tag.text.strip().rstrip(':')] = tag.xpath(".//span[@class='name']/text()")
        except:
            print("請嘗試將ComicsHomePage,第三參數設置為False\n或者再次運行")
            os._exit(0)

        # self.labelbox 大致格式
        # {'Parodies': [''], 'Characters': ['', ''], 'Tags': [''], 'Artists': [''], 'Languages': ['', ''], 'Pages': ['']}

    # 創建資料夾
    def Folder_Creation(self,FolderName):
        try:
            os.mkdir(FolderName)
        except:
            pass

    # 下載圖片
    def Download(self,location,picturename,imageurl,headers):
        ImageData = requests.get(imageurl, headers=headers)
        if ImageData.status_code == 200:
            with open(os.path.join(location,picturename),"wb") as f:
                f.write(ImageData.content)
download = ComicsHomePage()
# 自動擷取剪貼簿
class AutomaticCapture:
    def __init__(self):
        self.initial = r"https://nhentai.*"
        self.download_trigger = False
        self.clipboard_cache = None # 緩存用於辨識狀態改變
        self.download_list = set() # 保存輸入網址避免重複使用set

    def Read_clipboard(self):
        pyperclip.copy('')
        while True:
            clipboard = pyperclip.paste()
            time.sleep(0.3)

            # 下載觸發(將set轉成list,開始下載)
            if self.download_trigger:
                os.system("cls")
                download.enter(list(self.download_list))
                break

            elif clipboard != self.clipboard_cache and re.match(self.initial,clipboard): # 基本驗證擷取格式
                print(f"以擷取的網址:{clipboard}")
                self.download_list.add(clipboard)
                self.clipboard_cache = clipboard

    def Download_command(self):
        # 持續監測鍵盤按鍵是否為 alt+s
        while True:
            if keyboard.is_pressed("alt+s"):
                self.download_trigger = True
                while keyboard.is_pressed("alt+s"):
                    pass

if __name__ == "__main__":

    # 當無法正常啟用自動化窗口時 , 就啟用該方法 !!Google會被關掉
    # reset()

    # list 傳遞目前只適用於漫畫連結 , 搜尋連結不適用 
    Batch_Box = []

###########################################################

    #? 客製化下載方法

    # url , 頁數 , 隱藏窗口 (url可輸入,單本漫畫/搜尋連結/Batch_Box的list)
    # download.enter(Batch_Box)

###########################################################

    #? 自動擷取剪貼簿(只適用單本漫畫連結)

    print("自動擷取下載(如要使用搜尋頁面,使用客製化方法下載)\n複製網址完畢後 , 按下 Alt+S 開始下載")

    capture = AutomaticCapture()
    # 監聽剪貼版線程
    threading.Thread(target=capture.Read_clipboard).start()

    # 監聽鍵盤觸發下載(設置為守護線程,當主線程結束,守護線程自動終止)
    command = threading.Thread(target=capture.Download_command)
    command.daemon = True
    command.start()