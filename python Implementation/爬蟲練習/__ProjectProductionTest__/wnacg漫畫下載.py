from urllib.parse import unquote
from bs4 import BeautifulSoup
from lxml import etree , html
import concurrent.futures
import threading
import requests
import queue
import time
import os
import re
dir = os.path.dirname(os.path.abspath("R:/")) # 可更改預設路徑
os.chdir(dir)

# 程式入口點於最下方

# 初始化宣告
def __init__(self,Url,ComicsInternalLinks,MangaURL,FolderName,SaveName,Image_URL,headers,pages_format,ComicLink):
    self.Url = Url
    self.headers = headers
    self.MangaURL = MangaURL
    self.SaveName = SaveName
    self.Image_URL = Image_URL
    self.ComicLink = ComicLink
    self.FolderName = FolderName
    self.pages_format = pages_format
    self.ComicsInternalLinks = ComicsInternalLinks

# 較慢但通用多種下載
class SlowAccurate:

    # 批量輸入下載
    def BatchInput(Url):
        Judge = False
        AllLinks = []

        if isinstance(Url,list):

            SupportedFormat = r'^https:\/\/www\.wnacg\.org\/photos.*\d+\.html$'

            for url in Url:

                if re.match(SupportedFormat,url):
                    Judge = True
                    AllLinks.append(url)
                else:print("這並非此模支持的網址格式")

        else:
            # r 為原始字串符 他將不會轉譯 \ 反斜
            TagPage = r'^https:\/\/www\.wnacg\.org\/albums.*\.html$'
            # 轉換被轉譯的文字
            url = unquote(Url)

            if re.match(TagPage,url):
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
                bs4 = BeautifulSoup(request.text, "html.parser")

                # 獲取總共的頁數(只有一頁的會錯誤)
                try:
                    for i in bs4.select("div.f_left.paginator"):TotalPages = i.find_all("a")[-2].text
                except:TotalPages = "1"

                # 獲取頁面所有URL
                def GetLink(url,headers,UrlQueue):
                    bs4 = BeautifulSoup(session.get(url, headers=headers).text, "html.parser")
                    for i in bs4.select("div.pic_box"):
                        UrlQueue.put(f"https://www.wnacg.org{i.find('a')['href']}")

                # 使用隊列
                UrlQueue = queue.Queue()
                for page in range(int(TotalPages)):
                    # 啟用多線程同時去獲取頁面URL
                    thread = threading.Thread(target=GetLink,args=(url,headers,UrlQueue))
                    thread.start()

                    # 改變URL格式
                    if int(TotalPages) != 1:
                        url = f"https://www.wnacg.org/albums-index-page-{int(url.split('-')[3])+1}-tag-{url.split('-')[-1]}"

                # 等待所有URL獲取完畢
                thread.join()

                # 取得所有的URL並傳入 AllLinks
                while not UrlQueue.empty():
                    AllLinks.append(UrlQueue.get())

            else:print("這並非此模支持的網址格式")

        if Judge:
            for _input in AllLinks: # 懶得處理線程鎖,廢棄多線程
                SlowAccurate.BasicSettings(_input)

    # 取得基本訊息(這邊為了通用性,做了較多的數據處理,導致剛開始會跑比較久)
    def BasicSettings(Url):
        SupportedFormat = r'^https:\/\/www\.wnacg\.org\/photos.*\d+\.html$'
        if re.match(SupportedFormat,Url):

            ComicsInternalLinks = []

            session = requests.Session()
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            }
            
            Url = f"https://www.wnacg.org/photos-index-{'page-1'}-aid-{Url.split('aid-')[1]}"
            reques = session.get(Url)
            bs4 = BeautifulSoup(reques.text, "html.parser")

            # 主頁最終頁數
            Home_Pages = int(re.findall(r'\d+', bs4.select("div.f_left.paginator")[0].text)[-1])

            # 漫畫名稱
            NameProcessing = bs4.select_one("h2").text.strip()
            NameMerge = NameProcessing

            # 多線程獲取所有圖片的連結
            def GetImageLink(i, headers, UrlQueue):
                request = session.get(f"https://www.wnacg.org/photos-index-page-{i}-aid-{Url.split('aid-')[1]}", headers=headers)
                tree = html.fromstring(request.content)
                for x in tree.cssselect("div.pic_box.tb a"):
                    request = session.get(f"https://www.wnacg.org{x.get('href')}", headers=headers)
                    tree = html.fromstring(request.content)
                    UrlQueue.put(f'https:{tree.cssselect("img#picarea.photo")[0].get("src")}')

            UrlQueue = queue.Queue()
            threads = []

            for i in range(1,Home_Pages+1):
                thread = threading.Thread(target=GetImageLink,args=(i,headers,UrlQueue))
                thread.start()
                threads.append(thread)

            # 為了確保每次資料都是完整正確的
            for thread in threads:
                thread.join()

            while not UrlQueue.empty():
                ComicsInternalLinks.append(UrlQueue.get())

            #創建文件夾
            SlowAccurate.Ffolder(NameMerge)

            # 開始請求圖片
            SlowAccurate.DataRequest(ComicsInternalLinks,Url)

        else:
            print("這並非此模支持的網址格式")

    # 獲取漫畫數據
    def DataRequest(ComicsInternalLinks,MangaURL):
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

        with concurrent.futures.ThreadPoolExecutor(max_workers=128) as executor:

            for page in ComicsInternalLinks:
    
                SaveName = f"{SaveNameFormat:03d}.{page.split('/')[-1].split('.')[1]}"
                time.sleep(0.1)
                executor.submit(SlowAccurate.Download, SaveName, MangaURL , page , headers)
                print(SaveName)
  
                SaveNameFormat += 1

    PathStatus = False
    # 創建資料夾
    def Ffolder(FolderName):
        if SlowAccurate.PathStatus:
            os.chdir(os.path.join(".."))
        else:SlowAccurate.PathStatus = True
        
        try:
            #刪除名稱中的非法字元
            name = re.sub(r'[<>:"/\\|?*]', '', FolderName)
            os.mkdir(name) # 在該路徑下用漫畫名創建一個空資料夾
            os.chdir(os.path.join(os.getcwd(), name)) # 將預設路徑導入至該資料夾
        except:pass

    # 下載方法
    def Download(SaveName,MangaURL,Image_URL,headers):

        ImageData = requests.get(Image_URL, headers=headers)
        if ImageData.status_code == 200:
            with open(SaveName,"wb") as f:
                f.write(ImageData.content)
        else:print(f"請求錯誤:\n漫畫網址:{MangaURL}\n圖片網址:{Image_URL}")

