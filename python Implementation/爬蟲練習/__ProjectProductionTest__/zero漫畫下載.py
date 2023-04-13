from bs4 import BeautifulSoup
import concurrent.futures
import threading
import requests
import opencc
import time
import os
import re
# 可設置下載的位置
dir = os.path.dirname(os.path.abspath("R:/"))
os.chdir(dir)

# 程式入口點於最下方
# 無法下載第一話就需要VIP權限的(第一話可直接觀看,第二話需要VIP,這種的可以)

# 簡中轉繁
def Converter(language):
    converter = opencc.OpenCC('s2twp.json')
    return converter.convert(language)

# 圖片下載輸出(因為該網站速度不快,使用多線程也沒快多少)
def download(comicname,number,pages,comicurl,_format):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    comic = requests.get(f"http://tupa.zerobyw4090.com/manhua/{comicurl}",headers=headers)

    if comic.status_code == 200:
        with open(f"{comicname} 第{number}話 - {int(pages)+1}.{_format}","wb") as f:
                f.write(comic.content)

# 特別頁面取的頁數
def special_format(link,url):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }

    if url.find("special") != -1:
        try:
            request = requests.get(link,headers=headers)
            request = BeautifulSoup(request.text, "html.parser")
            request = request.select('img#img_0')[0].get('src').split("/")[-1].split(".")[0]
        except:pass

        return request

# 懶人批量下載
def default_download(allchapters,alllinks,finallink,comicname):

    cache = coding = ""
    ImageFormat = finallink.split(".")[1]

    for idx , chapters in enumerate(allchapters):

        if chapters == cache:
            coding = f"{chapters}sheng"
            pages = special_format(alllinks[idx],"special")
        else:
            coding = chapters
            pages = finallink.split("/")[2].split(".")[0]
        
        cache = chapters

        with concurrent.futures.ThreadPoolExecutor(max_workers=64) as executor:

            for i in range(1000):

                time.sleep(0.1)

                if len(pages) == 3:
                    page = int(pages)+i
                    page = f"{page:03d}"
                elif len(pages) == 2:
                    page = int(pages)+i
                    page = f"{page:02d}"
                elif len(pages) == 1:
                    page = int(pages)+i
                    page = f"{page:01d}"

                picturelink = "{}/{}/{}.{}".format(finallink.split("/")[0],coding,page,ImageFormat)

                if i < 10:
                    i = "0"+str(i)

                comic = executor.submit(download,comicname,coding,i,picturelink,ImageFormat)

                if int(comic.result().status_code) != 200:break

                print(picturelink)
        
        idx + 1

# 自訂客制化下載
def custom_download(url,chapter,Format,ImageFormat):
     
    head = {
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja-TW;q=0.6,ja;q=0.5",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "DNT": "1",
        "Pragma": "no-cache",
        "sec-gpc": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }

    req1 = requests.get(url,headers=head)
    ma = BeautifulSoup(req1.text, "html.parser")
    comicname = Converter(ma.find("h3", class_=("uk-heading-line mt10 m10")).text.split(" ")[0])
    comiclink = f"http://www.zerobyw4090.com/{ma.select_one('div.muludiv a')['href'].split('./')[1]}"
    req2 = requests.get(comiclink,headers=head)
    mb = BeautifulSoup(req2.text, "html.parser")

    try:
        finallink = mb.select('img#img_0')[0].get('src').split("manhua/")[1]
        pages = int(finallink.split("/")[2].split(".")[0])

        with concurrent.futures.ThreadPoolExecutor(max_workers=64) as executor:
            for i in range(1000):

                pages = pages+i
                p = f"{pages:0{Format}d}"

                picturelink = "{}/{}/{}.{}".format(finallink.split("/")[0],chapter,p,ImageFormat)

                if i < 10:
                    i = "0"+str(i)

                comic = executor.submit(download,comicname,chapter,i,picturelink,ImageFormat)

                print(comic.result().url)

                if int(comic.result().status_code) != 200:break
    except:
        print("不支援第一話就需要VIP的漫畫")

# 設置批量下載的
def download_settings(url):

    head = {
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "ccept-Encoding": "gzip, deflate",
        "ccept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja-TW;q=0.6,ja;q=0.5",
        "ache-Control": "no-cache",
        "onnection": "keep-alive",
        "NT": "1",
        "ost": "tupa.zerobyw4090.com",
        "ragma": "no-cache",
        "ec-gpc": "1",
        "ser-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    requests1 = requests.get(url,headers=head)
    ma = BeautifulSoup(requests1.text, "html.parser")

    allchapters = []
    alllinks = []
    comicname = Converter(ma.find("h3", class_=("uk-heading-line mt10 m10")).text.split(" ")[0])
    comiclink = f"http://www.zerobyw4090.com/{ma.select_one('div.muludiv a')['href'].split('./')[1]}"

    for i in ma.select("div.uk-grid-collapse.uk-child-width-1-4")[0].find_all("a"):
        allchapters.append(''.join(re.findall(r'\d+', i.text)))

    for i in ma.select("div.uk-grid-collapse.uk-child-width-1-4")[0].find_all("a"):
        alllinks.append(f"http://www.zerobyw4090.com/{i.get('href').split('./')[1]}")

    requests2 = requests.get(comiclink,headers=head)
    mb = BeautifulSoup(requests2.text, "html.parser")
    finallink = mb.select('img#img_0')[0].get('src').split("manhua/")[1]

    default_download(allchapters,alllinks,finallink,comicname)
            
if __name__ == "__main__":

    """懶人批量下載"""
    # 網址 (如果601,602 這種頁面類型,使用懶人批量下載失敗,用自訂下載 ,修改 命名格式 1~3 或 副檔名 jpg/png)
    #download_settings("#")

    """自訂下載(用於當批量下載不到,可以賭運氣看看)"""
    # 網址 , 章節數 , jpg命名格式(1=1 , 2=01 , 3=001) , 圖片副檔名
    custom_download("#",602,3,"png")