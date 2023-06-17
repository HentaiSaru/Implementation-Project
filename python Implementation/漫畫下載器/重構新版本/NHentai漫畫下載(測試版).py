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

# 下載路徑
dir = os.path.abspath("R:/")

# 網站域名
def DomainName():
    return "https://nhentai.net/"

#Todo [ 再此處輸入當前通過機器人驗證的 cookie (輸入錯誤會請求不到) ]
# 代碼中手動設置 cookie
def cookie_set():
    cookie = {
        "cf_clearance" : "",
        "csrftoken" : ""
    }
    return cookie

# 讀取保存 cookie 的 json
def cookie_read():
    # 切換到當前文件夾絕對路徑
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    try:
        with open("./Cookie/NHCookies.json" , "r") as file:
            return json.loads(file.read())
    except:
        # 沒有就進行創建
        cookie = {"csrftoken":"Please fill in the cookie","cf_clearance":"Please fill in the cookie"}
        with open("./Cookie/NHCookies.json" , "w") as file:
            file.write(json.dumps(cookie, indent=4, separators=(',',':')))

# 嘗試自動獲取Cookie , 並回傳結果
def cookie_get():
    return Get.Request_Cookie(DomainName() , f"{os.path.dirname(os.path.abspath(__file__))}\\Cookie\\NHCookies")

