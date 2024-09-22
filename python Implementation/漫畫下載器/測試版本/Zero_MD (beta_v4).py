import os
import re
import time

from multiprocessing import *
from concurrent.futures import *

import opencc
from Script import AutoCapture, Reques

"""

Todo: 自定下載功能
Todo: 全部下載完成後, 合併功能

"""

Config = {
    "DownloadPath": "R:/", # 路徑結尾必須為斜線
    "RequestDomain": "http://www.zerobywz.com/", # 域名修正: https://zerobyw.github.io/
}

#? 請求類的實例
request = Reques()

#? 獲取漫畫元數據
def GetMeta(Url: str):
    print("\n[獲取漫畫元數據]\n")

    #! 初始化變數
    StartTime = time.time()
    Twp = opencc.OpenCC("s2twp.json")
    Result = {"RequesState": False}

    Allow = fr"{Config['RequestDomain']}plugin\.php\?id=(.*)"
    if re.match(Allow, Url):
        try:
            #? 請求數據
            tree = request.http2_get(Url, "tree")

            #? 取得漫畫名稱
            name = re.match(r"^(.*?)【", tree.xpath("//h3[@class='uk-heading-line mt10 m10']/text()")[0])
            MangaName = Twp.convert(name.group(1))

            #? 取得漫畫連結 (預覽圖)
            ImgLink = tree.xpath("//div[@class='uk-width-medium']/img")[0].get('src')

            #? 取得漫畫章節編號
            MangaChapter = []
            for link in tree.xpath("//a[@class='uk-button uk-button-default']"):
                MangaChapter.append(re.sub(r'[^\d.-]', "", link.xpath("./text()")[0]))

            #? 合併結果數據 (圖片連結會進行拆分) ['圖片請求域名', '章節', '01.jpg']
            Result['RequesState'] = True
            Result.update({"MangaName": MangaName, "MangaChapter": MangaChapter, "ImgLink": ImgLink.rsplit("/", 2)})

            print("[獲取完成] 耗時 %.3f 秒\n" %((time.time() - StartTime)))
        except Exception as e:
            print(f"域名錯誤 , 或是伺服器問題! {e}")
    else:
        print("不符合的網址格式")

    #! 回傳結果
    return Result

#? 處理下載任務
class DownloadTask:
    def __init__(self):
        self.Merge = None # 下載完成是否合併
        self.Mantissa = None # 保存尾數
        self.Extension = None # 保存擴展名
        self.ImgDomain = None # 保存圖片請求域名

    #? 創建資料夾
    def create_folder(self, Name: str):
        try:os.mkdir(Name)
        except:pass

    #? 下載完成後合併
    def complete_merge(self):
        ...

    #? 下載任務
    def task_download(self, FolderName: str, SavePath: str, ImgLink: str):
        response = request.http2_get(ImgLink, "none")

        if response.status_code == 200:
            #! (請求成功) 當沒有資料夾時創建
            if not os.path.exists(FolderName): self.create_folder(FolderName)

            with open(SavePath, "wb") as f:
                f.write(response.content)

        return response.status_code

    #? 試錯處理
    def task_trial_error(self, Page: str, Url: str):
        for Mantissa in range(1, 6): # 試錯尾數最多 5 位數
            for Extension in ["jpg", "png", "jpeg", "webp", "gif", "avif"]: # 資源競爭問題, 該列表必須在函數內宣告
                test_link = f"{Url}/{Page.zfill(Mantissa)}.{Extension}"

                if request.http2_head(test_link) == 200:
                    #? 成功的改變預設的 , 尾數 / 擴展名
                    self.Mantissa = Mantissa
                    self.Extension = Extension
                    return test_link
        return None

    #? 任務處理
    def task_process(self, FolderName: str, Chapter: str, IsSpecial: bool):
        PageCount = 0 # 計算總共頁數

        if IsSpecial:
            print(f"第 {Chapter} 特別章節 - 開始下載", flush=True)
        else:
            print(f"第 {Chapter} 章節 - 開始下載", flush=True)

        with ThreadPoolExecutor(max_workers=500) as executor:

            #! 為了可下載需 Vip 權限的, 因此使用模糊請求
            for index in range(1, 1001):
                ImgLink = None
                Page = f"{index}".zfill(self.Mantissa) # 生成頁數 (生成錯誤不會報錯, 會直接結束程式)

                #? 生成下載連結
                if IsSpecial: #! 特別話 的網址類型可能變更
                    ImgLink = f"{self.ImgDomain}/{Chapter}sheng/{Page}.{self.Extension}"
                else:
                    ImgLink = f"{self.ImgDomain}/{Chapter}/{Page}.{self.Extension}"

                ImgSavePath = f"{FolderName}/{Page}.{self.Extension}" # 圖片的保存路徑 
                TaskStatus = executor.submit(self.task_download, FolderName, ImgSavePath, ImgLink).result()

                #! 自動試錯不提供選擇 (自動使用)
                if TaskStatus != 200:
                    TrialLink = self.task_trial_error(str(index), ImgLink.rsplit("/", 1)[0]) # 將尾部移除, 傳參給試錯組合
                    if TrialLink is not None:
                        self.task_download(FolderName, ImgSavePath, TrialLink)
                    else: #! 因為是模糊請求, 當試錯都失敗直接跳出迴圈 (所以根據試錯的邏輯, 可能會缺頁面)
                        break

                PageCount += 1

        print(f"第 {Chapter} 章節 [共 {PageCount} 頁] - 下載完成", flush=True)

