from AutomaticCapture import AutoCapture
from collections import OrderedDict
# 主要使用 concurrent.futures 的進程池和線程池加速處理下載
from concurrent.futures import *
# multiprocessing 的 Pool 進程池創建只能在主模塊使用
from multiprocessing import *
# 網址中文字解析
from urllib.parse import *
from lxml import etree
from tqdm import tqdm
import requests
import aiohttp
import asyncio
import time
import os
import re

""" Versions 1.0.3 (測試版)

    Todo - wnacg 漫畫下載器 :
        * - 當前功能 :
        ?   [+] 自動擷取網址 (需要 AutomaticCapture.py)
        ?   [+] 批量同步下載
        ?   [+] 顯示處理數量
        ?   [+] 顯示當前處理
        ?   [+] 顯示處理時間
        ?   [+] 下載位置選擇

        * - 當前問題:
        ?   [*] 有些需要登入才能觀看的漫畫頁面 , 就會請求不到圖片 (需自行填寫cookie , 才可正常請求)
        ?   [*] 使用多進程操作下載 , 沒特別處理進度條顯示問題 (進度條是請求下載處理的進度 , 不包含輸出圖片至硬碟)
        ?   [*] 搜尋頁面或TAG頁面的大量下載 , 網址處理有一些Bug , 有些會沒下載到(可再自行單本下載)
        ?   [*] 網址處理較慢 , 為了準確獲取圖片連結 , 有好幾個請求步驟
        ?   [*] 短時間大量下載很有可能會卡住 , 要嘛將延遲設置更高 , 要嘛就單本下載

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Todo - 爬蟲適用網域 : https://www.wnacg.com/

    Todo - 使用說明 : 輸入該漫畫的網址 , 會自動擷取 , 接著按下快捷鍵下載 , 下載完成會自動結束 (沒有結束代表還沒完成/或是卡死了[短時間下載太多會卡住])

    Todo - 代碼可修改 :
        *   修改 1. 下載的檔案位置
        *   修改 2. 最大創建進程數(建議別太多會卡住 , 除非電腦CPU核心夠多)
        *   修改 3. 下載延遲數(預設:0.5秒) 這是對網站 , 和硬碟的保護 , 雖然不限速會很快
        *   修改 4. 進程創建的延遲數(預設:1秒) 也是對網站的保護 , 太快容易大量下載時卡住

        ( 支援類型 : 
            ? 搜尋頁面 : https://www.wnacg.com/search/index.php?q=...
            ? Tag頁面 : https://www.wnacg.com/albums...
            ? 漫畫頁面 : https://www.wnacg.com/photos...
        )
    
        ! 網路的速度 , 與網站響應速度 , 影響處理速度
        ! 硬碟的讀寫速度 , 影響圖片下載速度
    
"""
# 網站域名(有時候域名會變更)
def DomainName():
    return "https://www.wnacg.com"

# 下載路徑設置
dir = os.path.abspath("R:/")
os.chdir(dir)

