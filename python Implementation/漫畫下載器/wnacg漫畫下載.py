from urllib.parse import unquote , urlparse
import concurrent.futures
from lxml import etree
from tqdm import tqdm
import threading
import requests
import asyncio
import aiohttp
import queue
import time
import os
import re
dir = os.path.abspath("R:/") # 可更改預設路徑
os.chdir(dir)

"""
    * 使用前請詳閱說明書

    爬蟲適用網站 : https://www.wnacg.com/
    使用說明 : 輸入該漫畫的網址 , 接著就會自動下載
    (支援: 
    ? 搜尋頁面 : https://www.wnacg.com/search/index.php?q=...
    ? Tag頁面 : https://www.wnacg.com/albums...
    ? 漫畫頁面 : https://www.wnacg.com/photos...
    )

    !! 現在都只要直接運行程式後輸入網址即可 , 預設使用 self

    [預設使用類型] SlowAccurate
    
    優點=>
    * 精準處理所有連結
    * 支持同時批量下載多本漫畫
    缺點=>
    * 網址處理較慢
    * 線程處理不精確 可能下載完但程式不會自動關閉 需要手動關閉 (通常大量下載時才會出錯)

    [目前棄用無優化 , 經過多次修改可能無法使用] FastNormal
    
    優點=>
    * 高速處理網址 (使用網址命名規則去變換)
    * 下載速度稍快
    缺點=>
    * 無後續更新優化
    * 網址不準確 有時候會下載失敗 因為是使用命名規則去變換 只要剛好不符合就會變成錯誤網址

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    [+] 修改網址判斷方式
    [*] 待修正,修改判斷網址方式後遺留的非必要代碼
    [*] 待修復重複下載漫畫下載問題(有點懶~)
    [*] 待修復有時候線程無法終止問題(程式無法自行結束)
    
"""

# 計算運行線程數 (需要修正)
def Threading():
    count = 0
    while True:
        time.sleep(1)
        if threading.active_count() == 4:count += 1
        else:count = 0

        if count == 3:
            os._exit(0)

