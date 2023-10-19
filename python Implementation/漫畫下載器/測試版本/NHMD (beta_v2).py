from Script.AutomaticCapture import AutoCapture
from Script.GetCookiesAutomatically import Get
from collections import OrderedDict
from concurrent.futures import *
from multiprocessing import *
from lxml import etree
from tqdm import tqdm
import requests
import aiohttp
import asyncio
import time
import json
import re
import os

""" Versions 1.0.3 (測試版)

    Todo - NHentai 漫畫下載

        * - 當前功能 :
        ?   [+] 多進程處理
        ?   [+] 多線程下載
        ?   [+] 下載位置選擇
        ?   [+] 自動擷取連結
        ?   [+] 下載進度顯示
        ?   [+] 各類數據顯示
        ?   [+] 多項下載功能設置
        ?   [+] 自動嘗試獲取 Cookie

        * - 測試功能 :
        ?   [*] 試錯重載
        ?   [*] 下載速度
        ?   [*] 請求穩定性
        ?   [*] 數據處理例外
        
        * - 當前失效 :
        ?   [-] 自動獲取 Cookies 的自動化 , 目前無法繞過機器人檢測獲取到數據 , TryGetCookie 維持預設就好
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Todo - 相關說明

        * 使用相關
        ! cookie 相關有 set / read / get , 只有 set 需要手動更改代碼
        ! filter 相關有 set / read / none , 並非強制設置 none 就是無設置
        ! 大致上設置都在 download_settings() , 設置說明也於此處
        ! 如果一直請求失敗 , 有可能是網站本身 , 或是網路連線問題
"""

#Todo [網站域名設置]
def DomainName():
    return "https://nhentai.net/"

#Todo [嘗試自動獲取Cookie , 並回傳結果]
def cookie_get():
    return Get.AGCookie(DomainName() , f"{os.path.dirname(os.path.abspath(__file__))}\\Cookie\\NHCookies")

