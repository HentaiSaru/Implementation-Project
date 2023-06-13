from concurrent.futures import ThreadPoolExecutor , ProcessPoolExecutor
from urllib.parse import unquote
from lxml import etree
import multiprocessing
from tqdm import tqdm
import pyperclip
import threading
import requests
import keyboard
import asyncio
import aiohttp
import time
import os
import re

"""
    * 使用前請詳閱說明書

    爬蟲適用網站 : https://www.wnacg.com/
    使用說明 : 輸入該漫畫的網址 , 會自動擷取 , 接著按下快捷鍵下載

    (支援: 
        ? 搜尋頁面 : https://www.wnacg.com/search/index.php?q=...
        ? Tag頁面 : https://www.wnacg.com/albums...
        ? 漫畫頁面 : https://www.wnacg.com/photos...
    )

    ! 網路的速度 , 與網站響應速度 , 會直接影響下載速度

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Versions 1.0.0 (重構測試版)

    功能:
        [+] 自動擷取網址
        [+] 批量同步下載

    問題:
        [*] 使用多進程操作下載 , 沒特別處理進度條顯示問題
        [*] 下載處理速度快慢 , 是根據使用者的CPU核心數
        [*] 網址處理有一些Bug , 有些會沒下載到
        [*] 網址處理較慢 , 為了準確獲取圖片連結 , 有好幾個請求步驟
    
"""

# 下載路徑設置
dir = os.path.abspath("R:/")
os.chdir(dir)

# 網站域名
def DomainName():
    return "https://www.wnacg.com"

# 精準處理下載
class Accurate:
    def __init__(self):
        # 用於驗證傳遞的網址格式
        self.Comic_Page_Format = r'^https:\/\/www\.wnacg\.com\/photos.*\d+\.html$'
        self.Search_Page_Format = r'https://www\.wnacg\.com/search/.*\?q=.+'
        self.Tag_page_format = r'^https:\/\/www\.wnacg\.com\/albums.*'

        # 取得CPU核心數
        self.CpuCore = multiprocessing.cpu_count()

        self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
        self.session = requests.Session()

        self.SingleBox = []
        self.BatchBox = []

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
            print("開始處理下載...")
            with ProcessPoolExecutor(max_workers=self.CpuCore) as executor:
                for url in self.SingleBox:
                    executor.submit(self.manga_page_data_processing,url)
        
        # 搜尋頁面與Tag頁面
        if len(self.BatchBox) > 0:
            for url in self.BatchBox:
                self.search_page_data_processing(url)

    # 搜尋頁面處理
    def search_page_data_processing(self,link):
        comic_link_box = []
        url = unquote(link)
        
        async def Get_all_page_data():
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

        asyncio.run(Get_all_page_data())

        print(f"獲取的漫畫數量 : {len(comic_link_box)}")
        print("開始處理下載...")
        with ProcessPoolExecutor(max_workers=self.CpuCore) as executor:
            for url in comic_link_box:
                executor.submit(self.manga_page_data_processing,url)

    # 漫畫頁面處理
    def manga_page_data_processing(self,url):
        picture_link = []

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

        Name = tree.xpath('//h2/text()')[0].strip()
        # 處理非法字元 , 獲得漫畫名
        manga_name = re.sub(r'[<>:"/\\|?*]', '', Name)

        # 漫畫下載路徑
        download_path = os.path.join(dir,manga_name)
        # 創建資料夾
        self.create_folder(download_path)

        # 處理圖片的網址 (重構測試)
        async def Get_picture_link():
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
                    image_link = tree.xpath('//img[@id="picarea"]/@src')[0]
                    picture_link.append(f"https:{image_link}")

        asyncio.run(Get_picture_link())
        self.download_processing(download_path,picture_link,manga_name)

    # 下載處理
    def download_processing(self,download_path,download_link,manga_name):
        SaveNameFormat = 1
        pbar = tqdm(total=len(download_link),desc=manga_name)

        with ThreadPoolExecutor(max_workers=500) as executor:
            for link in download_link:
                SaveName = f"{SaveNameFormat:03d}.{link.split('/')[-1].split('.')[1]}"

                executor.submit(self.download,download_path,link,SaveName)

                pbar.update(1)
                SaveNameFormat += 1
                time.sleep(0.01)
        pbar.close()

    # 資料夾創建
    def create_folder(self,Name):
        try:os.mkdir(Name)
        except:pass

    # 圖片下載
    def download(self,download_path,download_link,SaveName):
        ImageData = requests.get(download_link,headers=self.headers)
        with open(os.path.join(download_path,SaveName),"wb") as f:
            f.write(ImageData.content)

class AutomaticCapture:
    def __init__(self):
        self.initial = r"{}.*".format(DomainName())
        self.download_trigger = False
        self.clipboard_cache = None
        self.download_list = set()
        self.detection = True

    def Read_clipboard(self):
        pyperclip.copy('')
        while self.detection:
            clipboard = pyperclip.paste()
            time.sleep(0.1)

            if self.download_trigger:
                os.system("cls")

            elif clipboard != self.clipboard_cache and re.match(self.initial,clipboard):
                print(f"以擷取的網址:{clipboard}")
                self.download_list.add(clipboard)
                self.clipboard_cache = clipboard

    def Download_command(self):
        while self.detection:
            if keyboard.is_pressed("alt+s"):
                self.download_trigger = True
                self.detection = False
                while keyboard.is_pressed("alt+s"):
                    pass

if __name__ == "__main__":
    acc = Accurate()
    capture = AutomaticCapture()

    print("複製網址後自動擷取(Alt+S 開始下載):")
    clipboard = threading.Thread(target=capture.Read_clipboard)
    clipboard.start()
    command = threading.Thread(target=capture.Download_command)
    command.start()

    command.join()
    clipboard.join()

    if len(capture.download_list) > 0:
        acc.classify_url_formats(list(capture.download_list))
    else:
        print("無擷取內容")
        os._exit(0)