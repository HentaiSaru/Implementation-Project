from Script import AutoCapture, Reques, Get
from collections import OrderedDict
from concurrent.futures import *
from multiprocessing import *
from tqdm import tqdm
import asyncio
import time
import json
import re
import os

#Todo [ 手動獲取Cookie, 並保存Josn文件 ]
def cookie_get():
    return Get.MGCookie("https://e-hentai.org/", rf"{os.getcwd()}\Cookie\NHCookies")

class Set:
    """
    Set 類別 (手動設置)
    * [使用方式]
    * 在需要使用該數據的部份呼叫 Set()
    * 然後輸入 "cookie" 或 "filter" -> Set("cookie")
    * 就可以取得設置的字典數據
    """
    def __init__(self):
        #Todo [ 手動輸入當前通過機器人驗證的 cookie (輸入錯誤會請求不到) ]
        self.Cookies = {
            "csrftoken" : "",
            "cf_clearance" : ""
        }
        #Todo [手動設置排除標籤 , 並可於 download_settings() 套用回傳結果 , 設置詳情於 download_settings() 說明]
        self.TagExclude = {
            "Tags": [""]
        }

    def __call__(self, Type: str):
        if Type.lower() == "cookie":
            return self.Cookies
        elif Type.lower() == "filter":
            return self.TagExclude
        
class Read:
    """
    Read 類別 (自動讀取Json)
    * [使用方式]
    * 在需要使用該數據的部份呼叫 Read()
    * 然後輸入 "cookie" 或 "filter" -> Read("cookie")
    * 就可以取得設置的字典數據
    * 如沒有該數據 , 就會進行創建
    """
    def __init__(self):
        self.Cookies_Path = "./Cookie/NHCookies.json"
        self.Exclude_Path = "./Exclude/NHFilter.json"
        self.Open_Path = None
        self.Create_Format = {}
        self.Create_Path = None

    def __call__(self, Type: str):
        if Type.lower() == "cookie":
            self.Open_Path = self.Cookies_Path
        elif Type.lower() == "filter":
            self.Open_Path = self.Exclude_Path
            
        try:
            with open(self.Open_Path , "r") as file:
                return json.loads(file.read())
            
        except: # Todo 當找不到出現錯誤時, 進行創建
            if Type.lower() == "cookie":
                self.Create_Format = {
                    "cf_chl_2":"Please fill in the cookie",
                    "csrftoken" : "cookie",
                    "cf_clearance" : "cookie"
                }
            elif Type.lower() == "filter":
                self.Create_Format = {
                    "Parodies": ["Please enter Tag"],
                    "Characters": ["Please enter Tag"],
                    "Tags": ["Please enter Tag"],
                    "Artists": ["Please enter Tag"],
                    "Languages": ["Please enter Tag"]
                }
                
            with open(self.Open_Path, "w") as file:
                file.write(json.dumps(self.Create_Format, indent=4, separators=(',',':')))

#! 實例化
Set = Set()               
Read = Read()

#Todo [ 數據請求 ]
class DataRequest:
    def __init__(self):
        self.Reques = None #? 宣告, 由下方繼承後定義
        self.domain = "https://nhentai.net"

    def get(self, link, result="tree") -> object:
        return self.Reques.get(link, result)

    def http_get(self, link) -> object:
        return self.Reques.http_get(link)