# 下載請求方法
class NHentaidownloader:
    def __init__(self):
        #Todo => 請求相關設置
        self.session = requests.Session()
        self.Google_Headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
        self.Edge_Headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43"}
        self.headers = None
        #Todo => 判斷格式和排除格式
        self.search = r"https://nhentai\.net/.*"
        self.manga = r"https://nhentai\.net/g/\d+"
        self.illegal_filename = r'[<>:"/\\|?*]'
        #Todo => 下載設置項目
        self.TitleFormatting = None
        self.ProtectionDelay = None
        self.ProcessDelay = None
        self.TagFilterBox = None
        self.MaxProcess = None
        self.GetCookie = None
        self.Cookies = None
        self.SetUse = False
        self.Pages = None

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

    # 基本請求數據
    def get_data(self,url):
        request = self.session.get(url, headers=self.headers, cookies=self.Cookies)
        return etree.fromstring(request.content , etree.HTMLParser())
    
    # 異步數據請求
    async def async_get_data(self,session,url):
        async with session.get(url, headers=self.headers, cookies=self.Cookies) as response:
            content = await response.text()
            return etree.fromstring(content , etree.HTMLParser())
    
    # 下載設置功能
    def download_settings(
            self,
            SearchQuantity: int=5,
            TitleFormat: bool=False,
            TryGetCookie: bool=False,

            DownloadDelay = 0.3,
            ProcessCreationDelay = 1,
            MaxConcurrentDownload: int=cpu_count(),

            FilterTags: dict=None,
            CookieSource: dict=cookie_set(),
    ):
        """
    >>> SearchQuantity - 搜尋頁面的請求頁數 (預設: 5 頁)
    *   設置當你輸入搜尋介面 , 想要批量下載所有漫畫時
    *   預設只會載入 5 頁的資訊 , 如果該搜尋頁面總共 10 頁 , 就會被忽略
    *   當設置超過搜尋的最大頁數 , 就會以該搜尋的最大頁數為主
    >>> TitleFormat - 使用標題格式化 (預設: False)
    *   會將輸出創建的漫畫名稱套上格式
    *   預設就是用原本的名稱
    >>> TryGetCookie - 自動嘗試取得 cookie (預設: False)
    *   當請求失敗 , 無法獲取數據時 , 會進行嘗試自動取得 cookie
    !   請注意該方法請求成功的 cookie , 必須使用 google() 方法請求
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
    !   {'Parodies': [''], 'Characters': ['', ''], 'Tags': [''], 'Artists': [''], 'Languages': ['', ''], 'Pages': ['']}
    *   'Parodies' : 原創 / 二創作品
    *   'Characters' : 人物角色
    *   'Tags' : Tag 標籤
    *   'Artists' : 繪師
    *   'Languages' : 語言
    *   'Pages' : 頁數
    *    數據格式必須 為上方的 key 值 , 包含數據 list
    *    填入的值當擁有該TAG的 , 就會被排除掉 , 不會被下載
    >>> CookieSource - cookie 的設定來源 (預設: cookie_set() , 也就是在上方代碼設置)
    *   這是設置請求時所用的 cookie 導入來源 , 預設是使用 cookie_set() 方法
    *   就是由此代碼上方的設置填寫讀取 , 也可以改成 cookie_read() 方法
    *   變成由 cookies.json 中讀取 cookie 使用
    """
        # 判斷是否被調用設置了
        self.SetUse = True
        self.Cookies = CookieSource
        self.Pages = SearchQuantity
        self.GetCookie = TryGetCookie
        self.TagFilterBox = FilterTags
        self.TitleFormatting = TitleFormat
        self.ProtectionDelay = DownloadDelay
        self.MaxProcess = MaxConcurrentDownload
        self.ProcessDelay = ProcessCreationDelay
    
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
            if isinstance(link,str):
                category_box.append(link)
            elif isinstance(link,list):
                category_box = link
            else:raise Exception()

            # 載入下載設置
            if not self.SetUse:
                self.download_settings()

            for url in category_box:
                if re.match(self.manga,url):
                    self.comics_box.append(url)
                elif re.match(self.search,url):
                    self.search_box.append(url)
                else:
                    print(f"錯誤格式的連結{url}")

            if len(self.search_box) > 0:
                for url in self.search_box:
                    self.search_page_data(url)

            if len(self.comics_box) == 1:
                self.comic_page_data(url, 1)
            elif len(self.comics_box) > 1:
                with ProcessPoolExecutor(max_workers=self.MaxProcess) as executor:
                    for index , url in enumerate(self.comics_box):
                        executor.submit(self.comic_page_data , url, index)
                        time.sleep(self.ProcessDelay)
        except Exception as e:
            print(f"錯誤的輸入格式\n錯誤: {e}")

    # 漫畫頁數據處理
    def comic_page_data(self,url,count):

        print(f"[漫畫 {count} 請求] {url}")
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
                            print(f"[標籤排除] {url}")
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
            self.save_location = os.path.join(dir,self.title)
            
            # 圖片的連結
            img = tree.xpath("//meta[@itemprop='image']")[0].get("content")
            domain_name = img.rsplit('/',1)[0].replace(img[8:10],f"i{img[9]}")
            suffix = img.rsplit('.',1)[1]
            
            # 生成請求連結
            for i in range(1 , int(self.labelbox['Pages'][0])+1):
                SaveName = f"{i:03d}.{suffix}"
                comic_link = f"{domain_name}/{i}.{suffix}"
                self.download_link[SaveName] = comic_link
            
            print("[漫畫 %d 請求完成] %s => 請求耗時 %.3f 秒" % (count , url, (time.time() - StartTime)))
            self.download_processing()
        except Exception as e:
            if self.GetCookie:
                print(f"請求失敗 : {url}\n請稍後...")

                if cookie_get():
                    print("獲取成功!")
                    self.Cookies = cookie_read()
                    self.comic_page_data(url,count)
                else:
                    print("獲取失敗!")  
            else:
                print(f"請更換Cookie , 或檢查使用的瀏覽器\ndebug : {e}")

    # 搜尋頁數據處理
    def search_page_data(self,link):

        print(f"[請求搜尋數據] {link}")

        try:
            comic_link = []
            domain = DomainName().rsplit("/",1)[0]
            StartTime = time.time()

            if link.find("?page=") != -1:
                url = f"{link}?page=1"
            else:
                url = f"{link.split('?page=')[0]}?page=1"

            # 獲取漫畫連結方法
            def get_comic_link(tree):
                for data1 in tree.xpath("//div[@class='container index-container']"): 
                    for data2 in data1.xpath(".//div[@class='gallery']/a[@class='cover']"):
                        comic_link.append(f"{domain}{data2.get('href')}")

            # 首次數據請求
            tree = self.get_data(url)
            get_comic_link(tree)

            for data1 in tree.xpath("//section[@class='pagination']"): 
                lastpage = int(data1.xpath(".//a[@class='page']/text()")[-1])

            # 當設置的頁數 > 實際頁數 , 設置頁數 = 實際頁數
            if self.Pages > lastpage:
                self.Pages = lastpage

            async def Trigger():
                async with aiohttp.ClientSession() as session:
                    work = []

                    for page in range(2,self.Pages+1):
                        work.append(asyncio.create_task(self.async_get_data(session, f"{url.split('?page=')[0]}?page={page}")))
                    results = await asyncio.gather(*work)

                    for tree in results:
                        get_comic_link(tree)

            asyncio.run(Trigger())
            # 雖然有點多餘 , 但還是避免重複
            link_exclude = list(OrderedDict.fromkeys(comic_link))

            print("獲取的漫畫數量 : %d => 獲取耗時 %.3f 秒\n" %(len(link_exclude), (time.time() - StartTime)))
            with ProcessPoolExecutor(max_workers=self.MaxProcess) as executor:
                for index , url in enumerate(link_exclude):
                    executor.submit(self.comic_page_data , url, index)
                    time.sleep(self.ProcessDelay)

        except Exception as e:
            if self.GetCookie:
                print(f"請求失敗 : {url}\n請稍後...")

                if cookie_get():
                    print("獲取成功!")
                    self.Cookies = cookie_read()
                    self.search_page_data(link)
                else:
                    print("獲取失敗!")
            else:
                print(f"請更換Cookie , 或檢查使用的瀏覽器\ndebug : {e}")

    # 下載處理
    def download_processing(self):
        self.create_folder(self.save_location)

        with ThreadPoolExecutor(max_workers=500) as executor:
            for SaveName , comic_link in tqdm(self.download_link.items() , desc=self.title, colour="#9575DE"):
                executor.submit(self.download,os.path.join(self.save_location,SaveName),comic_link)
                time.sleep(self.ProtectionDelay)

    # 資料夾創建
    def create_folder(self,Name):
        try:os.mkdir(Name)
        except:pass

    # 下載方法
    def download(self,download_path,download_link):
        ImageData = self.session.get(download_link, headers=self.headers, cookies=cookie_set())
        with open(download_path , "wb") as f:
            f.write(ImageData.content)

if __name__ == "__main__":
    nh = NHentaidownloader()
    TagExclude = {
        'Tags': ['']
    }
    # 下載相關設置
    nh.download_settings(TitleFormat=True,SearchQuantity=1,CookieSource=cookie_read()) # ,TryGetCookie=True

    nh.google("")
    # nh.edge("")