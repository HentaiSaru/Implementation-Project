from bs4 import BeautifulSoup
import concurrent.futures
import requests
import time
import os

# 程式入口點於最下方

# 下載方法
def download(Picture_Name, Image_URL, headers):
    ImageData = requests.get(Image_URL, headers=headers)
    with open(Picture_Name,"wb") as f:
        f.write(ImageData.content)

# 創建資料夾
def Ffolder(name):
    dir = os.path.dirname(os.path.abspath("R:/")) # 可更改預設路徑
    os.chdir(dir)
    try:os.mkdir(name) # 在該路徑下用漫畫名創建一個空資料夾
    except:pass

# 獲取漫畫數據
def DataRequest(totalpages,firstpage,ComicLink,NameMerge):
    # 將路徑重新指向到創建的資料夾
    new_dir = os.path.join(os.getcwd(),NameMerge)
    os.chdir(new_dir)

    pages = 1
    nameformat = len(firstpage)

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    }

    with concurrent.futures.ThreadPoolExecutor(max_workers=64) as executor:

        for i in range(int(totalpages)):

            page = pages+i
            page = f"{page:0{nameformat}d}"

            Picture_Name = f"{page}.{ComicLink[4].split('.')[1]}"
            Image_URL = f"https://img4.qy0.ru/{ComicLink[0]}/{ComicLink[2]}/{ComicLink[3]}/{Picture_Name}"

            time.sleep(0.3)

            executor.submit(download, Picture_Name, Image_URL, headers)

            print(Image_URL)

# 取得基本訊息    
def BasicSettings(Url):
     
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    }

    reques = requests.get(Url, headers=headers)

    bs4 = BeautifulSoup(reques.text, "html.parser")
    NameProcessing = bs4.select("h2")[0].text

    # 作者名稱
    #Author = NameProcessing[0].strip("[]")
    # 漫畫名稱
    #MangaName = NameProcessing[1]
    # 作者+漫畫名合併
    #NameMerge = f"({Author}){MangaName}"
    NameMerge = NameProcessing

    # 總頁數
    totalpages = bs4.select("div.asTBcell.uwconn")[0].find_all("label")[1].text.strip("頁數：P")
    # 漫畫連結
    firstpage = bs4.select("span.name.tb")[0].text
    # 漫畫圖片連結
    ComicLink = bs4.select("div.pic_box.tb")[0].find("img").get("src").split("//t4.qy0.ru/")[1].split("/")

    #創建文件夾
    Ffolder(NameMerge)

    # 開始請求圖片
    DataRequest(totalpages,firstpage,ComicLink,NameMerge)

if __name__ == "__main__":

    # 只需輸入該漫畫的網址,接下來就會自動下載
    # 如需更改路徑在 Ffolder() 更改
    BasicSettings("#")