#Todo [ 下載連結驗證 分類 ]
class Validation(DataRequest):
    def __init__(self):
        super().__init__()
        self.search = re.compile(r"https://nhentai\.net/.*")
        self.manga = re.compile(r"https://nhentai\.net/g/\d+")
        self.GetCookie = None # 判斷是否自動獲取
        self.category_box = [] # 保存正確的類型
        self.comics_box = [] # 漫畫頁面網址
        self.search_box = [] # 搜尋頁面網址

    def URL_Classification(self, link) -> bool:
        try:
            if isinstance(link, str):
                self.category_box.append(link)
            elif isinstance(link, list):
                self.category_box = link
            else:
                raise ValueError()

            if self.Request_Status(): # 驗證請求狀態
                for url in self.category_box:
                    if self.manga.match(url):
                        self.comics_box.append(url)
                    elif self.search.match(url):
                        self.search_box.append(url)
                    else:
                        print(f"錯誤格式的連結{url}", flush=True)
                
                if len(self.search_box) > 0 or len(self.comics_box) > 0:
                    return True
                else:
                    return False
            else:
                raise TypeError()

        except TypeError:
            print("請更換 Cookie, 或檢查使用的請求瀏覽器")
            os._exit(1)
        except ValueError as e:
            print(f"錯誤的輸入格式\n錯誤碼 : {e}")
            os._exit(1)

    def Request_Status(self) -> bool:
        try:
            tree = self.get(self.domain)
            verify = tree.xpath("//div[@class='container index-container']/h2/text()")[0].strip()
            if verify == "New Uploads":
                return True
            else:
                raise Exception()
        except:
            if self.GetCookie:
                print(f"驗證錯誤請稍後...")
                if cookie_get():
                    print("\n獲取成功!\n")
                    self.Cookies = Read("cookie")
                    return True
                else:
                    print("\n獲取失敗!\n")
                    return False
            else:
                return False