# 較快但有些下載不了
class FastNormal:

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

            # 使用多線程獲取所有的頁數格式
            def GetFormat(i,headers,UrlQueue):
                reques = session.get(f"https://www.wnacg.org/photos-index-page-{i}-aid-{Url.split('aid-')[1]}", headers=headers)
                html = reques.content
                parser = etree.HTMLParser()
                tree = etree.fromstring(html, parser)
                for span in tree.xpath('//span[@class="name tb"]'):
                    UrlQueue.put(span.text)

            UrlQueue = queue.Queue()
            threads = []

            for i in range(1,Home_Pages+1):
                thread = threading.Thread(target=GetFormat,args=(i,headers,UrlQueue))
                thread.start()
                threads.append(thread)

            # 為了確保每次資料都是完整正確的
            for thread in threads:
                thread.join()

            while not UrlQueue.empty():
                total_pages_format.append(UrlQueue.get())
            
            #創建文件夾
            FastNormal.Ffolder(NameMerge)
            # 開始請求圖片
            FastNormal.DataRequest(total_pages_format,ComicLink,Url)
        else:
            print("這並非此模支持的網址格式")

    # 批量輸入下載
    def BatchInput(Url):
        Judge = False
        AllLinks = []

        if isinstance(Url,list):

            SupportedFormat = r'^https:\/\/www\.wnacg\.org\/photos.*\d+\.html$'

            for url in Url:

                if re.match(SupportedFormat,url):
                    Judge = True
                    AllLinks.append(url)
                else:print("這並非此模支持的網址格式")

        else:
            # r 為原始字串符 他將不會轉譯 \ 反斜
            TagPage = r'^https:\/\/www\.wnacg\.org\/albums.*\.html$'
            # 轉換被轉譯的文字
            url = unquote(Url)

            if re.match(TagPage,url):
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
                    TotalPages = tree.xpath('//div[@class="f_left paginator"]/a[last()-1]/text()')[0]
                except:TotalPages = "1"

                # 獲取頁面所有URL
                def GetLink(url,headers,UrlQueue):
                    request = session.get(url, headers=headers)
                    tree = etree.fromstring(request.content, parser)
                    for i in tree.xpath('//div[@class="pic_box"]'):
                        UrlQueue.put(f"https://www.wnacg.org{i.find('a')['href']}")

                # 使用隊列
                UrlQueue = queue.Queue()
                for page in range(int(TotalPages)):
                    # 啟用多線程同時去獲取頁面URL
                    thread = threading.Thread(target=GetLink,args=(url,headers,UrlQueue))
                    thread.start()

                    # 改變URL格式
                    if int(TotalPages) != 1:
                        url = f"https://www.wnacg.org/albums-index-page-{int(url.split('-')[3])+1}-tag-{url.split('-')[-1]}"

                # 等待所有URL獲取完畢
                thread.join()

                # 取得所有的URL並傳入 AllLinks
                while not UrlQueue.empty():
                    AllLinks.append(UrlQueue.get())

            else:print("這並非此模支持的網址格式")

        if Judge:
            for _input in AllLinks:
                FastNormal.BasicSettings(_input)

    # 獲取漫畫數據
    def DataRequest(pages_format,ComicLink,MangaURL):
        SaveNameFormat = 1
        Mantissa = ComicLink[0].split('t')[1]
        NumberType = ['1','2','3','4']

        headers = {
            "sec-fetch-dest": "image",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-site": "cross-site",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        }

        with concurrent.futures.ThreadPoolExecutor(max_workers=128) as executor:

            for page in pages_format:

                Picture_Name = f"{page}.{ComicLink[5].split('.')[1]}"
                Image_URL = f"https://img{Mantissa}/{ComicLink[1]}/{ComicLink[3]}/{ComicLink[4]}/{Picture_Name}"
    
                SaveName = f"{SaveNameFormat:03d}.{ComicLink[5].split('.')[1]}"

                time.sleep(0.1)
                print(SaveName)
                status = executor.submit(FastNormal.Download, SaveName, Image_URL, headers)
    
                # 無腦判斷法 (使用回傳判斷會降低運行效率)
                if status.result().status_code != 200:

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
                            break
                    
                    # 如果到最後還是請求失敗,就打印失敗的格式
                    if status.result().status_code != 200:print(f"請求錯誤:\n漫畫網址:{MangaURL}\n圖片網址:{Image_URL}")

                SaveNameFormat += 1

    PathStatus = False
    # 創建資料夾
    def Ffolder(FolderName):
        try:
            if SlowAccurate.PathStatus:
                os.chdir(os.path.join(".."))
            else:SlowAccurate.PathStatus = True
        
            #刪除名稱中的非法字元
            name = re.sub(r'[<>:"/\\|?*]', '', FolderName)
            os.mkdir(name) # 在該路徑下用漫畫名創建一個空資料夾
            os.chdir(os.path.join(os.getcwd(), name)) # 將預設路徑導入至該資料夾
        except:pass

    # 下載方法
    def Download(SaveName,Image_URL,headers):

        ImageData = requests.get(Image_URL, headers=headers)
        if ImageData.status_code == 200:
            with open(SaveName,"wb") as f:
                f.write(ImageData.content)
        else:
            if Image_URL.split('/')[-1].split('.')[1] == "jpg":

                Image_URL = Image_URL.replace(".jpg", ".png")

            elif Image_URL.split('/')[-1].split('.')[1] == "png":

                Image_URL = Image_URL.replace(".jpg", ".png")

            ImageData = requests.get(Image_URL, headers=headers)

            if ImageData.status_code == 200:
                with open(SaveName,"wb") as f:
                    f.write(ImageData.content)
            else:pass

        return ImageData

"""
    https://www.wnacg.org/
    使用說明 : 輸入該漫畫的網址,接著就會自動下載 (中文被轉譯,或是Page不是第1頁都沒有問題)

    BatchInput 可放兩種
    1. 為搜尋某Tag標籤搜尋頁網址 , 他將會把所有搜尋到的全部下載 (格式為:https://www.wnacg.org/albums...)
    2. Batch , 同時放置多個需下載的(無上限) , 漫畫頁面網址 (格式為:https://www.wnacg.org/photos...)

    前面為 : SlowAccurate. 是慢速下載但是可以很精準的抓到所有類型
    前面為 : FastNormal. 處理的比較快 同時無法完全的通用 目前已經用多重判斷 盡量讓其通用

    Bug待測試
    
"""

if __name__ == "__main__":

    # 批量下載列表
    Batch = [
        "",
    ]

    """處理速度較於緩慢,但可精準的下載所有類型"""

    # 單獨下載
    #SlowAccurate.BasicSettings("#")

    # 批量下載
    #SlowAccurate.BatchInput("#")


    """處理速度較於快速,但會有一些下載失敗"""

    # 單獨下載
    FastNormal.BasicSettings("#")

    # 批量下載
    #FastNormal.BatchInput("#")