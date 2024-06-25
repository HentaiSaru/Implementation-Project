from Script import AutoCapture, Reques, Get
from concurrent.futures import *
from multiprocessing import *
from lxml import etree
import opencc
import time
import re
import os

""" Versions 1.0.8 (垃圾版/等待重構)

    Todo - Zero 漫畫下載器
    
        * 功能概述 :
        ? 目前雖代碼寫的超爛, 但功能都還正常可以使用
        ? 可根據域名的變動修改 DomainName() 的參數
        ? 提供自動擷取下載, 與自訂頁數下載函數
        ? 可自訂下載位置, 與下載相關參數設置
        ? 多進程 和 多線程 加速下載處理
        ? 需 VIP 漫畫可直接下載

        * 開發環境 :
        ? Python 版本 3.11.7 - 64 位元
        ? 模塊下載 Python 包安裝.bat 運行
        ? 依賴下載 Script 資料夾內所有腳本

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Todo - 相關說明 (詳細使用說明於代碼最下方)

        * Vip漫畫下載

        ! 可免費下載Vip觀看漫畫的版本 , 因此在漫畫網址處理的部份 , 都是模糊處理的
        ! 也就是不是去精準獲取所有的連結 , 故此有時候會出現下載失敗 , 但是網頁是有辦法看到的狀況
        ! 這就是網址請求錯誤而已 , 使用自訂下載 , 來處理這部份問題

        * 下載速度

        ! 測試版的下載速度較快
        ! 但該網域本身速度就很慢
        ! 下載速度的影響(硬碟讀寫速度/網路速度/網站響應速度/返回驗證處理)

        * 下載進度

        ! 測試版沒有下載進度顯示
        ! 下載完成會顯示完成
        ! 程式停住就是在下載中不是卡住
        ! 全部下載完成程式會自動終止

"""

# 下載位置設置
dir = os.path.abspath("R:/")

# (該網站會每過一段時間會改域名 , 在此處更改即可繼續使用)
def DomainName():
    return "https://www.zerobywzz.com/"

