from concurrent.futures import *
from multiprocessing import *
from lxml import etree
from tqdm import tqdm
import requests
import time
import re
import os

# 下載路徑
dir = os.path.abspath("R:/")

# 網站域名
def DomainName():
    return "https://nhentai.net/"

#Todo [ 請再此處輸入你當前通過機器人驗證的 cookie (輸入錯誤會請求不到) ]
def cookie_set():
    cookie = {
        "cf_chl_2": "ca663eafa7822bc",
        "cf_clearance" : "U0sxcgebBnGyVYK6IejJbOeOeZBsgDRQHtO.lj9dN5I-1686927380-0-160",
        "csrftoken" : "RFUIyP21PFyLmRMf7tYAV1sCPhWG3CceBsRfs2fsmHDDqpSG7Sd2Coa1IfOhtM5V"
    }
    return cookie

class NHentaiDownloader:
    def __init__(self):
        self.session = requests.Session()
        self.Google_Headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
        self.Edge_Headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43"}
        self.headers = None

        self.search = r"https://nhentai\.net/.*"
        self.manga = r"https://nhentai\.net/g/\d+"

        self.ProtectionDelay = 0.2
        self.ProcessDelay = 1
        self.CpuCore = cpu_count()

        # 網址分類保存
        self.category_box = []

        # 漫畫標題
        self.title = None
        # 漫畫保存位置
        self.save_location = None
        # 漫畫Tag標籤
        self.labelbox = {}
        # 下載連結
        self.download_link = {}

    # 基本請求數據
    def get_data(self,url):
        request = self.session.get(url, headers=self.headers, cookies=cookie_set())
        return etree.fromstring(request.content , etree.HTMLParser())
    
    # google 請求
    def google(self,link):
        self.headers = self.Google_Headers
        self.URL_Classification(link)

    # edge 請求
    def edge(self,link):
        self.headers = self.Edge_Headers
        self.URL_Classification(link)

    # 網址分類方法 (待開發...)
    def URL_Classification(self,link):

        try:
            if isinstance(link,str):
                self.category_box.append(link)
            elif isinstance(link,list):
                self.category_box = link
            else:raise Exception()

            with ProcessPoolExecutor(max_workers=self.CpuCore) as executor:
                for url in self.category_box:
                    if re.match(self.manga,url):
                        executor.submit(self.comic_page_data , url)
                    elif re.match(self.search,url):
                        pass
                    else:
                        print(f"錯誤格式的連結{url}")

                    time.sleep(self.ProcessDelay)
        except:
            print("錯誤的輸入格式")
    
    # 漫畫頁數據處理
    def comic_page_data(self,url):

        print("開始請求漫畫數據")
        StartTime = time.time()
        tree = self.get_data(url)

        try:
            # 標題
            title = tree.xpath("//h2[@class='title']")[0]
            self.title = re.sub(r'[<>:"/\\|?*]', '', "".join(title.xpath(".//text()")).strip())
            self.save_location = os.path.join(dir,self.title)

            # 圖片的連結
            img = tree.xpath("//meta[@itemprop='image']")[0].get("content")
            domain_name = img.rsplit('/',1)[0].replace(img[8:10],f"i{img[9]}")
            suffix = img.rsplit('.',1)[1]

            # Tag標籤資訊
            label = tree.xpath("//section[@id='tags']")[0]
            for index , tag in enumerate(label.xpath(".//div")):
                if index == 4 or index == 6 or index == 8:continue # 這邊是排除不需要的數據
                else:self.labelbox[tag.text.strip().rstrip(':')] = tag.xpath(".//span[@class='name']/text()")

            # 生成請求連結
            for i in range(1 , int(self.labelbox['Pages'][0])+1):
                SaveName = f"{i:03d}.{suffix}"
                comic_link = f"{domain_name}/{i}.{suffix}"
                self.download_link[SaveName] = comic_link

            print("請求完成 耗時 : %.3f" % ((time.time() - StartTime)))
            self.download_processing()

            #! self.labelbox 大致格式
            # {'Parodies': [''], 'Characters': ['', ''], 'Tags': [''], 'Artists': [''], 'Languages': ['', ''], 'Pages': ['']}
        except:
            print("請更換Cookie , 或檢查使用的瀏覽器")

    # 下載處理
    def download_processing(self):
        self.create_folder(self.save_location)

        with ThreadPoolExecutor(max_workers=500) as executor:
            for SaveName , comic_link in tqdm(self.download_link.items() , desc=self.title, colour="#9575DE"):
                executor.submit(self.download,os.path.join(self.save_location,SaveName),comic_link)
                time.sleep(self.ProtectionDelay)

    # 資料夾創建
    def create_folder(self,Name):
        try:os.mkdir(Name)
        except:pass

    # 下載方法
    def download(self,download_path,download_link):
        ImageData = self.session.get(download_link, headers=self.headers, cookies=cookie_set())
        with open(download_path , "wb") as f:
            f.write(ImageData.content)

if __name__ == "__main__":
    nh = NHentaiDownloader()

    nh.google("")
    # nh.edge("")