""" 較慢但通用多種下載 (新方法) """
class SlowAccurate:
    def __init__(self):
        # 網址驗證格式
        self.TagPage = r'^https:\/\/www\.wnacg\.com\/albums.*'
        self.SearchPage = r'https://www\.wnacg\.com/search/.*\?q=.+'
        self.ComicPage = r'^https:\/\/www\.wnacg\.com\/photos.*\d+\.html$'
        self.SupportedFormat = r'^https:\/\/www\.wnacg\.com\/photos.*\d+\.html$'

        # 網址分類保存
        self.SeparateBox = [] 
        self.BatchBox = []

        # 數據請求
        self.session = requests.Session()
        self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",}

        # 判斷下載的類型
        self.DownloadType = False
    
        # 隊列保存
        self.Work = queue.Queue()

    # 網址分類
    def URL_Classification(self,box):
        
        for url in box:
            if re.match(self.TagPage,url) or re.match(self.SearchPage,url):
                self.BatchBox.append(url)
            elif re.match(self.ComicPage,url):
                self.SeparateBox.append(url)
            else:print(f"這並非支持的網址格式{url}")

        # 搜尋頁預設都是同步下載
        if len(self.BatchBox) > 0:
            self.DownloadType = True
            for url in self.BatchBox:self.BatchProcessing(url)

        # 只有單條網址就使用,單本加速下載
        if len(self.SeparateBox) == 1:
            self.DataProcessing(self.SeparateBox[0])

        # 大於一條以上使用同步下載
        elif len(self.SeparateBox) > 1:
            self.DownloadType = True
            for url in self.SeparateBox:
                self.DataProcessing(url)

    # 搜尋頁面批量處理
    def BatchProcessing(self,Url):
        url = unquote(Url)
        AllLinks = []

        if re.match(self.SearchPage,url):
            url = f'https://www.wnacg.com/search/?q={url.split("?q=")[1].split("&")[0]}'
        elif re.match(self.TagPage,url):
            url = f'https://www.wnacg.com/albums-index-page-1-tag-{url.split("-tag-")[1]}'

        # 首次取得數據
        request = self.session.get(url, headers=self.headers)
        parser = etree.HTMLParser()
        tree = etree.fromstring(request.content, parser)

        # 獲取總共的頁數(只有一頁的會錯誤)
        try:
            if re.match(self.SearchPage,url):
                TotalPages = tree.xpath('//div[@class="f_left paginator"]/a[last()]/text()')[0]
            elif re.match(self.TagPage,url):
                TotalPages = tree.xpath('//div[@class="f_left paginator"]/a[last()-1]/text()')[0]
        except:TotalPages = "1"

        # 獲取頁面所有URL
        async def GetLink(session, url):
            async with session.get(url) as response:
                html = await response.text()
                tree = etree.fromstring(html, parser)
                links = []
                for i in tree.xpath('//div[@class="pic_box"]'):
                    link = f"https://www.wnacg.com{i.find('a').get('href')}"
                    links.append(link)
                return links
            
        # 將所有頁面網址輸出,再將網址全部使用GetLink獲取頁面所有網址
        async def RanGet(url):
            async with aiohttp.ClientSession(headers=self.headers) as session:
                PageList = []
                for page in range(int(TotalPages)):
                    if int(TotalPages) != 1 and re.match(self.SearchPage,url):
                        url = f"https://www.wnacg.com/search/index.php?q={url.split('?q=')[1]}&m=&syn=yes&f=_all&s=&p={page+1}"
                    elif int(TotalPages) != 1 and re.match(self.TagPage,url):
                        url = f"https://www.wnacg.com/albums-index-page-{int(url.split('-')[3])+1}-tag-{url.split('-')[-1]}"
                    PageList.append(url)
                    
                tasks = []
                for page in PageList:
                    task = asyncio.create_task(GetLink(session, page))
                    tasks.append(task)
                results = await asyncio.gather(*tasks)

                for links in results:
                    AllLinks.extend(links)

        asyncio.run(RanGet(url))

        for _input in AllLinks: # 懶得處理線程鎖,廢棄多線程
            self.DataProcessing(_input)
    
    # (這邊為了通用性,做了較多的數據處理,剛開始會跑比較久)
    def DataProcessing(self,Url):
        
        try:
            
            if re.match(self.SupportedFormat,Url):

                ComicsInternalLinks = []
                ComicPictureLink = []

                Url = f"https://www.wnacg.com/photos-index-{'page-1'}-aid-{Url.split('aid-')[1]}"
                reques = self.session.get(Url)
                html = reques.content
                parser = etree.HTMLParser()
                tree = etree.fromstring(html, parser)

                # 主頁最終頁數
                Home_Pages = int(re.findall(r'\d+', tree.xpath('//label[contains(text(),"頁數：")]/text()')[0])[0])

                # 漫畫名稱
                NameProcessing = tree.xpath('//h2/text()')[0].strip()
                # 處理非法字元
                NameMerge = re.sub(r'[<>:"/\\|?*]', '', NameProcessing)

                # 獲取主頁所有圖片分頁的連結
                async def GetImageLink(i, headers):
                    async with aiohttp.ClientSession(headers=headers) as session:
                        async with session.get(f"https://www.wnacg.com/photos-index-page-{i}-aid-{Url.split('aid-')[1]}") as response:
                            html = await response.text()
                            parser = etree.HTMLParser()
                            tree = etree.fromstring(html, parser)
                            internal_links = [f"https://www.wnacg.com{x.get('href')}" for x in tree.xpath("//div[@class='pic_box tb']/a")]
                            return internal_links

                # 使用異步同時發起請求 (只要不同時請求就不會發生數據重複,但是數據量多時,可能會很慢)
                async def LinkRun():
                    tasks = []
                    links_set = set()
                    for i in range(1, Home_Pages+1):
                        tasks.append(asyncio.create_task(GetImageLink(i, self.headers)))
                    # 等待完成
                    image_links = await asyncio.gather(*tasks)
                    for link in image_links:
                        # 將其轉換為Set避免重複
                        links_set.update(link)
                    # 轉換為list並造順序排列
                    ComicsInternalLinks[:] = sorted(list(links_set), key=lambda x: urlparse(x).path)

                # 使用所有的分頁連結,去請求每個連結對應的,圖片連結
                async def GetImage(link, headers):
                    async with aiohttp.ClientSession(headers=headers) as session:
                        async with session.get(link) as response:
                            html = await response.text()
                            parser = etree.HTMLParser()
                            tree = etree.fromstring(html, parser)
                            image_link = tree.xpath('//img[@id="picarea"]/@src')[0]
                            return f"https:{image_link}"

                # 使用異步同時發起請求,獲取所有對應的圖片連結
                async def ImageRun():
                    tasks = []
                    for link in ComicsInternalLinks:
                        tasks.append(asyncio.create_task(GetImage(link, self.headers)))
                    image_links = await asyncio.gather(*tasks)
                    for link in image_links:
                        ComicPictureLink.append(link)
                    ComicPictureLink.sort() #先暫時用這種方式排序

                asyncio.run(LinkRun())
                asyncio.run(ImageRun())

                if self.DownloadType:
                    # 同步請求,工作序列(同時下載多本)
                    self.Work.put((ComicPictureLink,Url,NameMerge))
                elif self.DownloadType == False:
                    # 單線程請求(適用於單本加速下載)
                    download_path = os.path.join(dir, NameMerge)
                    self.Ffolder(download_path)
                    self.SingleDownload(ComicPictureLink,Url,NameMerge)
            else:
                print(f"這並非支持的網址格式{Url}")

        except TypeError:
            print("請放單獨的漫畫網址")

    def DownloadWork(self):
        # 允許最大同時下載數
        MAX_THREADS = 10
        active_threads = []

        while True:
            time.sleep(0.1)
            if not self.Work.empty():
                data = self.Work.get()
                ComicPictureLink = data[0]
                Url = data[1]
                NameMerge = data[2]

                def Simultaneous():
                    download_path = os.path.join(dir, NameMerge)
                    #創建文件夾
                    self.Ffolder(download_path)
                    # 開始請求圖片
                    self.SimultaneousDownload(ComicPictureLink,Url,NameMerge)

                if len(active_threads) < MAX_THREADS:
                    download = threading.Thread(target=Simultaneous)
                    active_threads.append(download)
                    download.start()
                else:
                    for thread in active_threads:
                        if not thread.is_alive():
                            active_threads.remove(thread)
                            break
    
    # 轉換漫畫資訊 多本同時下載(單本下載數量很慢)
    def SimultaneousDownload(self,ComicsInternalLinks,MangaURL,NameMerge):
        SaveNameFormat = 1
        pbar = tqdm(total=len(ComicsInternalLinks),desc=NameMerge)

        for page in ComicsInternalLinks:
            SaveName = f"{SaveNameFormat:03d}.{page.split('/')[-1].split('.')[1]}"
            # 同時下載多本
            self.Download(os.path.join(dir, NameMerge),SaveName,MangaURL,page,self.headers)

            pbar.update(1)
            
            SaveNameFormat += 1
        pbar.close()

    # 轉換漫畫資訊 單本下載加速
    def SingleDownload(self,ComicsInternalLinks,MangaURL,NameMerge):
        SaveNameFormat = 1
        pbar = tqdm(total=len(ComicsInternalLinks),desc=NameMerge)

        with concurrent.futures.ThreadPoolExecutor(max_workers=512) as executor:
            
            for page in ComicsInternalLinks:
                SaveName = f"{SaveNameFormat:03d}.{page.split('/')[-1].split('.')[1]}"
                # 單本下載加速     
                executor.submit(self.Download, os.path.join(dir, NameMerge) , SaveName, MangaURL , page , self.headers)

                pbar.update(1)

                SaveNameFormat += 1
                time.sleep(0.1)
                
        pbar.close()

    # 創建資料夾
    def Ffolder(self,FolderName):
        try:os.mkdir(FolderName) # 用漫畫名創建一個空資料夾(再傳遞時已經包含路徑+名稱)
        except:pass

    # 下載方法
    def Download(self,Path,SaveName,MangaURL,Image_URL,headers):

        ImageData = requests.get(Image_URL,headers=headers)
        if ImageData.status_code == 200:
            with open(os.path.join(Path, SaveName),"wb") as f:
                f.write(ImageData.content)
        else:print(f"請求錯誤:\n漫畫網址:{MangaURL}\n圖片網址:{Image_URL}")

