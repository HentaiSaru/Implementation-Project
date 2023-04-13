from bs4 import BeautifulSoup
import concurrent.futures
import requests
import time
import os
import re

# 程式入口點於最下方

# 下載方法
def download(SaveName, Image_URL, headers):
    
    ImageData = requests.get(Image_URL, headers=headers)
    
    if ImageData.status_code == 200:
        with open(SaveName,"wb") as f:
            f.write(ImageData.content)

# 創建資料夾
def Ffolder(name):
    dir = os.path.dirname(os.path.abspath("R:/")) # 可更改預設路徑
    os.chdir(dir)
    try:
        os.mkdir(name) # 在該路徑下用漫畫名創建一個空資料夾
        os.chdir(os.path.join(os.getcwd(), name)) # 將預設路徑導入至該資料夾
    except:pass

# 獲取漫畫數據
def DataRequest(pages_format,ComicLink,NameMerge):
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

            time.sleep(0.1)
 
            SaveName = f"{SaveNameFormat:03d}.{ComicLink[4].split('.')[1]}"
            
            executor.submit(download, SaveName, Image_URL, headers)

            SaveNameFormat += 1
            
            print(SaveName)

# 取得基本訊息(這邊為了通用性,做了較多的數據處理,導致剛開始會跑比較久)
def BasicSettings(Url):

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
    DataRequest(total_pages_format,ComicLink,NameMerge)

if __name__ == "__main__":

    # 只需輸入該漫畫的網址,接下來就會自動下載
    # 如需更改路徑在 Ffolder() 更改
    BasicSettings("#")