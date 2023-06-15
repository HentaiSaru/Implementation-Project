import concurrent.futures
from lxml import etree
import threading
import requests
import opencc
import re
import os

""" Versions 1.0.3 (穩定版)

    Todo - Zero 漫畫下載器

        * - 當前功能 :
        ?   [+] 自訂下載
        ?   [+] 特別章節下載
        ?   [+] 下載位置選擇
        ?   [+] 網址連結自動試錯
        ?   [+] 漫畫自動處理下載
        ?   [+] 多線程加速(沒感覺)

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Todo - 相關說明 (詳細使用說明於代碼最下方)

        * Vip漫畫下載

        ! 可免費下載Vip觀看漫畫的版本 , 因此在漫畫網址處理的部份 , 都是模糊處理的
        ! 也就是不是去精準獲取所有的連結 , 故此有時候會出現下載失敗 , 但是網頁是有辦法看到的狀況
        ! 這就是網址請求錯誤而已 , 使用自訂下載 , 來處理這部份問題
        ! 但如果Vip章節 , 他的請求網址 , 與第一話不同 , 和第一話就需要Vip權限 , 這兩種的是直接下載不了

        * 下載速度

        ! 該網域本身速度就很慢
        ! 下載速度的影響(硬碟讀寫速度/網路速度/網站響應速度)
        ! 直接無堵塞多線程當然會很快 , 但數據會出錯 , 該程式採取的是有堵塞的線程
        ! 異步請求好像也會數據出錯 , 沒有很完整的測試

"""

# 下載位置
dir = os.path.abspath("R:/")

# 域名(該網站會每過一段時間改域名,在此處更改即可繼續使用)
def DomainName():
    return "http://www.zerobyw3.com/"

class DataProcessing:
    def __init__(self):
        # 判斷網址格式
        self.UrlFormat = fr"{DomainName()}plugin\.php\?id=(.*)"
        # 名稱格式
        self.Name = r"^(.*?)【"
        # 只保留數字
        self.Filter = re.compile(r'[\d-]+')
        # 簡體轉繁體
        self.converter = opencc.OpenCC('s2twp.json')
        # 請求設置
        self.Data_status = None
        self.session = requests.Session()
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
        # 數據保存
        self.cache = None
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
    def Automatic(self, url:str, trial=False):

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
            # 特別章節
            special = False

            # 判斷特別章節
            if number == self.cache:
                self.folder_name = os.path.join(dir,f"{self.Manga_name} - 第{number}特別話")
                special = True
            else:
                # 資料夾名稱
                self.folder_name = os.path.join(dir,f"{self.Manga_name} - 第{number}話")

            self.cache = number
            
            def accelerate():
                if special:
                    print(f"開始下載 - 第{number}特別話")
                else:
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

                    if special:
                        # 特別漫畫連結的格式
                        ComicLink = f"{domain}{location}/{number}sheng/{page}.{FileExtension}"
                    else:
                        # 一般漫畫連結的格式
                        ComicLink = f"{domain}{location}/{number}/{page}.{FileExtension}" 
                    
                    # 保存位置
                    Save = os.path.join(self.folder_name,f"{page}.{FileExtension}")

                    # 下載請求(實際上並沒有多線程加速效果,不使用 join 會壞掉)
                    control = threading.Thread(target=self.download,args=(Save,ComicLink))
                    control.start()
                    control.join()

                    # 請求失敗
                    if self.Data_status != 200:
                        if trial:
                            Try = self.Automatic_Trial_And_Error(ComicLink)
                            if Try != None:
                                control = threading.Thread(target=self.download,args=(Save,Try))
                                control.start()
                                control.join()
                                print("#",end="")
                            else:
                                break
                        else:
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
    def Custom(self,url:str , chapter=None, mantissa=3, FE="png", trial=False, special=False):

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
        def operate(number,special):
            pages = 1

            if special:
                self.folder_name = os.path.join(dir,f"{self.Manga_name} - 第{number}特別話")
                special = True
            else:
                self.folder_name = os.path.join(dir,f"{self.Manga_name} - 第{number}話")

            def accelerate():
                if special:
                    print(f"開始下載 - 第{number}特別話")
                else:
                    print(f"開始下載 - 第{number}話")

                for i in range(1000):

                    page = mantissa_calculation(pages,i)

                    if special:
                        ComicLink = f"{domain}{location}/{number}sheng/{page}.{FileExtension}"
                    else:
                        ComicLink = f"{domain}{location}/{number}/{page}.{FileExtension}"

                    Save = os.path.join(self.folder_name,f"{page}.{FileExtension}")

                    control = threading.Thread(target=self.download,args=(Save,ComicLink))
                    control.start()
                    control.join()

                    if self.Data_status != 200:
                        if trial:
                            Try = self.Automatic_Trial_And_Error(ComicLink)
                            if Try != None:
                                control = threading.Thread(target=self.download,args=(Save,Try))
                                control.start()
                                control.join()
                                print("#",end="")
                            else:
                                break
                        else:
                            break
                    else:
                        print("#",end="")

                print("")

            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                executor.submit(accelerate)
            executor.shutdown()

        # 設置是list(多重設置)
        if isinstance(chapter,list):
            for number in chapter:
                operate(number,special)
        # 沒有設置(預設)
        elif chapter == None:
            for number in self.Comics_number:
                operate(number,special)
        # 有設置某參數
        else:
            operate(chapter,special)

    # 資料夾創建
    def Ffolder(self,FolderName):
        try:os.mkdir(FolderName) 
        except:pass

    # 自動測試正確的格式
    def Automatic_Trial_And_Error(self,url):
        initial = url.rsplit("/",1)
        # 取得url的尾數
        page = int(initial[1].split(".")[0])
        # 排除重複
        mantissa_combination = list(set([f"{page:01d}",f"{page:02d}",f"{page:03d}",f"{page:04d}"]))
        file_extension_combination = ["jpg","png"]

        for i in range(len(mantissa_combination)):
            for j in range(len(file_extension_combination)):
                test = f"{mantissa_combination[i]}.{file_extension_combination[j]}"
                test_link = f"{initial[0]}/{test}"

                Data_status = self.session.get(test_link,headers=self.headers)

                if Data_status.status_code == 200:
                    return test_link
    
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