""" 較快但有些下載不了 (舊方法未修正) """
class FastNormal:

    # 批量輸入下載
    def BatchInput(Url):
        # 用於確認輸出
        Judge = False
        AllLinks = []

        if isinstance(Url,list):

            SupportedFormat = r'^https:\/\/www\.wnacg\.com\/photos.*\d+\.html$'

            for url in Url:

                if re.match(SupportedFormat,url):
                    Judge = True
                    AllLinks.append(url)
                else:print(f"這並非支持的網址格式{Url}")

        else:
            url = unquote(Url)
            Match = False
            # r 為原始字串符 他將不會轉譯 \ 反斜
            SearchPage = r'https://www\.wnacg\.com/search/.*\?q=.+'
            TagPage = r'^https:\/\/www\.wnacg\.com\/albums.*'

            if re.match(SearchPage,url):
                url = f'https://www.wnacg.com/search/?q={url.split("?q=")[1].split("&")[0]}'
                Match = True
            elif re.match(TagPage,url):
                url = f'https://www.wnacg.com/albums-index-page-1-tag-{url.split("-tag-")[1]}'
                Match = True

            if Match:
                Judge = True
                headers = {
                    "authority": "www.wnacg.com",
                    "cache-control": "no-cache",
                    "pragma": "no-cache",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
                }

                # 首次取得數據
                session = requests.Session()
                request = session.get(url, headers=headers)
                parser = etree.HTMLParser()
                tree = etree.fromstring(request.content, parser)

                # 獲取總共的頁數(只有一頁的會錯誤)
                try:

                    if re.match(SearchPage,url):
                       TotalPages = tree.xpath('//div[@class="f_left paginator"]/a[last()]/text()')[0]
                    elif re.match(TagPage,url):
                       TotalPages = tree.xpath('//div[@class="f_left paginator"]/a[last()-1]/text()')[0]

                except:TotalPages = "1"

                # 獲取頁面所有URL
                async def GetLink(session, urls):
                    async with session.get(urls) as response:
                        html = await response.text()
                        tree = etree.fromstring(html, parser)
                        links = []
                        for i in tree.xpath('//div[@class="pic_box"]'):
                            link = f"https://www.wnacg.com{i.find('a').get('href')}"
                            links.append(link)
                        return links

                # 將所有頁面網址輸出,再將網址全部使用GetLink獲取頁面所有網址
                async def RanGet(url):
                    async with aiohttp.ClientSession(headers=headers) as session:
                        PageList = []
                        for page in range(int(TotalPages)):
                            if int(TotalPages) != 1 and re.match(SearchPage,url):
                                url = f"https://www.wnacg.com/search/index.php?q={url.split('?q=')[1]}&m=&syn=yes&f=_all&s=&p={page+1}"
                            elif int(TotalPages) != 1 and re.match(TagPage,url):
                                url = f"https://www.wnacg.com/albums-index-page-{int(url.split('-')[3])+1}-tag-{url.split('-')[-1]}"
                            
                            PageList.append(url)

                        tasks = []
                        for page in PageList:
                            task = asyncio.create_task(GetLink(session, page))
                            tasks.append(task)
                        results = await asyncio.gather(*tasks)
                        for links in results:
                            AllLinks.extend(links)
                asyncio.run(RanGet(url))

            else:print(f"這並非支持的網址格式{Url}")

        if Judge:
            for _input in AllLinks:
                FastNormal.BasicSettings(_input)

    def BasicSettings(Url):
        SupportedFormat = r'^https:\/\/www\.wnacg\.com\/photos.*\d+\.html$'
        if re.match(SupportedFormat,Url):

            total_pages_format = []

            session = requests.Session()
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            }

            Url = f"https://www.wnacg.com/photos-index-{'page-1'}-aid-{Url.split('aid-')[1]}"
            reques = session.get(Url)
            html = reques.content
            parser = etree.HTMLParser()
            tree = etree.fromstring(html, parser)

            # 主頁總共頁數
            Home_Pages = int(re.findall(r'\d+', tree.xpath('//label[contains(text(),"頁數：")]/text()')[0])[0])
            
            # 漫畫名稱
            NameProcessing = tree.xpath('//h2/text()')[0].strip()
            NameMerge = NameProcessing

            # 漫畫圖片連結
            ComicLink = [x for x in tree.xpath('//div[@class="pic_box tb"]/a/img/@src')[0].split("/") if x]

            # 獲取頁面中所有的頁碼格式
            async def get_format(session,url, headers, UrlQueue):
                async with session.get(url, headers=headers) as response:
                    html = await response.text()
                    parser = etree.HTMLParser()
                    tree = etree.fromstring(html, parser)
                    for span in tree.xpath('//span[@class="name tb"]'):
                        if span.text not in UrlQueue.queue:
                            UrlQueue.put(span.text)

            UrlQueue = queue.Queue()
            async def main(home_pages, headers):
                async with aiohttp.ClientSession() as session:
                    # 先將總共頁數的網址全部存入
                    urllist = [f"https://www.wnacg.com/photos-index-page-{i}-aid-{Url.split('aid-')[1]}" for i in range(1, home_pages+1)]
                    # 呼叫get_format獲取所有的格式
                    tasks = [asyncio.create_task(get_format(session, url, headers, UrlQueue)) for url in urllist]
                    # 等待完成
                    await asyncio.gather(*tasks)

                    # 將取得數據存入 total_pages_format 並排序
                    while not UrlQueue.empty():
                        total_pages_format.append(UrlQueue.get())
                    total_pages_format.sort()
            asyncio.run(main(Home_Pages, headers))
            
            #創建文件夾
            FastNormal.Ffolder(NameMerge)
            # 開始請求圖片
            FastNormal.DataRequest(total_pages_format,ComicLink,Url,NameMerge)
        else:
            print("這並非此模支持的網址格式")

    # 獲取漫畫數據
    def DataRequest(pages_format,ComicLink,MangaURL,NameMerge):
        global TestError
        SaveNameFormat = 1
        Mantissa = ComicLink[0].split('t')[1]
        NumberType = ['1','2','3','4']
        ImageType = ['.jpg','.png']

        headers = {
            "sec-fetch-dest": "image",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-site": "cross-site",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        }

        TestError = False
        with concurrent.futures.ThreadPoolExecutor(max_workers=512) as executor:

            for page in pages_format:

                Picture_Name = f"{page}.{ComicLink[5].split('.')[1]}"
                Image_URL = f"https://img{Mantissa}/{ComicLink[1]}/{ComicLink[3]}/{ComicLink[4]}/{Picture_Name}"
    
                SaveName = f"{SaveNameFormat:03d}.{ComicLink[5].split('.')[1]}"

                status = executor.submit(FastNormal.Download, SaveName, Image_URL, headers)
                print(f"{NameMerge}-{SaveName}")
                time.sleep(0.1)
    
                # 無腦判斷法
                if TestError: 

                    Type = Image_URL.split('/')[-1].split('.')[1]

                    for Img in ImageType:

                        Image_URL = f"{Image_URL.split(f'.{Type}')[0]}{Img}"

                        for Number in NumberType:
                            # 獲取Image_URL的數字位置
                            value = Image_URL.split('img')[1].split('.')[0]
                            # 將該數字替換成 Number
                            Image_URL = f"https://img{value.replace(f'{value}',f'{Number}')}.qy0{Image_URL.split('.qy0')[1]}"

                            # 再次呼叫方法
                            status = executor.submit(FastNormal.Download, SaveName, Image_URL, headers)
                            
                            # 判斷當他成功時
                            if status.result().status_code == 200:
                                # 將之後的請求數字都變更
                                Mantissa = f"{Number}.qy0.ru"
                                TestError = False
                                break
                    
                        if status.result().status_code == 200:break
                            
                    # 如果到最後還是請求失敗,就打印失敗的格式
                    if status.result().status_code != 200:print(f"請求錯誤:\n漫畫網址:{MangaURL}\n圖片網址:{Image_URL}")

                SaveNameFormat += 1

    PathStatus = False
    # 創建資料夾
    def Ffolder(FolderName):
        #刪除名稱中的非法字元
        name = re.sub(r'[<>:"/\\|?*]', '', FolderName)
        try:
            if FastNormal.PathStatus:
                os.chdir(os.path.join(".."))
            else:FastNormal.PathStatus = True
        
            os.mkdir(name) # 在該路徑下用漫畫名創建一個空資料夾
            os.chdir(os.path.join(os.getcwd(), name)) # 將預設路徑導入至該資料夾
        except:
            os.chdir(os.path.join(os.getcwd(), name))
            pass

    # 下載方法
    def Download(SaveName,Image_URL,headers):
        global TestError

        ImageData = requests.get(Image_URL, headers=headers)
        if ImageData.status_code == 200:
            with open(SaveName,"wb") as f:
                f.write(ImageData.content)
        else:TestError = True

        return ImageData

if __name__ == "__main__":

    Slow = SlowAccurate()
    """計算運行線程,用於結束程式運行"""
    threading.Thread(target=Threading).start()
    """加速工作隊列"""
    threading.Thread(target=Slow.DownloadWork).start()
    
    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

    """處理速度較於緩慢,但可精準的下載所有類型(輸入到重覆的網址,只會覆蓋下載,不會再創一個新的)"""
    box = []

    print("輸入網址(要開始下載輸入 s ):")
    while True:
        url = input("\n輸入:")
        if url.lower() == "s":
            os.system("cls")
            print("開始下載...")
            break
        else:box.append(url)
    if len(box) >= 1:Slow.URL_Classification(box)
    else:os._exit(0)

    """處理速度較於快速,但會有一些下載失敗(懶得修復問題,不建議使用)"""

    # 單獨下載
    #FastNormal.BasicSettings("#")

    # 批量下載
    # FastNormal.BatchInput("#")