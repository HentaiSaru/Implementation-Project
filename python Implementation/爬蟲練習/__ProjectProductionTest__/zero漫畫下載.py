from bs4 import BeautifulSoup
import threading
import requests
import opencc
import time
import os
# 可設置下載的位置
dir = os.path.dirname(os.path.abspath("R:/"))
os.chdir(dir)

# 程式入口點於最下方
# 無法下載第一話就需要VIP權限的(第一話可直接觀看,第二話需要VIP,這種的可以)

def download(comicname,j,i,comic):

    with open(f"{comicname}_{j}_{i}.jpg","wb") as f:
                f.write(comic.content)

def Converter(language):
    converter = opencc.OpenCC('s2twp.json')
    return converter.convert(language)

def comic_crawling(url):

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
    request = requests.get(f"http://tupa.zerobyw4090.com/manhua/{url}",head)
    return request

def default_download(chapter,finallink,comicname):

    pages = finallink.split("/")[2].split(".")[0]

    for j in range(1,chapter+1):

        for i in range(1000):

            time.sleep(0.5)

            if len(pages) == 3:
                page = int(pages)+i
                p = f"{page:03d}"
            elif len(pages) == 2:
                page = int(pages)+i
                p = f"{page:02d}"
            elif len(pages) == 1:
                page = int(pages)+i
                p = f"{page:01d}"

            flink = "{}/{}/{}.jpg".format(finallink.split("/")[0],j,p)
            print(flink)

            comic = comic_crawling(flink) 
            if comic.status_code != 200:break
                
            if i < 10:
                i = "0"+str(i)

            threading.Thread(target=download,args=(comicname,j,i,comic)).start()

def custom_download(url,chapter,Format):
     
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
    req1 = requests.get(url,headers=head)
    ma = BeautifulSoup(req1.text, "html.parser")
    comicname = Converter(ma.find("h3", class_=("uk-heading-line mt10 m10")).text.split(" ")[0])
    comiclink = f"http://www.zerobyw4090.com/{ma.select_one('div.muludiv a')['href'].split('./')[1]}"
    req2 = requests.get(comiclink,headers=head)
    mb = BeautifulSoup(req2.text, "html.parser")

    try:
        finallink = mb.select('img#img_0')[0].get('src').split("manhua/")[1]

        for i in range(1000):

            pages = int(finallink.split("/")[2].split(".")[0])
            pages = pages+i
            p = f"{pages:0{Format}d}"

            flink = "{}/{}/{}.jpg".format(finallink.split("/")[0],chapter,p)
            print(flink)
            comic = comic_crawling(flink) 

            if i < 10:
                i = "0"+str(i)

            if comic.status_code != 200:break

            time.sleep(0.5)
            threading.Thread(target=download,args=(comicname,chapter,i,comic)).start()
    except:
        print("不支援第一話就需要VIP的漫畫")

def download_settings(url,chapter):

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
    req1 = requests.get(url,headers=head)
    ma = BeautifulSoup(req1.text, "html.parser")
    comicname = Converter(ma.find("h3", class_=("uk-heading-line mt10 m10")).text.split(" ")[0])
    comiclink = f"http://www.zerobyw4090.com/{ma.select_one('div.muludiv a')['href'].split('./')[1]}"
    req2 = requests.get(comiclink,headers=head)
    mb = BeautifulSoup(req2.text, "html.parser")
    finallink = mb.select('img#img_0')[0].get('src').split("manhua/")[1]

    default_download(chapter,finallink,comicname)

            
if __name__ == "__main__":

    # 網址,總章節數
    download_settings("#",47)

    # 網址,章節數,jpg命名格式(1=1 , 2=01 , 3=001)
    #custom_download("#",602,2)