#Todo [ 下載器主程式 ]
class NHentaidownloader(Validation):
    def __init__(self):
        super().__init__()
        #Todo [ 排除非法字元 ]
        self.illegal_filename = re.compile(r'[<>:"/\\|?*]')
        #Todo [ 判斷是否改變設置 ]
        self.SetUse = False
        # Todo [ 下載參數設置 ]
        self.TitleFormatting = None
        self.ProtectionDelay = None # 下載的延遲
        self.ErrorReDownload = None
        self.ProcessDelay = None # 進程創建延遲
        self.TagFilterBox = None
        self.MaxProcess = None
        self.Pages = None
        self.path = None
        # Todo [ 保存數據參數 ]
        self.title = None # 漫畫標題
        self.labelbox = {} # 漫畫 Tag 標籤
        self.download_link = {} # 下載連結
        self.save_location = None # 保存位置

    #? [ 下載設定 ]
    def download_settings(
        self,
        Browser: str="Google",
        SearchQuantity: int=5,
        TitleFormat: bool=False,
        TryGetCookie: bool=False,
        TryRedownload: bool=True,
        DownloadPath: str=os.getcwd(),
        
        DownloadDelay=0.3,
        ProcessCreationDelay=1,
        MaxConcurrentDownload: int=cpu_count(),
        
        FilterTags: dict=None,
        CookieSource: dict=Set("cookie"),
    ):
        """
        * Browser => 使用的瀏覽器 [Google/Edge]
        * SearchQuantity => 傳入搜尋頁面時, 需要爬取幾頁的數據
        * TitleFormat => 是否需要使用標題格式, 創建資料夾名稱的格式
        * TryGetCookie => 是否啟用自動獲取 Cookie
        * TryRedownload => 請求失敗時是否自動試錯
        * DownloadPath => 下載的路徑
        * DownloadDelay => 每張圖片的下載請求延遲
        * ProcessCreationDelay => 進程創建的延遲
        * MaxConcurrentDownload => 同時處理的最大進程數
        * FilterTags => 用於過濾含有特定Tag的漫畫 [Read("filter") / Set("filter")]
        * CookieSource => Cookie 的來源 [Read("cookie") / Set("cookie")]
        
        >>> FilterTags 補充說明 [數據格式必須有 key 值 , 包含數據 list]
        !   {'Parodies': [''], 'Characters': [''], 'Tags': [''], 'Artists': [''], 'Languages': [''], 'Pages': ['']}
        *   'Parodies' : 原創 / 二創作品
        *   'Characters' : 人物角色
        *   'Tags' : Tag 標籤
        *   'Artists' : 繪師
        *   'Languages' : 語言
        *   'Pages' : 頁數
        """
        self.SetUse = True # 判斷設置方法被調用
        self.path = DownloadPath
        self.Pages = SearchQuantity # 搜尋頁下載頁數
        self.GetCookie = TryGetCookie
        self.TagFilterBox = FilterTags
        self.TitleFormatting = TitleFormat
        self.ErrorReDownload = TryRedownload
        self.ProtectionDelay = DownloadDelay # 下載延遲
        self.MaxProcess = MaxConcurrentDownload
        self.ProcessDelay = ProcessCreationDelay # 進程創建延遲
        self.Reques = Reques(Browser.lower().capitalize(), CookieSource)

    #? [ 下載請求 ]
    def download_request(self, link):
        if not self.SetUse:
            self.download_settings()

        if self.URL_Classification(link):
            self.Process_Trigger()

    #? [ 驗證後觸發處理 ]
    def Process_Trigger(self):
        if len(self.search_box) > 0:
            for url in self.search_box:
                self.search_page_data(url)
        elif len(self.comics_box) > 0:
            with ProcessPoolExecutor(max_workers=self.MaxProcess) as executor:
                for index, url in enumerate(self.comics_box):
                    executor.submit(self.comic_page_data, url, index+1)
                    time.sleep(self.ProcessDelay)

    #? [ 搜尋頁處理 ]
    def search_page_data(self, link):
        print(f"[搜尋連結]: {link}", flush=True)
        StartTime = time.time()
        comic_link = []

        try:
            #* 獲取漫畫連結方法
            def get_comic_link(tree):
                for data1 in tree.xpath("//div[@class='container index-container']"): 
                    for data2 in data1.xpath(".//div[@class='gallery']/a[@class='cover']"):
                        comic_link.append(f"{self.domain}{data2.get('href')}")

            if link.find("?page=") != -1:
                url = f"{link.split('?page=')[0]}?page=1"
            else:
                url = f"{link}?page=1"

            #* 首次數據請求
            tree = self.get(url)
            get_comic_link(tree)

            #* 獲取最終頁數
            last = tree.xpath("//a[@class='last']")[0].get("href")
            lastpage = int(last.split("?page=")[1])

            #* 當設置的頁數 > 實際頁數 或 == 0 , 設置頁數 = 實際頁數
            if self.Pages > lastpage or self.Pages == 0:
                self.Pages = lastpage

            #* 異步的同時請求, 當數量太多時, 可能會造成數據沒請求到
            async def Trigger():
                count = 0
                work = []
                for page in range(2, self.Pages+1):
                    work.append(asyncio.create_task(self.http_get(f"{url.split('?page=')[0]}?page={page}")))
                    count+=1
                    if count == 5 and self.Pages > 5:
                        print(f"\r以處理 [{page-1}] 頁 休息1秒...", end="", flush=True)
                        await asyncio.sleep(1)
                        count = 0      
                results = await asyncio.gather(*work)

                for tree in results:
                    get_comic_link(tree)

            #* 啟用異步處理      
            asyncio.run(Trigger())

            #* 雖然有點多餘 , 但還是避免重複
            link_exclude = list(OrderedDict.fromkeys(comic_link))
            print("\r獲取的漫畫數量 : %d => 獲取耗時 %.3f 秒\n" %(len(link_exclude), (time.time() - StartTime)), flush=True)
            return
            #* 觸發漫畫頁處理
            with ProcessPoolExecutor(max_workers=self.MaxProcess) as executor:
                for index, url in enumerate(link_exclude):
                    executor.submit(self.comic_page_data, url, index)
                    time.sleep(self.ProcessDelay)

        except Exception as e:
            print(f"搜尋頁: {e}")
            
    #? [ 漫畫頁處理 ]
    def comic_page_data(self, url, count):
        print(f"[漫畫 {count} 請求] {url}", flush=True)
        StartTime = time.time()
        
        try:
            tree = self.get(url)

            #* 取得 Tag 標籤資訊
            label = tree.xpath("//section[@id='tags']")[0]
            #* 處理 Tag 數據格式
            for index, tag in enumerate(label.xpath(".//div")):
                if index in {4, 6, 8}:continue #? 略過不須判斷的標
                self.labelbox[tag.text.strip().rstrip(':')] = tag.xpath(".//span[@class='name']/text()")

            #* 比對 Tag 數據
            if self.TagFilterBox != None:
                for key, value in self.TagFilterBox.items():
                    lab = self.labelbox[key]
                    result = set(value) & set(lab)
                    if result:
                        print(f"[漫畫 [{count}] 標籤排除]")
                        return

            #* 取得標題元素    
            TitleElement = tree.xpath("//h2[@class='title'] | //h1[@class='title']")
            
            if self.TitleFormatting:
                #* 標題格式處理
                for title in TitleElement:
                    #? 有些漫畫會缺少某個元素, 不這樣就會出錯
                    try:
                        beginning = title.xpath(".//span[@class='before']/text()")[0]
                        beginning = re.sub(r'\[([^\]]*)\]', r'(\1)', beginning).strip()
                    except:beginning = ""

                    try:
                        middle = title.xpath(".//span[@class='pretty']/text()")[0].strip()
                    except:middle = ""

                    try:
                        tail = title.xpath(".//span[@class='after']/text()")[0].strip()
                    except:tail = "" 

                    title = f"{beginning}{middle}___{tail}"
                    self.title = self.illegal_filename.sub("", title).strip()
            else:
                title = TitleElement[0]
                self.title = self.illegal_filename.sub("", "".join(title.xpath(".//text()")).strip())

            #* 取得保存位置
            self.save_location = os.path.join(self.path, self.title)

            #* 取得圖片連結樣本
            img = tree.xpath("//meta[@itemprop='image']")[0].get("content") #? 完整連結
            domain_name = img.rsplit('/', 1)[0].replace(img[8:10], f"i{img[9]}") #? 分割出域名
            suffix = img.rsplit('.', 1)[1] #? 分割出後墜

            #* 樣本生成後續連結
            for i in range(1, int(self.labelbox["Pages"][0])+1):
                self.download_link[f"{i:03d}.{suffix}"] = f"{domain_name}/{i}.{suffix}"

            print("[漫畫 %d 請求完成] => 請求耗時 %.3f 秒" % (count , (time.time() - StartTime)), flush=True)
            self.download_processing()
        except Exception as e:
            print(f"漫畫頁: {e}")

    #? [ 下載處理 ]
    def download_processing(self):
        self.create_folder(self.save_location)
        
        with ThreadPoolExecutor(max_workers=100) as executor:
            for SaveName, ComicLink in tqdm(self.download_link.items(), desc=self.title, colour="#9575DE"):
                Save = os.path.join(self.save_location, SaveName) #* 圖片保存位置
                executor.submit(self.download_pictures, Save, ComicLink)
                time.sleep(self.ProtectionDelay)
        
    #? [ 資料夾創建 ]
    def create_folder(self, Name):
        try:os.mkdir(Name)
        except:pass

    #? [ 漫畫圖片下載 ]
    def download_pictures(self, download_path, download_link):
        ImageData = self.get(download_link, "none")
        
        if ImageData.status_code == 200:
            with open(download_path, "wb") as file:
                file.write(ImageData.content)
        else:
            if self.ErrorReDownload:
                self.error_download_try_again(download_path, download_link)
                
    #? [ 下載重試 ]
    def error_download_try_again(self, path, link):
        
        domain = link.rsplit(".", 1)[0] #* 域名拆分
        shunt = ["i", "i2", "i3", "i5", "i7"] #* 伺服器
        extension = ["jpg", "png"] #* 擴展名
        
        for server in shunt:
            for expand in extension:
                download_link = f"{domain.replace(link[8:10], server)}.{expand}"
                tryerror = self.get(download_link, "none")
                
                if tryerror.status_code == 200:
                    with open(path , "wb") as f:
                        f.write(tryerror.content)

if __name__ == "__main__":
    nh = NHentaidownloader()

    nh.download_settings(
        TitleFormat=True,
        DownloadDelay=0.1,
        SearchQuantity=10,
        DownloadPath="R:/",
        FilterTags=Read("filter"),
        CookieSource=Read("cookie"),
    )
    
    AutoCapture.settings("https://nhentai.net/")
    capture = AutoCapture.GetList()
    if capture != None:
        nh.download_request(capture)
    else:
        print("無擷取內容")
        os._exit(0)