class Set:
    """
    Set 類別 (手動設置)
    * [使用方式]
    * 在需要使用該數據的部份呼叫 Set()
    * 然後輸入 "cookie" 或 "filter" -> Set("cookie")
    * 就可以取得設置的字典數據
    """
    def __init__(self):
        #Todo [ 再此處手動輸入當前通過機器人驗證的 cookie (輸入錯誤會請求不到) ]
        self.Cookies = {
            "cf_clearance" : "",
            "csrftoken" : ""
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
Set = Set()

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

    def Create(self, Type: str):
        if Type.lower() == "cookie":
            self.Create_Format = {
                "cf_clearance":"Please fill in the cookie"
            }
        elif Type.lower() == "filter":
            #Todo [用於排除Tag類型字典 (不必要的Key可以刪除 , 加速排除處理)]
            self.Create_Format = {
                "Parodies": ["Please enter Tag"],
                "Characters": ["Please enter Tag"],
                "Tags": ["Please enter Tag"],
                "Artists": ["Please enter Tag"],
                "Languages": ["Please enter Tag"]
            }

        with open(self.Open_Path , "w") as file:
            file.write(json.dumps(self.Create_Format, indent=4, separators=(',',':')))

    def __call__(self,Type: str):
        if Type.lower() == "cookie":
            self.Open_Path = self.Cookies_Path
        elif Type.lower() == "filter":
            self.Open_Path = self.Exclude_Path
            
        try:
            with open(self.Open_Path , "r") as file:
                return json.loads(file.read())
        except:
            self.Create(Type)
Read = Read()

#? [下載請求方法]
class NHentaidownloader:
    def __init__(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        #Todo => 請求相關設置
        self.session = requests.Session()
        self.Google_Headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"}
        self.Edge_Headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/117.0.2045.47"}
        self.headers = None
        #Todo => 判斷格式和排除格式
        self.search = r"https://nhentai\.net/.*"
        self.manga = r"https://nhentai\.net/g/\d+"
        self.illegal_filename = r'[<>:"/\\|?*]'
        #Todo => 下載設置項目
        self.TitleFormatting = None
        self.ProtectionDelay = None
        self.ErrorReDownload = None
        self.ProcessDelay = None
        self.TagFilterBox = None
        self.MaxProcess = None
        self.GetCookie = None
        self.Cookies = None
        self.Pages = None
        self.path = None
        #Todo => 判斷是否自訂設置
        self.SetUse = False

        #? 網址分類保存 (初始分類時用)
        self.comics_box = []
        self.search_box = []
        #Todo => 漫畫資訊保存
        # 漫畫標題
        self.title = None
        # 漫畫保存位置
        self.save_location = None
        # 漫畫Tag標籤
        self.labelbox = {}
        #Todo => 保存生成的下載連結
        # 下載連結
        self.download_link = {}
    
    # 下載設置功能
    def download_settings(
            self,
            SearchQuantity: int=5,
            TitleFormat: bool=False,
            TryGetCookie: bool=False,
            TryRedownload: bool=True,
            DownloadPath: str=os.path.dirname(os.path.abspath(__file__)),

            DownloadDelay = 0.3,
            ProcessCreationDelay = 1,
            MaxConcurrentDownload: int=cpu_count(),

            FilterTags: dict=None,
            CookieSource: dict=Set("cookie"),
    ):
        """
    >>> SearchQuantity - 搜尋頁面的請求頁數 (預設: 5 頁)
    *   設置當你輸入搜尋介面 , 想要批量下載所有漫畫時
    *   預設只會載入 5 頁的資訊 , 如果該搜尋頁面總共 10 頁 , 就會被忽略
    *   當設置超過搜尋的最大頁數 , 就會以該搜尋的最大頁數為主
    *   設置輸入 0 會變成自動使用 , 最大頁數去搜尋
    >>> TitleFormat - 使用標題格式化 (預設: False)
    *   會將輸出創建的漫畫名稱套上格式
    *   預設就是用原本的名稱
    >>> TryGetCookie - 自動嘗試取得 cookie (預設: False)
    *   當請求失敗 , 無法獲取數據時 , 會進行嘗試自動取得 cookie
    !   請注意該方法請求成功的 cookie , 必須使用 google() 方法請求
    >>> TryRedownload - 嘗試重新下載 (預設: True)
    *   當圖片格式錯誤時 , 嘗試重新變換格式
    *   再次進行下載
    >>> DownloadPath - 漫畫下載的路徑 (預設: 當前路徑位置)
    *   無特別設置 , 會以該程式的所在位置
    *   作為下載目錄進行下載
    >>> DownloadDelay - 下載速度的延遲 (預設: 0.3s)
    *   主要是為了保護伺服器 , 和避免被禁止請求 , 在請求下載時進行延遲
    *   因為下載是多進程的 , 不設速度雖然會超快 , 但對伺服器不好
    >>> ProcessCreationDelay - 創建進程的延遲 (預設: 1s)
    *   在處理下載的部份是使用多進程處理的 , 這個是設置創建多進程時的延遲
    *   目的也是為了保護伺服器 , 不要短期間接收大量的請求 , 而受到損害
    >>> MaxConcurrentDownload - 最大同時創建的進程數 (預設: CPU核心數)
    *   這是設置最大創建的進程數量 , 也就是同時可以併發處理下載數
    *   預設是根據自身的 CPU 核心數 , 越多不見得越快
    >>> FilterTags - 排除標籤字典 (預設: None)
    !   {'Parodies': [''], 'Characters': [''], 'Tags': [''], 'Artists': [''], 'Languages': [''], 'Pages': ['']}
    *   'Parodies' : 原創 / 二創作品
    *   'Characters' : 人物角色
    *   'Tags' : Tag 標籤
    *   'Artists' : 繪師
    *   'Languages' : 語言
    *   'Pages' : 頁數
    *    數據格式必須 為上方的 key 值 , 包含數據 list
    *    填入的值當擁有該TAG的 , 就會被排除掉 , 不會被下載
    >>> CookieSource - cookie 的設定來源 (預設: cookie_set())
    *   這是設置請求時所用的 cookie 導入來源
    *   可以改成 cookie_read() 方法
    *   變成由 cookies.json 中讀取 cookie 使用
    """
        # 判斷是否被調用設置了
        self.SetUse = True
        self.path = DownloadPath
        self.Cookies = CookieSource
        self.Pages = SearchQuantity
        self.GetCookie = TryGetCookie
        self.TagFilterBox = FilterTags
        self.TitleFormatting = TitleFormat
        self.ProtectionDelay = DownloadDelay
        self.MaxProcess = MaxConcurrentDownload
        self.ProcessDelay = ProcessCreationDelay
        self.ErrorReDownload = TryRedownload
    
    # 基本請求數據
    def get_data(self,url):
        request = self.session.get(url, headers=self.headers, cookies=self.Cookies)
        return etree.fromstring(request.content , etree.HTMLParser())
    
    # 異步數據請求
    async def async_get_data(self,session,url):
        async with session.get(url, headers=self.headers, cookies=self.Cookies) as response:
            content = await response.text()
            return etree.fromstring(content , etree.HTMLParser())
    
    # google 請求
    def google(self,link):
        self.headers = self.Google_Headers
        self.URL_Classification(link)

    # edge 請求
    def edge(self,link):
        self.headers = self.Edge_Headers
        self.URL_Classification(link)

    # 網址分類方法
    def URL_Classification(self,link):
        category_box = []
        try:
            if isinstance(link, str):
                category_box.append(link)
            elif isinstance(link, list):
                category_box = link
            else:raise Exception()

            # 載入下載設置
            if not self.SetUse:
                self.download_settings()

            # 驗證請求
            try:
                tree = self.get_data(DomainName())
                verify = tree.xpath("//div[@class='container index-container']/h2/text()")[0].strip()
                if verify != "New Uploads":
                    raise Exception()
            except:
                if self.GetCookie:
                    print(f"驗證錯誤請稍後...")
                    if cookie_get():
                        print("\n獲取成功!\n")
                        self.Cookies = Read("cookie")
                    else:
                        print("\n獲取失敗!\n請求失敗連結")
                        print(category_box)
                        return
                else:
                    print("請檢查 Cookie , 或使用的 Headers")
                    return

            for url in category_box:
                if re.match(self.manga, url):
                    self.comics_box.append(url)
                elif re.match(self.search, url):
                    self.search_box.append(url)
                else:
                    print(f"錯誤格式的連結{url}", flush=True)

            if len(self.search_box) > 0:
                for url in self.search_box:
                    self.search_page_data(url)

            if len(self.comics_box) == 1:
                self.comic_page_data(url, 1)
            elif len(self.comics_box) > 1:
                with ProcessPoolExecutor(max_workers=self.MaxProcess) as executor:
                    for index , url in enumerate(self.comics_box):
                        executor.submit(self.comic_page_data , url, index+1)
                        time.sleep(self.ProcessDelay)
        except Exception as e:
            print(f"錯誤的輸入格式\n錯誤: {e}")

    # 漫畫頁數據處理
    def comic_page_data(self,url,count):

        print(f"[漫畫 {count} 請求] {url}", flush=True)
        StartTime = time.time()
        tree = self.get_data(url)

        try:
            # Tag標籤資訊
            label = tree.xpath("//section[@id='tags']")[0]
            for index , tag in enumerate(label.xpath(".//div")):
                if index == 4 or index == 6 or index == 8:continue # 這邊是排除不需要的數據
                else:self.labelbox[tag.text.strip().rstrip(':')] = tag.xpath(".//span[@class='name']/text()")
            
            # 當有設置排除標籤時 , 重複時會進行排除
            if self.TagFilterBox != None:
                for key , value in self.TagFilterBox.items():
                    try:
                        lab = self.labelbox[key]
                        result = set(value) & set(lab)
                        if result:
                            print(f"[漫畫 {count} 標籤排除]")
                            return
                    except:
                        continue

            # 這邊是處理有些標題元素位置不同的問題
            TitleElement = tree.xpath("//h2[@class='title']")
            if len(TitleElement) == 0:
                TitleElement = tree.xpath("//h1[@class='title']")

            if self.TitleFormatting:
                for title in TitleElement:
                    # 有些漫畫會缺少某個元素 , 不這樣就會出錯
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
                    self.title = re.sub(self.illegal_filename, '', title).strip()
            else:
                title = TitleElement[0]
                self.title = re.sub(self.illegal_filename, '', "".join(title.xpath(".//text()")).strip())

            # 保存位置
            self.save_location = os.path.join(self.path, self.title)
            
            # 圖片的連結
            img = tree.xpath("//meta[@itemprop='image']")[0].get("content")
            domain_name = img.rsplit('/',1)[0].replace(img[8:10],f"i{img[9]}")
            suffix = img.rsplit('.',1)[1]
            
            # 生成請求連結
            for i in range(1 , int(self.labelbox['Pages'][0])+1):
                SaveName = f"{i:03d}.{suffix}"
                comic_link = f"{domain_name}/{i}.{suffix}"
                self.download_link[SaveName] = comic_link
            
            print("[漫畫 %d 請求完成] => 請求耗時 %.3f 秒" % (count , (time.time() - StartTime)), flush=True)
            self.download_processing()
        except Exception as e:
            print(f"DeBug : {e}")

    # 搜尋頁數據處理
    def search_page_data(self,link):

        print(f"[請求搜尋數據] {link}", flush=True)

        try:
            comic_link = []
            domain = DomainName().rsplit("/",1)[0]
            StartTime = time.time()

            if link.find("?page=") != -1:
                url = f"{link.split('?page=')[0]}?page=1"
            else:
                url = f"{link}?page=1"
            
            # 獲取漫畫連結方法
            def get_comic_link(tree):
                for data1 in tree.xpath("//div[@class='container index-container']"): 
                    for data2 in data1.xpath(".//div[@class='gallery']/a[@class='cover']"):
                        comic_link.append(f"{domain}{data2.get('href')}")

            # 首次數據請求
            tree = self.get_data(url)
            get_comic_link(tree)

            # 獲取最後一頁
            last = tree.xpath("//a[@class='last']")[0].get("href")
            lastpage = int(last.split("?page=")[1])

            # 當設置的頁數 > 實際頁數 或 == 0 , 設置頁數 = 實際頁數
            if self.Pages > lastpage or self.Pages == 0:
                self.Pages = lastpage

            # 異步的同時請求 , 當數量太多時 , 可能會造成數據沒請求到
            async def Trigger():
                count = 0
                async with aiohttp.ClientSession() as session:
                    work = []

                    for page in range(2,self.Pages+1):
                        work.append(asyncio.create_task(self.async_get_data(session, f"{url.split('?page=')[0]}?page={page}")))
                        count+=1

                        # 這邊必須設置延遲 , 不然大量讀取會有缺少的數據
                        if count == 5 and self.Pages > 5:
                            print(f"\r以處理 [{page-1}] 頁 休息1秒...", end="", flush=True)
                            await asyncio.sleep(1)
                            count = 0

                    results = await asyncio.gather(*work)

                    for tree in results:
                        get_comic_link(tree)

            asyncio.run(Trigger())

            # 雖然有點多餘 , 但還是避免重複
            link_exclude = list(OrderedDict.fromkeys(comic_link))

            print("\r獲取的漫畫數量 : %d => 獲取耗時 %.3f 秒\n" %(len(link_exclude), (time.time() - StartTime)), flush=True)
            with ProcessPoolExecutor(max_workers=self.MaxProcess) as executor:
                for index , url in enumerate(link_exclude):
                    executor.submit(self.comic_page_data , url, index)
                    time.sleep(self.ProcessDelay)

        except Exception as e:
            print(f"DeBug : {e}")

    # 下載處理
    def download_processing(self):
        self.create_folder(self.save_location)

        with ThreadPoolExecutor(max_workers=100) as executor:
            for SaveName , comic_link in tqdm(self.download_link.items() , desc=self.title, colour="#9575DE"):

                save = os.path.join(self.save_location,SaveName)
                executor.submit(self.download, save, comic_link)
                time.sleep(self.ProtectionDelay)

    # 資料夾創建
    def create_folder(self,Name):
        try:os.mkdir(Name)
        except:pass

    # 正常下載方法
    def download(self,download_path,download_link):
        ImageData = self.session.get(download_link, headers=self.headers, cookies=self.Cookies)

        if ImageData.status_code == 200:
            with open(download_path , "wb") as f:
                f.write(ImageData.content)
        else:
            if self.ErrorReDownload:
                self.error_download_try_again(download_path,download_link)
    
    # 下載錯誤的 嘗試 重新下載
    def error_download_try_again(self,path,link):
        
        domain = link.rsplit(".",1)[0]
        shunt = ["i3","i5","i7"]
        extension = ["jpg","png"]

        for i in range(len(shunt)):
            for j in range(len(extension)):
                download_link = f"{domain.replace(link[8:10],shunt[i])}.{extension[j]}"
                tryerror = self.session.get(download_link, headers=self.headers, cookies=self.Cookies)

                if tryerror.status_code == 200:
                    with open(path , "wb") as f:
                        f.write(tryerror.content)

if __name__ == "__main__":
    nh = NHentaidownloader()
    # 自動擷取設置
    AutoCapture.settings(DomainName())

    # 下載相關設置
    nh.download_settings(
        DownloadPath="R:/",
        TitleFormat=True,
        SearchQuantity=10,
        #TryGetCookie=True,
        FilterTags=Read("filter"),
        CookieSource=Read("cookie"),
    )

    capture = AutoCapture.GetList()
    if capture != None:
        nh.google(capture)
    else:
        print("無擷取內容")
        os._exit(0)