class ZeroDownloader:
    def __init__(self):
        """ #_#_#_#_#_#_#_#_#_#_#_#_#_#_#
        Todo ----------------------------
            *  { 進程處理 }
            ?  [ ProcessDelay ] 創建進程 的 延遲秒數
            ?  [ MaxProcesses ] 同時可運行的最大進程數
        Todo ----------------------------
        """
        self.ProcessDelay = 1
        self.MaxProcesses = cpu_count() - 1 # cpu 核心數

        """ #_#_#_#_#_#_#_#_#_#_#_#_#_#_#
        Todo ----------------------------
            *  { 過濾格式 }
            ?  [ Filter ] 將字串中數字以外的過濾
            ?  [ NameFormat ] 漫畫的名稱格式變
            ?  [ UrlFormat ] 篩選正確的該網站網址格式
        Todo ----------------------------
        """
        self.Filter = r'[^\d.-]'
        self.NameFormat = r"^(.*?)【"
        self.UrlFormat = fr"{DomainName()}plugin\.php\?id=(.*)"

        """ #_#_#_#_#_#_#_#_#_#_#_#_#_#_#
        Todo ----------------------------
            *  { 狀態判斷 }
            ?  [ retry ] 判斷是否使用自動試錯
            ?  [ request_status ] 判斷是否請求成功
        Todo ----------------------------
        """
        self.retry = None
        self.request_status = False

        """ #_#_#_#_#_#_#_#_#_#_#_#_#_#_#
        Todo ----------------------------
            *  { 數據保存 }
            ?  [ Comics_number ] 保存漫畫章節數
            ?  [ Comics_link ] 保存漫畫連結
            ?  [ Comic_link_format ] 初始漫畫請求連結格式
            ?  [ Manga_name ] 漫畫的名子
            ?  [ cache ] 用於判斷重複章節
        Todo ----------------------------
        """
        self.Comics_number = []
        self.Comics_link = []
        self.Comic_link_format = None
        self.Manga_name = None
        self.cache = None

        """ #_#_#_#_#_#_#_#_#_#_#_#_#_#_#
        Todo ----------------------------
            *  { 請求連結的構成要素 }
            ?  [ reques ] 用於請求數據 ( API 調用)
            ?  [ FileExtension ] 請求網址的圖片副檔名
            ?  [ location ] 請求網址的位置
            ?  [ Mantissa ] 請求網址的尾數
            ?  [ domain ] 請求網址的網域
        Todo ----------------------------
        """
        self.reques = Reques("Google")
        self.FileExtension = None
        self.location = None
        self.Mantissa = None
        self.domain = None

    def data_processing(self, url):

        print("\n[獲取漫畫數據]\n")
        StartTime = time.time()
        converter = opencc.OpenCC("s2twp.json")

        if re.match(self.UrlFormat,url):
            try:
                tree = self.reques.http2_get(url, "tree")

                # 漫畫名稱處理
                name = re.match(self.NameFormat , tree.xpath("//h3[@class='uk-heading-line mt10 m10']/text()")[0])
                self.Manga_name = converter.convert(name.group(1))

                # 獲取漫畫話數 and 漫畫連結
                for link in tree.xpath("//a[@class='uk-button uk-button-default']"):
                    self.Comics_number.append(re.sub(self.Filter, "", link.xpath("./text()")[0]))
                    self.Comics_link.append(f"{DomainName()}/{link.get('href').split('./')[1]}")

                self.Comic_link_format = tree.xpath("//div[@class='uk-width-medium']/img")[0].get('src')
                self.request_status = True # 判斷是否完全請求到數據

                print("[獲取完成] 耗時 %.3f 秒\n" %((time.time() - StartTime)))
                
            except Exception as e:
                print(f"域名錯誤 , 或是伺服器問題! {e}")

        else:print("不符合的網址格式")

    # 加速下載方法
    def accelerate(self, special, folder_name, number):
        # 初始頁數
        pages = 1
        count = 0

        if special:
            print(f"第 {number} 特別話 - 開始下載", flush=True)
        else:
            print(f"第 {number} 話 - 開始下載", flush=True)

        with ThreadPoolExecutor(max_workers=500) as executor:
            # 為了可下載需Vip權限的 , 因此使用模糊請求
            for i in range(1000):
                # 頁數格式判斷
                if len(self.Mantissa) == 3:
                    page = int(pages)+i
                    page = f"{page:03d}"
                elif len(self.Mantissa) == 2:
                    page = int(pages)+i
                    page = f"{page:02d}"
                elif len(self.Mantissa) == 1:
                    page = int(pages)+i
                    page = f"{page:01d}"

                if special:
                    # 特別漫畫連結的格式
                    ComicLink = f"{self.domain}{self.location}/{number}sheng/{page}.{self.FileExtension}"
                else:
                    # 一般漫畫連結的格式
                    ComicLink = f"{self.domain}{self.location}/{number}/{page}.{self.FileExtension}"

                # 保存位置格式
                Save = rf"{folder_name}\{page}.{self.FileExtension}"

                # 呼叫下載 , 並接收回傳 (雖然使用 result() 會降低效率 , 但因為不知道總頁數 , 不使用這樣就不好判斷結束)
                Data_status = executor.submit(self.download, folder_name, Save, ComicLink).result()

                if Data_status != 200:
                    if self.retry:
                        Try = self.Automatic_Trial_And_Error(ComicLink)
                        if Try != None:
                            self.download(folder_name, Save, Try)
                            count += 1
                        else:
                            break
                    else:
                        break

                count += 1

            print(f"第 {number} 話 [共 {count} 頁] - 下載完成", flush=True)

    # 自動下載方法
    def Automatic(self, url:str, retry=True):

        # 請求數據
        self.data_processing(url)
        self.retry = retry

        if self.request_status:
            Manga_name = self.Manga_name # 漫畫名稱
            self.Ffolder(rf"{dir}{Manga_name}") # 創建漫畫資料夾
            self.domain = DomainName().replace("www","tupa") # 圖片請求域名格式變更

            link = self.Comic_link_format.split("/") # 連結處理
            self.location = f"{link[-4]}/{link[-3]}" # 網址連結的位置

            end = link[-1].split(".") # 網址尾部處理
            self.Mantissa = end[0] # 連結尾數
            self.FileExtension = end[1] # 連結擴展名

            with ProcessPoolExecutor(max_workers=self.MaxProcesses) as executor:
                for number in self.Comics_number: # 漫畫話數
                    # 特別章節
                    special = False

                    # 判斷特別章節
                    if number == self.cache:
                        folder_name = rf"{dir}{Manga_name}\{Manga_name} - 第{number}特別話"
                        special = True
                    else:
                        # 資料夾名稱
                        folder_name = rf"{dir}{Manga_name}\{Manga_name} - 第{number}話"

                    # 只要與前一個有重複的數字 , 就是特別章節
                    self.cache = number

                    if special:
                        print(f"第 {number} 特別話 - 準備下載", flush=True)
                    else:
                        print(f"第 {number} 話 - 準備下載", flush=True)

                    executor.submit(self.accelerate, special, folder_name, number)
                    time.sleep(self.ProcessDelay)

    # 自訂下載方法
    def Custom(self,url:str, chapter=None, mantissa=3, FE="png", retry=True, special=False):

        # 尾數轉換字串
        def mantissa_conversion(mantissa):
            pages = 1
            if mantissa == 3:
                page = f"{pages:03d}"
            elif mantissa == 2:
                page = f"{pages:02d}"
            elif mantissa == 1:
                page = f"{pages:01d}"
            return page

        # 數據請求
        self.data_processing(url)
        self.retry = retry

        if self.request_status:

            """ ____________ 初始值設置 ____________ """

            Manga_name = self.Manga_name
            Comics_number = None

            self.domain = DomainName().replace("www", "tupa")

            link = self.Comic_link_format.split("/")
            self.location = f"{link[-4]}/{link[-3]}"

            self.Mantissa = mantissa_conversion(mantissa)
            self.FileExtension = FE

            """ ____________ 章節數設置 ____________ """

            # 設置是list(多重設置)
            if isinstance(chapter,list):
                Comics_number = chapter
            # 沒有設置(預設)
            elif chapter == None:
                Comics_number = self.Comics_number
            # 有設置某參數
            else:
                Comics_number = list(str(chapter))

            """ ____________ 開始請求下載 ____________ """

            with ProcessPoolExecutor(max_workers=self.MaxProcesses) as executor:
                for number in Comics_number:

                    if number == self.cache:
                        folder_name = rf"{dir}{Manga_name}\{Manga_name} - 第{number}特別話"
                        special = True
                    else:
                        folder_name = rf"{dir}{Manga_name}\{Manga_name} - 第{number}話"
                    self.cache = number

                    if special:
                        print(f"第 {number} 特別話 - 準備下載", flush=True)
                    else:
                        print(f"第 {number} 話 - 準備下載", flush=True)

                    executor.submit(self.accelerate, special, folder_name, number)
                    time.sleep(self.ProcessDelay)

    # 資料夾創建
    def Ffolder(self, FolderName):
        try:os.mkdir(FolderName) 
        except:pass

    # 自動測試正確的格式
    def Automatic_Trial_And_Error(self, url):

        # 將url從右側分割1次
        initial = url.rsplit("/", 1)
        # 取得url的尾數
        page = int(initial[1].split(".")[0])

        # 尾數格式
        mantissa_combination = [f"{page:01d}", f"{page:02d}", f"{page:03d}", f"{page:04d}", f"{page:05d}"]
        # 擴展格式
        extension_combination = ["jpg", "png", "gif", "jpeg"]

        for mantissa in mantissa_combination:
            for extension in extension_combination:
                # 測試的尾端格式
                test = f"{mantissa}.{extension}"
                # 合併的測試連結
                test_link = f"{initial[0]}/{test}"
                # 請求測試
                Data_status = self.reques.http2_get(test_link, "none")

                if Data_status.status_code == 200:
                    # 成功的改變預設的 , 尾數/擴展名
                    self.Mantissa = mantissa
                    self.FileExtension = extension
                    return test_link

    # 下載方法
    def download(self, folder_name, save_name, link):
        # 請求後將狀態傳遞
        Data = self.reques.http2_get(link, "none")

        if Data.status_code == 200:
            # (請求成功) 當沒有資料夾時創建
            if not os.path.exists(folder_name):
                self.Ffolder(folder_name)

            with open(save_name,"wb") as f:
                f.write(Data.content)

        return Data.status_code

