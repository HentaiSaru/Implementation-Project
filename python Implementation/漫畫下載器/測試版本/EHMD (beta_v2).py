from Script import AutoCapture, Reques, Get
from collections import OrderedDict
from concurrent.futures import *
from multiprocessing import *
import multiprocessing
from tqdm import tqdm
import aiohttp
import asyncio
import math
import time
import json
import re
import os

""" Versions 1.0.2 (測試版) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Todo - EHentai/ExHentai 漫畫下載

        * 功能概述 :
        ? 可下載 EHentai 和 ExHentai , 下載 Ex 需要設置 cookie
        ? cookie 有代碼中設置 Set() 和 json 讀取 Read()
        ? 目前只支援漫畫頁面的下載 , 搜尋頁面的不支援 , 後續會再添加

        * 開發環境 :
        ? Python 版本 3.12.2 - 64 位元
        ? 模塊下載 Python包安裝.bat 運行
        ? 依賴下載 Script 資料夾內所有腳本

        * 測試項目 :
        ? 原圖下載
        ? 下載穩定性
        ? 請求處理穩定性

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Todo - 使用說明

        * 可設置的功能都於 download_settings() 方法中設置

        * set 和 read 類 使用說明 , 看該類的註解

        * 請求的延遲別設置太短 , 有 IP 被 Ban 的可能性
        * 但有時請求失敗 , 可能是伺服器 , 或是 Cookie 的問題
        * 下載原圖時盡量不要多本同時載 , 容易下載不完全 (目前試錯只有 10 次)

        * 關於排除 Tag 的字典 , 設置時的 Key 值隨便打 , value 需包含在 list 內
        * 只要該漫畫有相關標籤 , 就會被排除掉

        * 傳入網址於 download_request() or 測試通道 , 即可開始請求下載
"""

#Todo [手動獲取Cookie, 並保存Josn文件]
def cookie_get():
    return Get.MGCookie("https://e-hentai.org/", rf"{os.getcwd()}\Cookie\EHCookies")

class Set:
    """
    Set 類別 (手動設置)
    * [使用方式]
    * 在需要使用該數據的部份呼叫 Set()
    * 然後輸入 "cookie" 或 "filter" -> Set("cookie")
    * 就可以取得設置的字典數據
    """
    def __init__(self):
        self.Cookies = { #Todo [ 只有請求 Ex 時需要設置 ]
            "igneous":"",
            "ipb_member_id":"",
            "ipb_pass_hash":""
        }
        self.TagExclude = { #Todo [手動設置排除標籤 , 並可於 download_settings() 套用回傳結果 , 設置詳情於 download_settings() 說明]
            "Tags": [""]
        }

    def __call__(self, Type: str):
        if Type.lower() == "cookie":
            return self.Cookies
        elif Type.lower() == "filter":
            return self.TagExclude
 
class Read:
    """
    Read 類別 (自動讀取Json)
    * [使用方式]
    * 在需要使用該數據的部份呼叫 Read()
    * 然後輸入 "cookie" 或 "filter" -> Read("cookie")
    * 就可以取得設置的字典數據
    * 如沒有該數據 , 就會進行創建
    """
    def __init__(self):
        self.Cookies_Path = "./Cookie/EHCookies.json"
        self.Exclude_Path = "./Exclude/EHFilter.json"
        self.Open_Path = None
        self.Create_Format = {}
        self.Create_Path = None

    def __call__(self, Type: str):
        if Type.lower() == "cookie":
            self.Open_Path = self.Cookies_Path
        elif Type.lower() == "filter":
            self.Open_Path = self.Exclude_Path
            
        try:
            with open(self.Open_Path , "r") as file:
                return json.loads(file.read())
            
        except: # Todo 當找不到出現錯誤時, 進行創建
            if Type.lower() == "cookie":
                self.Create_Format = {
                    "cf_clearance":"Please fill in the cookie"
                }
            elif Type.lower() == "filter":
                self.Create_Format = {
                    "Tags": ["Please enter Tag", "Please enter Tag"],
                }
                
            with open(self.Open_Path, "w") as file:
                file.write(json.dumps(self.Create_Format, indent=4, separators=(',',':')))

# 實例化
Set = Set()
Read = Read()

#Todo [數據請求回傳]
class DataRequest:
    # 這邊有些多此一舉, 但是可以讓調用代碼縮短
    Reques = None

    def get(self, link, result="tree") -> object:
        return self.Reques.get(link, result)

    def async_get(self, link, session) -> object:
        return self.Reques.async_get(link, session)