#? 下載器入口點
class ZeroDownloader(DownloadTask):
    def __init__(self, Merge: bool = False):
        super()

        self.Merge = Merge
        self.Cache = None # 緩存章節數
        self.TaskDelay = 1 # 生成任務的延遲
        self.MaxTask = cpu_count() - 1 # 最大同時處理任務數量

    #? 自動生成下載任務
    def AutoCreateTask(self, Url: str):
        Meta = GetMeta(Url)

        #! 請求狀態為 True 才處理
        if Meta['RequesState']:
            MangaName = Meta['MangaName'] # 取的漫畫名稱
            MangaSavePath = rf"{Config['DownloadPath']}{MangaName}" # 生成漫畫保存路徑
            self.create_folder(MangaSavePath) # 直接創建資料夾

            self.ImgDomain = Meta['ImgLink'][0] # 取得圖片請求域名 (初始化賦予)
            End = Meta["ImgLink"][2].split(".") # 取得圖片對象, 進行分割

            self.Mantissa = len(End[0]) # 取得尾數 長度 (初始化賦予)
            self.Extension = End[1] # 取得擴展名 (初始化賦予)

            #? 處理漫畫頁數, 生成下載任務
            with ProcessPoolExecutor(max_workers=self.MaxTask) as executor:
                for Chapter in Meta['MangaChapter']:
                    IsSpecial = False # 判斷是否為特別章節 (標記)
                    FolderName = "" # 內部漫畫資料夾名稱

                    if Chapter == self.Cache: # 判斷是否為特別章節
                        IsSpecial = True
                        FolderName = f"{MangaSavePath}/{MangaName} - 第 {Chapter} 特別章節"
                    else:
                        FolderName = f"{MangaSavePath}/{MangaName} - 第 {Chapter} 章節"

                    self.Cache = Chapter

                    if IsSpecial:
                        print(f"第 {Chapter} 特別章節 - 準備下載", flush=True)
                    else:
                        print(f"第 {Chapter} 章節 - 準備下載", flush=True)

                    executor.submit(self.task_process, FolderName, Chapter, IsSpecial)
                    time.sleep(self.TaskDelay)

if __name__ == "__main__":
    Download = ZeroDownloader()

    """
        ~ 自動創建任務 ~
    
        ? 使用方法:
        ! 添加符合規則的網址即可 (http://Zero網域/plugin.php?...&kuid=...)

        * 自動擷取網址後創建任務
        * 將擷取網址註解, 手動添加網址後創建任務
    """
    AutoCapture.settings(Config['RequestDomain'])
    CaptureLink = AutoCapture.GetLink()
    Download.AutoCreateTask(CaptureLink)
    
    """
        ~ 自定創建任務 ~

        ! 參數只有 url 是必填, 其餘可選擇

        * 連結 url - 輸入符合規則的網址 (字串)
        * 章節 chapter - 填寫要下載的章節, 第幾話 (數字 or 字串)
        * 尾數 mantissa - 填 3 = 001 , 2 = 01 ... (數字)
        * 副檔名 exten - 設置副檔名 , 正確的連結格式 , 就可以請求成功
        * 特別章節 special - 開啟後可以下載特別章節 (全彩中文/全彩生肉/無修正/...) 這類的特別章節
    """