#################################################################################

# 快速設置範圍
def custom_range(start,end):
    for chapter in range(start,end+1):
        CB.append(chapter)

if __name__ == "__main__":
    zero = ZeroDownloader()
    CB = []

#################################################################################

    """ 自動下載說明

        ? 可用參數 : (連結:str(url) , 自動試錯:(True/False))
        ! 只要填入漫畫連結 , 自動下載所有的漫畫 , 當無法下載 , 基本上就是網址格式錯誤
        ! 可使用自訂下載 , 來一個一個測試 , 直到找到正確得請求網址

        * url - 填寫連結字串
        * 自動試錯 - 預設是 False (啟用後當有很多格式錯誤的, 會跑比較久)
    """
    # 自動擷取URL
    AutoCapture.settings(DomainName())
    
    capture = AutoCapture.GetLink()
    zero.Automatic(capture)

#################################################################################

    """ 自訂下載說明

        ? 可用參數 : (連結:str(url) , 漫畫章節:(int/list) , 尾數字數:(int) , 副檔名:str(png/jpg) , 自動試錯:(True/False) , 特別章節:(True/False)
        ! 參數只有 url 是必填 , 其餘可填可不填(都自訂還是填一下)

        * 連結 url - 填寫連結字串
        * 章節 chapter - 填寫要下載的漫畫 , 第幾話(填寫數字或字串都可以) , 可使用上方CB來大量填寫 , 也可使用custom_range設置範圍
        * 尾數 mantissa - 填 3 = 001 , 2 = 01 ... , 這是根據該網站的命名去測試到正確的格式
        * 副檔名 FE - 就設置副檔名 , 以符合正確的連結格式 , 就可以請求成功
        * 自動試錯 retry - 如果很懶得填寫 , 章節 尾數 副檔名 , 去測試到正確的Url , 可以嘗試使用
        * 特別章節 special - 開啟後可以下載特別章節 (全彩中文/全彩生肉/無修正/...) 這類的特別章節
    """

    # 可使用自訂範圍 , 或是直接填入CB , 設置完成 , 直接再 Custom 尾數傳入 CB
    # custom_range(1,2)

    # zero.Custom("#" , chapter=1)