#Todo [下載連結驗證 分類]
class Validation(DataRequest):
    GetCookie = None # 判斷是否需要自動獲取
    Judgment_type = "https://e-hentai.org/" # 判斷輸入的網址類型, 用於驗證是否能請求
    E_HManga = r"https://e-hentai.org/g/\d+/[a-zA-Z0-9]+/"
    Ex_HManga = r"https://exhentai.org/g/\d+/[a-zA-Z0-9]+/"

    category = [] # 分類用
    save_box = [] # 下載連結

    # 驗證是否請求到網站數據
    def Request_Status(self) -> bool:

        try:
            tree = self.get(self.Judgment_type)
            tree.xpath("//div[@class='searchtext']/p/text()")
            return True
        except:
            if self.GetCookie:
                print(f"驗證錯誤請稍後...")
                if cookie_get():
                    print("\n獲取成功!\n")
                    self.Cookies = Read("cookie")
                    return True
                else:
                    print("\n獲取失敗!\n")
                    return False
            else:
                return False

    # 網址進行分類
    def URL_Classification(self, link) -> bool:
        try:
            # 判斷類型
            if isinstance(link, str):
                self.category.append(link)
            elif isinstance(link, list):
                self.category = link
            else:
                raise ValueError()

            # 判斷網址格式
            for url in self.category:
                if re.match(self.E_HManga, url):
                    self.save_box.append(url)
                elif re.match(self.Ex_HManga, url):
                    self.save_box.append(url)
                    self.Judgment_type = "https://exhentai.org/"
                else:
                    print(f"不支援的網址格式 : {url}")

            if len(self.save_box) > 0: # 驗證請求狀態
                if self.Request_Status():
                    return self.save_box
                else:
                    raise TypeError()

        except TypeError:
            print("請確認, [網路|Cookie|使用的請求瀏覽器], 等是否正常")
            os._exit(1)
        except ValueError as e:
            print(f"錯誤的輸入格式\n錯誤碼 : {e}")
            os._exit(1)

