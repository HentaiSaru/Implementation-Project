from urllib.parse import unquote
from bs4 import BeautifulSoup
import concurrent.futures
import threading
import requests
import queue
import time
import os
import re

# 程式入口點於最下方
# 線程鎖 lock = threading.Lock() 棄用

# 下載方法
def Download(SaveName, Image_URL, headers):
    
    ImageData = requests.get(Image_URL, headers=headers)
    
    if ImageData.status_code == 200:
        with open(SaveName,"wb") as f:
            f.write(ImageData.content)
    else: print(f"請求失敗:{Image_URL}")

# 創建資料夾
def Ffolder(name):
    dir = os.path.dirname(os.path.abspath("R:/")) # 可更改預設路徑
    os.chdir(dir)
    try:
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

            Picture_Name = f"{page}.{ComicLink[4].split('.')[1]}"
            Image_URL = f"https://img4.qy0.ru/{ComicLink[0]}/{ComicLink[2]}/{ComicLink[3]}/{Picture_Name}"
 
            SaveName = f"{SaveNameFormat:03d}.{ComicLink[4].split('.')[1]}"
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
        if Url.find("page") == -1:
            Url = f"https://www.wnacg.org/photos-index-{'page-1'}-aid-{Url.split('aid-')[1]}"
        reques = session.get(Url, headers=headers)
        bs4 = BeautifulSoup(reques.text, "html.parser")
        # 主頁頁數
        Home_Pages = re.findall(r'\d+', bs4.select("div.f_left.paginator")[0].text)
        # 漫畫名稱
        NameProcessing = bs4.select_one("h2").text.strip()
        NameMerge = NameProcessing
        # 漫畫圖片連結
        ComicLink = bs4.select_one("div.pic_box.tb img")["src"].split("//t4.qy0.ru/")[1].split("/")
        for i in Home_Pages:
            reques = session.get(f"https://www.wnacg.org/photos-index-page-{i}-aid-{Url.split('aid-')[1]}", headers=headers)
            bs4 = BeautifulSoup(reques.text, "html.parser")
            # 所有的頁數格式獲取
            total_pages_format += [span.text for span in bs4.select("span.name.tb")]
        
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

            # 獲取總共的頁數
            for i in bs4.select("div.f_left.paginator"):TotalPages = i.find_all("a")[-2].text

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
                url = f"https://www.wnacg.org/albums-index-page-{int(url.split('-')[3])+1}-tag-{url.split('-')[-1]}"
    
            # 等待所有URL獲取完畢
            thread.join()

            # 取得所有的URL並傳入 AllLinks
            while not UrlQueue.empty():
                AllLinks.append(UrlQueue.get())

        else:print("這並非此模支持的網址格式")

    if Judge:
        for _input in AllLinks:
            BasicSettings(_input)

if __name__ == "__main__":

    # 輸入該漫畫的網址,接下來就會自動下載
    # 下載路徑在 Ffolder() 更改

    """ 開始下載 """

    #BasicSettings("#")
    

    """
        BatchInput 可放兩種 (批量下載存在Bug,正在開發中)
        1. 為搜尋某Tag標籤搜尋頁網址 , 他將會把所有搜尋到的全部下載 (格式為:https://www.wnacg.org/albums...)
        2. Batch , 同時放置多個需下載的 , 漫畫頁面網址 (格式為:https://www.wnacg.org/photos...)
    """
    Batch = [
        "#",
        "#",
    ]

    BatchInput("#")