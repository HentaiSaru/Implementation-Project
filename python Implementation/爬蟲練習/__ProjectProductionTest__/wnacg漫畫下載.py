from urllib.parse import unquote
from bs4 import BeautifulSoup
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

# 下載方法
def Download(SaveName, Image_URL, headers):
    
    ImageData = requests.get(Image_URL, headers=headers)
    
    if ImageData.status_code == 200:
        with open(SaveName,"wb") as f:
            f.write(ImageData.content)
    else: print(f"請求失敗:{Image_URL}")

# 創建資料夾
def Ffolder(name):
    os.chdir(os.path.join(os.getcwd(),".."))
    try:
        #刪除名稱中的非法字元
        name = re.sub(r'[<>:"/\\|?*]', '_', name)
        os.mkdir(name) # 在該路徑下用漫畫名創建一個空資料夾
        os.chdir(os.path.join(os.getcwd(), name)) # 將預設路徑導入至該資料夾
    except:pass

# 獲取漫畫數據
def DataRequest(pages_format,ComicLink):
    SaveNameFormat = 1
    
    headers = {
        "authority": "img4.qy0.ru",
        "sec-fetch-dest": "image",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-site": "cross-site",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-gpc": "1",
        "referer": "https://img4.qy0.ru/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    }

    with concurrent.futures.ThreadPoolExecutor(max_workers=128) as executor:
        
        for page in pages_format:

            Picture_Name = f"{page}.{ComicLink[5].split('.')[1]}"
            Image_URL = f"https://img{ComicLink[0].split('t')[1]}/{ComicLink[1]}/{ComicLink[3]}/{ComicLink[4]}/{Picture_Name}"
 
            SaveName = f"{SaveNameFormat:03d}.{ComicLink[5].split('.')[1]}"
            print(SaveName)

            time.sleep(0.1)
            executor.submit(Download, SaveName, Image_URL, headers)

            SaveNameFormat += 1

# 取得基本訊息(這邊為了通用性,做了較多的數據處理,導致剛開始會跑比較久)
def BasicSettings(Url):
    SupportedFormat = r'^https:\/\/www\.wnacg\.org\/photos.*\d+\.html$'
    if re.match(SupportedFormat,Url):

        total_pages_format = []
        Home_Pages = []

        session = requests.Session()
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        }

        Url = f"https://www.wnacg.org/photos-index-{'page-1'}-aid-{Url.split('aid-')[1]}"
        reques = session.get(Url)
        bs4 = BeautifulSoup(reques.text, "html.parser")

        # 主頁頁數
        Home_Pages = re.findall(r'\d+', bs4.select("div.f_left.paginator")[0].text)

        # 漫畫名稱
        NameProcessing = bs4.select_one("h2").text.strip()
        NameMerge = NameProcessing
        
        # 漫畫圖片連結
        #ComicLink = re.split(r"//t\d\.qy\d\.ru/", bs4.select_one("div.pic_box.tb img")["src"])[1].split("/")
        ComicLink = [x for x in bs4.select_one("div.pic_box.tb img")["src"].split("/") if x]

        # 使用多線程獲取所有的頁數格式
        def GetFormat(i,headers,UrlQueue):
            reques = session.get(f"https://www.wnacg.org/photos-index-page-{i}-aid-{Url.split('aid-')[1]}", headers=headers)
            bs4 = BeautifulSoup(reques.text, "html.parser")
            for span in bs4.select("span.name.tb"):
                UrlQueue.put(span.text)

        UrlQueue = queue.Queue()
        threads = []

        for i in Home_Pages:
            thread = threading.Thread(target=GetFormat,args=(i,headers,UrlQueue))
            thread.start()
            threads.append(thread)

        # 為了確保每次資料都是完整正確的
        for thread in threads:
            thread.join()

        while not UrlQueue.empty():
            total_pages_format.append(UrlQueue.get())

        #創建文件夾
        Ffolder(NameMerge)
        # 開始請求圖片
        DataRequest(total_pages_format,ComicLink)

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
            BasicSettings(_input)

"""
    https://www.wnacg.org/
    使用說明 : 輸入該漫畫的網址,接著就會自動下載

    BatchInput 可放兩種
    1. 為搜尋某Tag標籤搜尋頁網址 , 他將會把所有搜尋到的全部下載 (格式為:https://www.wnacg.org/albums...)
    2. Batch , 同時放置多個需下載的(無上限) , 漫畫頁面網址 (格式為:https://www.wnacg.org/photos...)

    Bug說明 : 基本上已經盡量取得正確的URL了 , 但是如果下載途中卡住 , 基本上都是因為
    可能他前面都是.jpg , 突然摻雜了一個.png , 就會導致用錯誤的網址去請求 , 就會卡在那邊 , 之後會顯示請求失敗的網址 , 改成另一種格式就可以

    可能的解決方案為 : 使用自動化操作取得正確的網址格式 , 因為該網站的圖片顯示 , 是在同樣的網頁框架 , 去請求圖片 , 所以會變化的只有圖片網址
    無法達成 , 請求整個網頁框架 , 再去獲取網址的操作(沒辦法換頁)
"""

if __name__ == "__main__":


    """ 單獨下載 """

    #BasicSettings("")

    
    """ 批量下載 """

    Batch = [
        "",
    ]

    BatchInput(Batch)