#Todo [下載器主程式]
class EHentaidownloader(Validation):
    def __init__(self):
        self.illegal_filename = r'[<>:"/\\|?*]'
        self.SetUse = False # 判斷是否改變設置
        # Todo [ 下載參數設置 ]
        self.path = None
        self.MaxProcess = None
        self.OriginalType = None
        self.ProcessDelay = None
        self.TagFilterBox = None
        self.SpecifyRange = None
        self.ProtectionDelay = None
        # Todo [ 保存數據參數 ]
        self.title = None
        self.test_counter = 0
        self.save_location = None
        self.Download_link = {}

    #? 下載設定 
    def download_settings(
        self,
        Browser: str="Google",
        GetCookie: bool=False,
        DownloadDelay =0.3,
        ProcessCreationDelay =1,
        OriginalImage: bool=True,
        DownloadPath: str=os.getcwd(),
        CookieSource: dict=Set("cookie"),
        MaxConcurrentDownload: int=cpu_count(),
        Scope: str=None,
        FilterTags: dict=None,
    ):
        """
        >>> [ Browser (預設: "Google") ]
        * 設置請求時模擬的瀏覽器
        * 目前只有 Google / Edge
        
        >>> [ GetCookie (預設: False) ]
        * 啟用後當請求失敗時, 會開啟網頁登入窗口,
        * 登入後按下確認, 自動獲取 Cookie 保存成 Json
        
        >>> [ DownloadDelay (預設: 0.3s) ]
        * 下載圖片時的延遲, 避免請求過快, 保護伺服器 和 避免被 Ban IP
        
        >>> [ ProcessCreationDelay (預設: 1s) ]
        * 開始處理數據時創建進程的延遲
        
        >>> [ OriginalImage (預設: True) ]
        * 選擇是否下載原圖, False 就是下載重新採樣圖
        * 當選擇下載原圖時, DownloadDelay 調整最快設置為 2 秒
        
        >>> [ DownloadPath (預設: 當前代碼路徑) ]
        * 圖片下載位置

        >>> [ CookieSource (預設: Set("cookie")) ]
        * 設置 Cookie 的來源, 預設是讀取手動設置, 可改成讀取 Json
        * 改成 Read("cookie") 即可
        
        >>> [ MaxConcurrentDownload (預設: 自身 cpu 核心數) ]
        * 最大併發進程數量
        
        >>> [ Scope (預設: None) ]
        * 指定下載的範圍
        * 格式: "1, 2, 3, 4-6, 7~10, !8"

        >>> [ FilterTags (預設: None) ]
        * 輸入字典格式 {"key":["排除Tag","排除Tag","排除Tag"]}
        * 手動設置 -> Set("filter")
        * 讀取 Json -> Read("filter")
        """
        self.SetUse = True # 當首次被呼叫時, 設置已使用
        self.path = DownloadPath
        self.SpecifyRange = Scope
        self.GetCookie = GetCookie
        self.TagFilterBox = FilterTags
        self.OriginalType = OriginalImage
        self.MaxProcess = MaxConcurrentDownload
        self.ProcessDelay = ProcessCreationDelay
        self.Reques = Reques(Browser.lower().capitalize(), CookieSource) # 初始化請求
        self.ProtectionDelay = max(2, DownloadDelay) if OriginalImage else DownloadDelay # 下載延遲計算

    #? (正式通道) 下載請求
    def download_request(self, link):
        # 檢查是否設置過
        if not self.SetUse:
            self.download_settings()
        self.Process_Trigger(self.URL_Classification(link))

    #? (測試通道) 下載請求 [無驗證] 
    def download_request_test(self, link):
        if not self.SetUse:
            self.download_settings()
        self.test_counter += 1
        multiprocessing.Process(target=self.Comic_Process, args=(link, self.test_counter)).start()

    #? 數據處理觸發
    def Process_Trigger(self, box):
        if box != None:
            if len(box) == 1:
                self.Comic_Process(box[0], 1)
            else:
                with ProcessPoolExecutor(max_workers=self.MaxProcess) as executor:
                    for index, url in enumerate(box):
                        executor.submit(self.Comic_Process, url, index+1)
                        time.sleep(self.ProcessDelay)
    
    #? 計算需下載的範圍
    def ScopeParsing(self, scope: str, box: dict) -> dict:
        """
        scope : -> 指定下載的範圍
        box : -> 下載的數據
        """
        if isinstance(scope, str) and isinstance(box, dict):
            all_keys = list(box.keys())
            result = set(); exclude = set();
            for s in re.split(r'\s*,\s*', scope):
                if s.isdigit():
                    result.add(int(s)-1)
                elif re.match(r"^\d+(?:~\d+|-\d+)$", s):
                    Range = list(map(int, re.split(r"\D+", s)))
                    result.update([i-1 for i in range(Range[0], Range[1]+1)])
                elif re.match(r"!+\d+", s):
                    exclude.add(int(s.replace("!", ""))-1)

            result -= exclude
            valid_keys = [all_keys[index] for index in result if 0 <= index < len(all_keys)]
            return {key: box[key] for key in valid_keys}
        else:
            raise ValueError("錯誤的輸入類型")

    #? 處理漫畫數據           
    def Comic_Process(self, url, count):
        url = url.split("?p=")[0] # 獲取第一頁數據
        StartTime = time.time()
        print(f"[漫畫 {count} 開始處理] => {url}", flush=True)

        #! 保存主頁跳轉連結
        home_page_link = []
        def home_page(tree):
            for link in tree.xpath("//div[@id='gdt']/div/a"):
                href = link.get("href")
                if href != None:
                    home_page_link.append(href)


        image_link = OrderedDict()
        ResampleImage = "//img[@id='img']"
        OriginalImage = "//div[@id='i6']/div[3]/a"
        #? 根據 OriginalType 的選擇動跳調整, 索引順序
        DownloadType = {True: [OriginalImage, ResampleImage], False: [ResampleImage, OriginalImage]}[self.OriginalType]
        #! 保存圖片連結
        """
        ? 此寫法雖然較為簡潔, 但是對於大量數據處理時, 性能不太好
        def picture_link(tree):
            for link in tree.xpath(DownloadType[0]) or tree.xpath(DownloadType[1]):
                href = link.get("href") or link.get("src")
                image_link[href] = None
        """
        #! 需要優化
        def picture_link(tree):
            xp = tree.xpath(DownloadType[0])
            if not xp:
                xp = tree.xpath(DownloadType[1])
            else:
                for data in xp:
                    link = data.get("src")
                    if not link:
                        link = data.get("href")
                    if not link.endswith("509.gif"):
                        image_link[link] = None

        tree = self.get(url) # 請求第一頁連結
        home_page(tree)

        # 獲取漫畫總頁數
        total_pages = math.ceil(int(tree.xpath("//td[@class='gdt2']/text()")[-2].split(" ")[0]) / 20)

        try: # 取得漫畫標題, 排除非法字元
            title = tree.xpath("//*[@id='gj']/text()")
            title = title[0] if title else tree.xpath("//*[@id='gn']/text()")[0]
            self.title = re.sub(self.illegal_filename, "", title).strip()
        except:
            print("""
        [無法取得標題元素!]

        可能原因:
            [1]需要特別的Cookie
            [2]該頁面元素位置有例外
            [3]你的IP被Ban了
            """)
            return

        # 取得保存路徑
        self.save_location = os.path.join(self.path, self.title)

        #! 有設置排除 Tag 時, 會進行排除
        if self.TagFilterBox != None:
            # 取得所有 Tag
            label_box = tree.xpath("//td/div/a/text()")
            for value in self.TagFilterBox.values():
                result = set(value) & set(label_box)
                if result:
                    print(f"[漫畫 {count} 排除]", flush=True)
                    return

        #! 核心獲取圖片連結邏輯
        async def Trigger():
            count = 0 # 計數器
            work = work1 = []
            async with aiohttp.ClientSession() as session:
                if total_pages > 1:
                    for page in range(1, total_pages):
                        work.append(asyncio.create_task(self.async_get(f"{url}?p={page}", session)))

                        count+=1
                        if count == 5: #* 每處理5頁, 暫停1秒
                            print(f"\r以處理 [{page}] 頁", end="", flush=True)
                            await asyncio.sleep(1)
                            count = 0
                    results = await asyncio.gather(*work)

                    # 處理獲取跳轉連結
                    for tree in results:
                        home_page(tree)

                    # 計算跳轉連結
                    Processed_pages = len(home_page_link)
                    if (Processed_pages <= 0):
                        os.system("cls")
                        print("數據處理錯誤")
                        os._exit(1)

                for link in home_page_link:
                    work1.append(self.async_get(link, session))

                    count+=1
                    if count == 100: #* 每處理100張, 暫停1秒
                        Processed_pages -= count
                        print(f"\r剩餘處理 [{Processed_pages}] 張", end="", flush=True)
                        await asyncio.sleep(1)
                        count = 0
                results = await asyncio.gather(*work1)

                for tree in results:
                    picture_link(tree)

        #! 觸發異步請求處理
        asyncio.run(Trigger())

        # 將下載數據轉換成 list
        data = list(image_link.keys())
        if len(data) < 1:
            print("連結獲取失敗")
            return

        # 計算漫畫名擴充值
        filling = f"%0{max(2, int(math.log10(len(data))) + 1)}d"
        # 生成下載數據
        for page, link in enumerate(data):
            self.Download_link[f"{filling % (page+1)}"] = link

        if self.SpecifyRange:
            self.Download_link = self.ScopeParsing(self.SpecifyRange, self.Download_link)

        print("\r[漫畫 %d 處理完成] => 處理耗時 %.3f 秒" % (count, (time.time() - StartTime)), flush=True)
        self.create_folder(self.save_location) # 創建資料夾
        self.download_processing() # 進行下載處理

    #? 創建下載資料夾
    def create_folder(self,Name):
        try:os.mkdir(Name)
        except:pass

    #? 圖片下載線程處理
    def download_processing(self):
        with ThreadPoolExecutor(max_workers=100) as executor:
            for SaveName, Link in tqdm(self.Download_link.items(), desc=self.title, colour="#DB005B"):

                save_location = os.path.join(self.save_location, f"{SaveName}.{Link.rsplit('.', 1)[1]}")
                executor.submit(self.download_pictures, save_location, Link)
                time.sleep(self.ProtectionDelay)

    #? 圖片下載 (等待修正)
    def download_pictures(self, download_path, download_link, Retries=10):
        while Retries > 0:
            ImageData = self.get(download_link, "none")
            
            if "do not have sufficient GP to buy a download quota" in ImageData.text:
                print("\n原圖下載超額, 請變更 IP 位置")
                os._exit(1)

            elif ImageData.status_code == 200:
                with open(download_path, "wb") as file:
                    file.write(ImageData.content)
                break

            else:
                # 簡單的試錯 (等待 5 秒重新循環), 有空在寫 Queue 處理
                time.sleep(5)
                Retries -= 1

if __name__ == "__main__":
    eh = EHentaidownloader()

    # 進行下載設置
    eh.download_settings(
        DownloadPath = "R:/",
        CookieSource = Read("cookie"),
    )

    AutoCapture.settings("https://(exhentai|e-hentai)")

    # 獲取擷取列表, 一次回傳一個列表, 自動停止擷取
    # capture = AutoCapture.GetList()
    # if capture != None:
        # eh.download_request(capture)
    # else:
        # print("無擷取內容")
        # os._exit(0)

    for capture in AutoCapture.Unlimited():
        eh.download_request_test(capture)