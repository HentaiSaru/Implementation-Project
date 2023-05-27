import concurrent.futures
from lxml import etree
import threading
import requests
import opencc
import re
import os

""" Versions 1.0.1 (Vip可下載)

* 重構版 Zero漫畫下載器
[+] 漫畫自動處理下載
[+] 下載重新處理
[+] 多線程加速(沒感覺)

* 重構移除功能
[-] 自訂下載

! 可免費下載Vip觀看漫畫的版本 , 在漫畫網址處理的部份 , 都是模糊處理的
! 也就是不是去精準獲取所有的連結 , 故此有時候會出現下載失敗 , 但是網頁是有辦法看到的狀況
! 這就是網址請求錯誤而已 , 後續開發自訂下載 , 用來處理這部份問題

"""

# 下載位置
dir = os.path.abspath("R:/")

# 域名(該網站會每過一段時間改域名)
def DomainName():
    return "http://www.zerobyw3.com/"

class DataProcessing:
    def __init__(self):
        # 判斷網址格式
        self.UrlFormat = fr"{DomainName()}plugin\.php\?id=(.*)"
        # 名稱格式
        self.Name = r"^(.*?)【"
        # 只保留數字
        self.Filter = re.compile(r'\d+')
        # 簡體轉繁體
        self.converter = opencc.OpenCC('s2twp.json')
        # 請求設置
        self.Data_status = None
        self.session = requests.Session()
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
        # 數據保存
        self.folder_name = None
        self.Manga_name = None
        self.Comics_number = []
        self.Home_page_link = []
        self.Retry_on_failure = {}
        # 第一頁的漫畫格式
        self.Comic_link_format = None

    # 數據處理
    def DealWith(self,url):
        
        if re.match(self.UrlFormat,url):
            request = self.session.get(url, headers=self.headers)
            tree = etree.fromstring(request.content, etree.HTMLParser())

            # 漫畫名稱處理
            name = re.match(self.Name, tree.xpath("//h3[@class='uk-heading-line mt10 m10']/text()")[0])
            # 簡體轉繁體
            self.Manga_name = self.converter.convert(name.group(1))

            # 獲取漫畫話數 , 漫畫連結
            for link in tree.xpath("//a[@class='uk-button uk-button-default']"):
                self.Comics_number.append("".join(re.findall(self.Filter,link.xpath("./text()")[0])))
                self.Home_page_link.append(f"{DomainName()}/{link.get('href').split('./')[1]}")

            # 請求內頁
            request = self.session.get(self.Home_page_link[0], headers=self.headers)
            tree = etree.fromstring(request.content, etree.HTMLParser())

            try:
                # 獲取初始格式
                self.Comic_link_format = tree.xpath("//img[@id='img_0']")[0].get("src")
            except:
                print("第一話需要VIP的無法處理")
                
        else:print("不符合的網址格式")

    # 自動下載方法
    def Automatic(self,url):

        # 呼叫處理
        self.DealWith(url)

        # 域名格式
        domain = DomainName().replace("www","tupa")

        # 連結位置
        link = self.Comic_link_format.split("/")
        location = f"{link[-4]}/{link[-3]}"

        # 漫畫尾數 , 副檔名
        Mantissa = link[-1].split(".")[0]
        FileExtension = link[-1].split(".")[1]

        # 以從主頁面獲取的頁數變換
        for number in self.Comics_number:

            # 初始頁數
            pages = 1
            # 資料夾名稱
            self.folder_name = os.path.join(dir,f"{self.Manga_name} - 第{number}話")
            
            def accelerate():
                print(f"開始下載 - 第{number}話")

                # 為了可下載需Vip權限的 , 因此使用模糊請求
                for i in range(1000):
                    # 頁數格式判斷
                    if len(Mantissa) == 3:
                        page = int(pages)+i
                        page = f"{page:03d}"
                    elif len(Mantissa) == 2:
                        page = int(pages)+i
                        page = f"{page:02d}"
                    elif len(Mantissa) == 1:
                        page = int(pages)+i
                        page = f"{page:01d}"

                    # 漫畫連結的格式
                    ComicLink = f"{domain}{location}/{number}/{page}.{FileExtension}"
                    # 保存位置
                    Save = os.path.join(self.folder_name,f"{page}.{FileExtension}")

                    # 下載請求(實際上並沒有多線程加速效果,不使用 join 會壞掉)
                    control = threading.Thread(target=self.download,args=(Save,ComicLink))
                    control.start()
                    control.join()

                    # 請求失敗直接退出
                    if self.Data_status != 200:
                        break
                    else:
                        print("#",end="")

                print("")

            # 這邊雖使用線程池 , 但個人感覺沒變快
            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                executor.submit(accelerate)

            # 線程池關閉
            executor.shutdown()

    # 自訂下載方法
    def Custom(self,url:str , comics=None, mantissa=3 , FE="png"):

        self.DealWith(url)
        domain = DomainName().replace("www","tupa")

        link = self.Comic_link_format.split("/")
        location = f"{link[-4]}/{link[-3]}"

        FileExtension = FE

        # 計算尾數
        def mantissa_calculation(pages,i):
            if mantissa == 3:
                page = int(pages)+i
                page = f"{page:03d}"
            elif mantissa == 2:
                page = int(pages)+i
                page = f"{page:02d}"
            elif mantissa == 1:
                page = int(pages)+i
                page = f"{page:01d}"
            return page
        
        # 操作下載
        def operate(number):
            pages = 1
            self.folder_name = os.path.join(dir,f"{self.Manga_name} - 第{number}話")

            def accelerate():
                print(f"開始下載 - 第{number}話")

                for i in range(1000):

                    page = mantissa_calculation(pages,i)
                    ComicLink = f"{domain}{location}/{number}/{page}.{FileExtension}"
                    Save = os.path.join(self.folder_name,f"{page}.{FileExtension}")

                    control = threading.Thread(target=self.download,args=(Save,ComicLink))
                    control.start()
                    control.join()

                    if self.Data_status != 200:
                        break
                    else:
                        print("#",end="")
                print("")

            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                executor.submit(accelerate)
            executor.shutdown()

        # 設置是list(多重設置)
        if isinstance(comics,list):
            for number in comics:
                operate(number)
        # 沒有設置(預設)
        elif comics == None:
            for number in self.Comics_number:
                operate(number)
        # 有設置了某參數
        else:
            operate(comics)

    # 資料夾創建
    def Ffolder(self,FolderName):
        try:os.mkdir(FolderName) 
        except:pass

    # 自動測試正確的格式
    def Automatic_Trial_And_Error(self):
        pass
    
    # 下載方法
    def download(self,save,link):
        # 請求後將狀態傳遞
        Data_status = self.session.get(link,headers=self.headers)
        self.Data_status = Data_status.status_code

        if self.Data_status == 200:
            # (請求成功)沒有資料夾時創建
            if os.path.exists(self.folder_name):
                with open(save,"wb") as f:
                    f.write(Data_status.content)
            else:
                self.Ffolder(self.folder_name)

if __name__ == "__main__":
    download = DataProcessing()

    download.Automatic("http://www.zerobyw3.com/plugin.php?id=jameson_manhua&c=index&a=bofang&kuid=13073")