# 精準處理下載
class Accurate:
    def __init__(self):
        """ ----------------------------
        [- CPU核心數 (創建進程數量) -]
        
        越多並不會越快 , 但在大量下載時 , 相對更快
        如只想用自身 CPU 的核心數 , 就把 + 2 刪除

        """
        self.CpuCore = cpu_count() + 2

        """ ----------------------------
        [- 保護延遲秒數 -]

        這個延遲速度影響到下載速度
        為了保護網站的伺服器 , 設置的延遲
        同時也保護硬碟的寫入 , 設置低雖然快但是
        但網站響應卡住 , 下載就跟著卡住了

        """
        self.ProtectionDelay = 0.5

        """ ----------------------------
        [- 進程創建延遲秒數 -]

        這個延遲速度影響到併發的進程處理速度
        同樣也是保護網站的伺服器 , 避免短時間大量請求
        延遲太低大量下載時 , 會卡住因為伺服器響應問題

        """
        self.ProcessDelay = 1

        ########################################

        self.session = requests.Session()
        self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
        self.cookie = {
            "MPIC_bnS5": "#",
            "X_CACHE_KEY" : "#"
        }

        ########################################

        # 用於驗證傳遞的網址格式
        self.Comic_Page_Format = r'^https:\/\/www\.wnacg\.com\/photos.*\d+\.html$'
        self.Search_Page_Format = r'https://www\.wnacg\.com/search/.*\?q=.+'
        self.Tag_page_format = r'^https:\/\/www\.wnacg\.com\/albums.*'
        
        # 分類為漫畫網址的保存
        self.SingleBox = []
        # 分類為搜尋網址的保存
        self.BatchBox = []

    #Todo - 當有圖片請求不到下載不完整 , 在上方填寫 cookie , 並在請求的這邊打上 cookies=self.cookie
    # 異步數據請求
    async def async_get_data(self,session,url):
        async with session.get(url, headers=self.headers) as response:
            content = await response.text()
            return etree.fromstring(content , etree.HTMLParser())
    
    # 普通數據請求
    def get_data(self,url):
        request = self.session.get(url, headers=self.headers)
        return etree.fromstring(request.content , etree.HTMLParser())
 
    # URL格式分類
    def classify_url_formats(self,link):
        
        for url in link:
            if re.match(self.Comic_Page_Format,url):
                self.SingleBox.append(url)
            elif re.match(self.Search_Page_Format,url) or re.match(self.Tag_page_format,url):
                self.BatchBox.append(url)
            else:
                print(f"Error : {url} - 並非支持的網址格式")

        # 漫畫頁面
        if len(self.SingleBox) > 0:

            # 如果只有一本下載就降低延遲
            if len(self.SingleBox) == 1:
                self.ProtectionDelay = 0.01

            print(f"獲取的漫畫數量 : {len(self.SingleBox)}")

            with ProcessPoolExecutor(max_workers=self.CpuCore) as executor:
                for index , url in enumerate(self.SingleBox):
                    executor.submit(self.manga_page_data_processing, url, index+1)
                    time.sleep(self.ProcessDelay)
        
        # 搜尋頁面與Tag頁面
        if len(self.BatchBox) > 0:
            for url in self.BatchBox:
                self.search_page_data_processing(url)

    # 搜尋頁面處理
    def search_page_data_processing(self,link):
        comic_link_box = []
        url = unquote(link)
        
        async def Request_Trigger():
            New_url = ""
            pages = 0
            page_count = 1
            total_pages = 2

            # 頁數讀取準確度測試
            async with aiohttp.ClientSession() as session:
                while page_count <= total_pages:
                    # 搜尋頁面的處理
                    if re.match(self.Search_Page_Format,url):
                        New_url = f"{url.split('&syn=yes')[0]}&p={page_count}"
                        tree = await self.async_get_data(session,New_url)

                        try:
                            pages = int(tree.xpath('//div[@class="f_left paginator"]/a[last()]/text()')[0])
                        except:total_pages = 1

                        if pages > total_pages:
                            total_pages = pages

                    # Tag頁面的處理
                    elif re.match(self.Tag_page_format,url):
                        New_url = f"{DomainName()}/albums-index-page-{page_count}-tag-{url.split('-')[-1]}"
                        tree = await self.async_get_data(session,New_url)

                        try:
                            pages = int(tree.xpath('//div[@class="f_left paginator"]/a/text()')[-1])
                        except:total_pages = 1

                        if pages > total_pages:
                            total_pages = pages

                    # 最後取得漫畫連結(這個連結取得還是有BUG,無法取得完整的)
                    for data in tree.xpath("//div[@class='title']"):
                        link = f"https://www.wnacg.com{data.find('a').get('href')}"
                        comic_link_box.append(link)
                    
                    page_count += 1

        print("搜尋頁面開始處理...")

        asyncio.run(Request_Trigger())

        print(f"獲取的漫畫數量 : {len(comic_link_box)}")

        with ProcessPoolExecutor(max_workers=self.CpuCore) as executor:
            for index , url in enumerate(comic_link_box):
                executor.submit(self.manga_page_data_processing, url, index+1)
                time.sleep(self.ProcessDelay)

    # 漫畫頁面處理
    def manga_page_data_processing(self,url,number):
        print(f"第 {number} 本漫畫開始處理...")

        picture_link = []
        StartTime = time.time()

        link = url.split("index-")
        New_url = f"{link[0]}index-page-1-{link[1]}"

        tree = self.get_data(New_url)

        # 漫畫總頁數
        total_pages = int(re.findall(r'\d+', tree.xpath('//label[contains(text(),"頁數：")]/text()')[0])[0])
                
        # 漫畫主頁頁數(12頁漫畫 = 主頁1頁)
        remainder = total_pages % 12
        home_pages = total_pages / 12

        # 當餘數大於0代表需要多一頁
        if remainder > 0:
            home_pages = int(home_pages + 1)
        else:
            home_pages = int(home_pages)

        Name = tree.xpath('//h2/text()')[0].strip()
        # 處理非法字元 , 獲得漫畫名
        manga_name = re.sub(r'[<>:"/\\|?*]', '', Name)

        # 漫畫下載路徑
        download_path = os.path.join(dir,manga_name)
        # 創建資料夾
        self.create_folder(download_path)
        
        # 處理圖片的網址 (每次請求都會對重複的進行排除)
        async def Request_Trigger():
            async with aiohttp.ClientSession() as session:
                work1 = []
                work2 = []

                # 獲取漫畫主頁,的所有分頁連結
                for page in range(1,home_pages+1):
                    work1.append(asyncio.create_task(self.async_get_data(session,f"{link[0]}index-page-{page}-{link[1]}")))
                results = await asyncio.gather(*work1)

                # 使用所有分頁連結,請求內頁連結
                for tree in results:
                    for html in tree.xpath("//div[@class='pic_box tb']/a"):
                        work2.append(asyncio.create_task(self.async_get_data(session,f"{DomainName()}{html.get('href')}")))
                results = await asyncio.gather(*work2)
                
                # 使用內頁連結,取得圖片連結
                for tree in results:
                    try:
                        image_link = tree.xpath('//img[@id="picarea"]/@src')[0]
                        picture_link.append(f"https:{image_link}")
                    except:
                        pass
                       
        asyncio.run(Request_Trigger())
        picture_exclude = list(OrderedDict.fromkeys(picture_link))

        print("第 %d 本漫畫 - 處理花費時間 : %.3f" % (number , (time.time()-StartTime)))
        self.download_processing(download_path,picture_exclude,manga_name)

    # 資料夾創建
    def create_folder(self,Name):
        try:os.mkdir(Name)
        except:pass

    # 下載處理
    def download_processing(self,download_path,download_link,manga_name):
        SaveNameFormat = 1

        with ThreadPoolExecutor(max_workers=500) as executor:
            for link in tqdm(download_link, desc=manga_name, colour="#9AC5F4"):
                SaveName = f"{SaveNameFormat:03d}.{link.split('/')[-1].split('.')[1]}"

                executor.submit(self.download,download_path,link,SaveName)

                SaveNameFormat += 1
                time.sleep(self.ProtectionDelay)

    # 圖片下載
    def download(self,download_path,download_link,SaveName):
        ImageData = requests.get(download_link,headers=self.headers)

        with open(os.path.join(download_path,SaveName),"wb") as f:
                f.write(ImageData.content)

if __name__ == "__main__":
    acc = Accurate()

    AutoCapture.settings(DomainName())
    capture = AutoCapture.GetList()

    if capture != None:
        acc.classify_url_formats(capture)
    else:
        print("無擷取內容")
        os._exit(0)