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

# 程式入口點於最下方 (574行)

""" 初始化宣告 """
def __init__(self,Url,ComicsInternalLinks,MangaURL,NameMerge,FolderName,SaveName,Image_URL,headers,pages_format,ComicLink):
    self.Url = Url
    self.headers = headers
    self.MangaURL = MangaURL
    self.SaveName = SaveName
    self.MangaURL = NameMerge
    self.Image_URL = Image_URL
    self.ComicLink = ComicLink
    self.FolderName = FolderName
    self.pages_format = pages_format
    self.ComicsInternalLinks = ComicsInternalLinks

# 計算運行線程數
def Threading():
    count = 0
    while True:
        time.sleep(1)
        if threading.active_count() == 4:
            count += 1
        else:count = 0

        if count == 3:
            os._exit(0)

""" 較慢但通用多種下載 """
class SlowAccurate:
    # 判斷下載的類型
    DownloadType = False

    # 批量輸入下載
    def BatchInput(Url):
        # 用於確認輸出
        Judge = False
        AllLinks = []
    
        if isinstance(Url,list):

            SupportedFormat = r'^https:\/\/www\.wnacg\.org\/photos.*\d+\.html$'

            for url in Url:

                if re.match(SupportedFormat,url):
                    Judge = True
                    AllLinks.append(url)
                else:print("這並非支持的網址格式")

        else:
            url = unquote(Url)
            Match = False

            # r 為原始字串符 他將不會轉譯 \ 反斜
            SearchPage = r'https://www\.wnacg\.org/search/.*\?q=.+'
            TagPage = r'^https:\/\/www\.wnacg\.org\/albums.*'

            if re.match(SearchPage,url):
                url = f'https://www.wnacg.org/search/?q={url.split("?q=")[1].split("&")[0]}'
                Match = True
            elif re.match(TagPage,url):
                url = f'https://www.wnacg.org/albums-index-page-1-tag-{url.split("-tag-")[1]}'
                Match = True

            if Match:
                Judge = True
                headers = {
                    "authority": "www.wnacg.org",
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
                async def GetLink(session, url):
                    async with session.get(url) as response:
                        html = await response.text()
                        tree = etree.fromstring(html, parser)
                        links = []
                        for i in tree.xpath('//div[@class="pic_box"]'):
                            link = f"https://www.wnacg.org{i.find('a').get('href')}"
                            links.append(link)
                        return links

                # 將所有頁面網址輸出,再將網址全部使用GetLink獲取頁面所有網址
                async def RanGet(url):
                    async with aiohttp.ClientSession(headers=headers) as session:
                        PageList = []
                        for page in range(int(TotalPages)):
                            if int(TotalPages) != 1 and re.match(SearchPage,url):
                                url = f"https://www.wnacg.org/search/index.php?q={url.split('?q=')[1]}&m=&syn=yes&f=_all&s=&p={page+1}"
                            elif int(TotalPages) != 1 and re.match(TagPage,url):
                                url = f"https://www.wnacg.org/albums-index-page-{int(url.split('-')[3])+1}-tag-{url.split('-')[-1]}"
                            
                            PageList.append(url)

                        tasks = []
                        for page in PageList:
                            task = asyncio.create_task(GetLink(session, page))
                            tasks.append(task)
                        results = await asyncio.gather(*tasks)
                        for links in results:
                            AllLinks.extend(links)
                asyncio.run(RanGet(url))
            else:print("這並非支持的網址格式")

        if Judge:
            SlowAccurate.DownloadType = True
            for _input in AllLinks: # 懶得處理線程鎖,廢棄多線程
               SlowAccurate.BasicSettings(_input)

    # 取得基本訊息(這邊為了通用性,做了較多的數據處理,剛開始會跑比較久)
    Work = queue.Queue()
    def BasicSettings(Url):

        try:
            SupportedFormat = r'^https:\/\/www\.wnacg\.org\/photos.*\d+\.html$'

            if re.match(SupportedFormat,Url):

                ComicsInternalLinks = []
                ComicPictureLink = []

                session = requests.Session()
                headers = {
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
                }

                Url = f"https://www.wnacg.org/photos-index-{'page-1'}-aid-{Url.split('aid-')[1]}"
                reques = session.get(Url)
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
                        async with session.get(f"https://www.wnacg.org/photos-index-page-{i}-aid-{Url.split('aid-')[1]}") as response:
                            html = await response.text()
                            parser = etree.HTMLParser()
                            tree = etree.fromstring(html, parser)
                            internal_links = [f"https://www.wnacg.org{x.get('href')}" for x in tree.xpath("//div[@class='pic_box tb']/a")]
                            return internal_links

                # 使用異步同時發起請求 (只要不同時請求就不會發生數據重複,但是數據量多時,可能會很慢)
                async def LinkRun():
                    tasks = []
                    links_set = set()
                    for i in range(1, Home_Pages+1):
                        tasks.append(asyncio.create_task(GetImageLink(i, headers)))
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
                        tasks.append(asyncio.create_task(GetImage(link, headers)))
                    image_links = await asyncio.gather(*tasks)
                    for link in image_links:
                        ComicPictureLink.append(link)
                    ComicPictureLink.sort() #先暫時用這種方式排序

                asyncio.run(LinkRun())
                asyncio.run(ImageRun())

                if SlowAccurate.DownloadType:
                    # 同步請求,工作序列(同時下載多本)
                    SlowAccurate.Work.put((ComicPictureLink,Url,NameMerge))
                elif SlowAccurate.DownloadType == False:
                    # 單線程請求(適用於單本加速下載)
                    download_path = os.path.join(dir, NameMerge)
                    SlowAccurate.Ffolder(download_path)
                    SlowAccurate.SingleDownload(ComicPictureLink,Url,NameMerge)

            else:
                print("這並非支持的網址格式")

        except TypeError:
            print("請放單獨的漫畫網址")

    def DownloadWork():
        # 允許最大同時下載數
        MAX_THREADS = 10
        active_threads = []

        while True:
            time.sleep(0.1)
            if not SlowAccurate.Work.empty():
                data = SlowAccurate.Work.get()
                ComicPictureLink = data[0]
                Url = data[1]
                NameMerge = data[2]

                def Simultaneous():
                    download_path = os.path.join(dir, NameMerge)
                    #創建文件夾
                    SlowAccurate.Ffolder(download_path)
                    # 開始請求圖片
                    SlowAccurate.SimultaneousDownload(ComicPictureLink,Url,NameMerge)

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
    def SimultaneousDownload(ComicsInternalLinks,MangaURL,NameMerge):
        SaveNameFormat = 1

        headers = {
            "sec-fetch-dest": "image",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-site": "cross-site",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        }
        pbar = tqdm(total=len(ComicsInternalLinks),desc=NameMerge)
        for page in ComicsInternalLinks:
            SaveName = f"{SaveNameFormat:03d}.{page.split('/')[-1].split('.')[1]}"
            # 同時下載多本
            SlowAccurate.Download(os.path.join(dir, NameMerge),SaveName,MangaURL,page,headers)

            pbar.update(1)
            
            SaveNameFormat += 1

    # 轉換漫畫資訊 單本下載加速
    def SingleDownload(ComicsInternalLinks,MangaURL,NameMerge):
        SaveNameFormat = 1

        headers = {
            "sec-fetch-dest": "image",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-site": "cross-site",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        }

        pbar = tqdm(total=len(ComicsInternalLinks),desc=NameMerge)
        with concurrent.futures.ThreadPoolExecutor(max_workers=512) as executor:
            
            for page in ComicsInternalLinks:
                SaveName = f"{SaveNameFormat:03d}.{page.split('/')[-1].split('.')[1]}"
                # 單本下載加速     
                executor.submit(SlowAccurate.Download, os.path.join(dir, NameMerge) , SaveName, MangaURL , page , headers)

                pbar.update(1)

                SaveNameFormat += 1
                time.sleep(0.1)

    # 創建資料夾
    def Ffolder(FolderName):
        try:
            os.mkdir(FolderName) # 用漫畫名創建一個空資料夾(再傳遞時已經包含路徑+名稱)
        except:
            pass

    # 下載方法
    def Download(Path,SaveName,MangaURL,Image_URL,headers):

        ImageData = requests.get(Image_URL, headers=headers)
        if ImageData.status_code == 200:
            with open(os.path.join(Path, SaveName),"wb") as f:
                f.write(ImageData.content)
        else:print(f"請求錯誤:\n漫畫網址:{MangaURL}\n圖片網址:{Image_URL}")

""" 較快但有些下載不了 """
class FastNormal:

    # 批量輸入下載
    def BatchInput(Url):
        # 用於確認輸出
        Judge = False
        AllLinks = []

        if isinstance(Url,list):

            SupportedFormat = r'^https:\/\/www\.wnacg\.org\/photos.*\d+\.html$'

            for url in Url:

                if re.match(SupportedFormat,url):
                    Judge = True
                    AllLinks.append(url)
                else:print("這並非支持的網址格式")

        else:
            url = unquote(Url)
            Match = False
            # r 為原始字串符 他將不會轉譯 \ 反斜
            SearchPage = r'https://www\.wnacg\.org/search/.*\?q=.+'
            TagPage = r'^https:\/\/www\.wnacg\.org\/albums.*'

            if re.match(SearchPage,url):
                url = f'https://www.wnacg.org/search/?q={url.split("?q=")[1].split("&")[0]}'
                Match = True
            elif re.match(TagPage,url):
                url = f'https://www.wnacg.org/albums-index-page-1-tag-{url.split("-tag-")[1]}'
                Match = True

            if Match:
                Judge = True
                headers = {
                    "authority": "www.wnacg.org",
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
                            link = f"https://www.wnacg.org{i.find('a').get('href')}"
                            links.append(link)
                        return links

                # 將所有頁面網址輸出,再將網址全部使用GetLink獲取頁面所有網址
                async def RanGet(url):
                    async with aiohttp.ClientSession(headers=headers) as session:
                        PageList = []
                        for page in range(int(TotalPages)):
                            if int(TotalPages) != 1 and re.match(SearchPage,url):
                                url = f"https://www.wnacg.org/search/index.php?q={url.split('?q=')[1]}&m=&syn=yes&f=_all&s=&p={page+1}"
                            elif int(TotalPages) != 1 and re.match(TagPage,url):
                                url = f"https://www.wnacg.org/albums-index-page-{int(url.split('-')[3])+1}-tag-{url.split('-')[-1]}"
                            
                            PageList.append(url)

                        tasks = []
                        for page in PageList:
                            task = asyncio.create_task(GetLink(session, page))
                            tasks.append(task)
                        results = await asyncio.gather(*tasks)
                        for links in results:
                            AllLinks.extend(links)
                asyncio.run(RanGet(url))

            else:print("這並非支持的網址格式")

        if Judge:
            for _input in AllLinks:
                FastNormal.BasicSettings(_input)

    def BasicSettings(Url):
        SupportedFormat = r'^https:\/\/www\.wnacg\.org\/photos.*\d+\.html$'
        if re.match(SupportedFormat,Url):

            total_pages_format = []

            session = requests.Session()
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            }

            Url = f"https://www.wnacg.org/photos-index-{'page-1'}-aid-{Url.split('aid-')[1]}"
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
                    urllist = [f"https://www.wnacg.org/photos-index-page-{i}-aid-{Url.split('aid-')[1]}" for i in range(1, home_pages+1)]
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
            if SlowAccurate.PathStatus:
                os.chdir(os.path.join(".."))
            else:SlowAccurate.PathStatus = True
        
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

"""
    !! 使用前請詳閱說明書

    爬蟲適用網站 : https://www.wnacg.org/
    使用說明 : 輸入該漫畫的網址,接著就會自動下載 (支援: 搜尋頁面 / Tag頁面 / 漫畫頁面)

    前面為 : SlowAccurate. 是慢速下載但是可以很精準的抓到所有類型
    (目前只有他支援批量下載時,可同時下載10本)

    前面為 : FastNormal. 處理的比較快 同時無法完全的通用 目前已經用多重判斷 盡量讓其通用
    (但只要頁面較多處理就一定比較久 , 懶得修復其功能性)

    !! 重要不要同時使用超過一種的下載方式 , 批量就批量 , 單獨就單獨 , 不然數據可能會出錯

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    BatchInput 只能放一種,只有漫畫頁面
    1. BasicSettings (格式為:https://www.wnacg.org/photos...)

    BatchInput 可放三種 (注意格式!!)
    1. 為搜尋某Tag標籤搜尋頁網址 , 他將會把所有搜尋到的全部下載 (格式為:https://www.wnacg.org/albums...)
    2. 搜尋的網址連結 (格式為:https://www.wnacg.org/search/index.php?q=...)
    3. Batch , 同時放置多個需下載的(無上限) , 漫畫頁面網址 (格式為:https://www.wnacg.org/photos...)

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    [+] SlowAccurate 方法更新進度條顯示 , 批量下載顯示可能有Bug
    [*] 待修復重複下載漫畫下載問題
    
"""

if __name__ == "__main__":

    """計算運行線程,用於結束程式運行"""
    threading.Thread(target=Threading).start()
    """加速工作隊列"""
    threading.Thread(target=SlowAccurate.DownloadWork).start()

    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

    # 批量下載列表(以列表的方式,放入多個漫畫網址,最後將 Batch 放至批量下載進行傳遞)
    Batch = [
        "",
    ]

    """處理速度較於緩慢(那種2-300頁的真的很慢),但可精準的下載所有類型"""

    # 單獨下載
    #SlowAccurate.BasicSettings("")
    # 批量下載
    SlowAccurate.BatchInput("")

    """處理速度較於快速,但會有一些下載失敗(懶得修復問題,不建議使用)"""

    # 單獨下載
    #FastNormal.BasicSettings("#")

    # 批量下載
    # FastNormal.BatchInput("")