# 快速設置範圍
def custom_range(start,end):
    for chapter in range(start,end+1):
        CB.append(chapter)

if __name__ == "__main__":
    download = DataProcessing()
    CB = []

#################################################################################

    """ 自動下載說明

        ? 可用參數 : (連結:str(url) , 自動試錯:(True/False))
        ! 只要填入漫畫連結 , 自動下載所有的漫畫 , 當無法下載 , 基本上就是網址格式錯誤
        ! 可使用自訂下載 , 來一個一個測試 , 直到找到正確得請求網址

        * url - 填寫連結字串
        * 自動試錯 - 預設是 False (啟用後當有很多格式錯誤的,會跑比較久)
    """
    # download.Automatic("#",True)

#################################################################################

    """ 自訂下載說明

        ? 可用參數 : (連結:str(url) , 漫畫章節:(int/list) , 尾數字數:(int) , 副檔名:str(png/jpg) , 自動試錯:(True/False) , 特別章節:(True/False)
        ! 參數只有 url 是必填 , 其餘可填可不填(都自訂還是填一下)

        * 連結 url - 填寫連結字串
        * 章節 chapter - 填寫要下載的漫畫,第幾話 , 可使用上方CB來大量填寫 , 也可使用custom_range , 設置範圍
        * 尾數 mantissa - 填 3 = 001 , 2 = 01 ... , 這是根據該網站的命名去測試到正確的格式
        * 副檔名 FE - 就設置副檔名 , 以符合正確的連結格式 , 就可以請求成功
        * 自動試錯 trial - 如果很懶得填寫 , 章節 尾數 副檔名 , 去測試到正確的Url , 可以嘗試使用
        * 特別章節 special - 開啟後可以下載特別章節 (全彩中文/全彩生肉/無修正/...) 這類的特別章節
    """

    # 可使用自訂範圍 , 或是直接填入CB , 設置完成 , 直接再 Custom 尾數傳入 CB
    custom_range(1,10)

    # download.Custom("#",601,trial=True,special=True)