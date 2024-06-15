import os
import shutil
import threading
import tkinter as tk
from tkinter import filedialog
from operator import itemgetter
from collections import Counter

import progressbar

""" Versions 1.0.0 - V2

    Todo - 精簡版檔案類型分類

        ? (開發/運行環境):
        * Windows 11 23H2
        * Python 3.12.3 64-bit

        * 第三方庫:
        * progressbar

        ? 功能說明:
        * 資料夾路徑選取
        * 多線程複製輸出
        * 檔案類型選擇
        * 輸出進度顯示
        * 完成自動開啟
        * 功能選項

        ? 使用說明:
        * 選擇需分類檔案的資料夾
        * 接著根據顯示的代號, 選擇要複製的檔案類型

        * 輸出的速度取決於硬碟讀寫速度
        * 輸出是採複製的方式 , 對原始檔案無影響
"""

class Read(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.Folder_Path = None
        self.Complete_Data = None

    def __Read_All_Files(self):
        # 保存選擇資料夾後讀取的所有數據
        Read_Data = {}

        for Root, _, Files in os.walk(self.Folder_Path): # 路徑 , 資料夾 , 檔名
            Read_Data[Root] = Files

        return Read_Data

    # 選擇開啟資料夾
    def __Open_Folder(self):
        self.withdraw() # 隱藏主窗口
        self.Folder_Path = filedialog.askdirectory(title="選擇資料夾")
        self.destroy() # 消除

        if self.Folder_Path is not None:
            return self.__Read_All_Files()

    # 解析開啟的路徑數據
    def Analysis(self):

        Data = self.__Open_Folder()

        if len(Data) <= 0:
            print("無選擇資料夾")
            os._exit(1)

        # 緩存處理擴展名
        File_Extension = None
        # 保存所有檔案類型 用於顯示選擇
        File_Type = set()
        # 保存所有檔案類型 用於計算數量
        Type_Quantity = []
        # 保存所有檔案數據
        Complete_Data = []

        for Path, FileBox in Data.items():
            if len(FileBox) != 0: # 當他是 0 帶表示空資料夾
                for name in FileBox:
                    try:
                        File_Extension = name.rsplit(".", 1)[1].strip()
                    except Exception: # 可能有例外
                        pass

                    try:
                        Lowercase = File_Extension.lower()

                        File_Type.add(Lowercase)
                        Type_Quantity.append(Lowercase)
                        Complete_Data.append(os.path.join(Path, name).replace("\\","/"))
                    except Exception:
                        print("無可分類檔案")
                        os._exit(1)

        self.Complete_Data = Complete_Data
        return File_Type, Type_Quantity

# 自訂例外
class DataEmptyError(Exception):
    pass

# 複製輸出
class Copy:
    def __init__(self):
        self.Save_Path = None
        self.Origin_Path = None
        self.Output_Data = None
        self.Output_Select = None
        self.__Copy_Output = lambda Copy_Path, Output_Path: shutil.copyfile(Copy_Path, Output_Path)

    # 複製處理
    def __Copy_Deal(self):
        Work_State = []

        for Copy_Path in self.Output_Data:
           Convert = Copy_Path.split("/")

           # 將檔案路徑的, 上一層資料夾, 與檔名分離出來, 組成輸出路徑
           Output_Path = os.path.join(self.Save_Path, f"[{Convert[-2]}]{Convert[-1]}")

           # 輸出工作
           Work = threading.Thread(target=self.__Copy_Output, args=(Copy_Path, Output_Path))
           Work_State.append(Work)
           Work.start()

        WorkLoad = len(Work_State)
        Progress_Bar = [ # 進度條樣式配置
            ' ', progressbar.Bar(marker='■', left='[', right=']'),
            ' ', progressbar.Counter(), f'/{WorkLoad}',
        ]

        with progressbar.ProgressBar(widgets=Progress_Bar, max_value=WorkLoad) as bar:
            for Index, Working in enumerate(Work_State):
                bar.update(Index)
                Working.join()

        # 開啟存檔位置
        os.startfile(os.path.dirname(self.Save_Path))

    # 處理輸出數據
    def Output(self):
        # 生成保存路徑
        self.Save_Path = f"{self.Origin_Path}/{os.path.basename(self.Origin_Path)} ({self.Output_Select})"

        try:
            if len(self.Output_Data) == 0 or self.Output_Data is None:
                raise DataEmptyError()

            os.mkdir(self.Save_Path)
            self.__Copy_Deal()

        except DataEmptyError:
            print("該路徑下無可複製文件")
        except Exception:
            self.__Copy_Deal()

class TypeSelection(Read, Copy):
    def __init__(self):
        Read.__init__(self)
        Copy.__init__(self)
        self.Repeat = None

    # 選擇輸出類型
    def __Choose(self, Options):

        while True:
            try:
                Select = int(input("\n選擇輸出類型 (代號) : "))
                if Select == 0:
                    print(f"你選擇了 : 全部\n")
                    self.Output_Select = "ALL"
                else:
                    Type = Options[Select-1][0]
                    print(f"你選擇了 : {Type}\n")

                    Format = f".{Type}"
                    self.Output_Data = [Item for Item in self.Complete_Data if Item.endswith(Format)]
                    self.Output_Select = Type

                self.Output()
                if not self.Repeat: break

            except Exception:
                print("無效的代號")

    def Select(self, Repeat: bool=False):
        """
        選擇輸出類型文件

        Repeat = 是否重複選擇
        """
        # 獲取解析數據
        File_Type, Type_Quantity = self.Analysis()
        self.Origin_Path = self.Folder_Path
        self.Repeat = Repeat

        # 展示用
        Show_Table = []
        Show_Table.append(["[0]", "ALL", f"{len(self.Complete_Data)}"])

        # Key = 類型, Value = 對應數量
        Quantity = Counter(Type_Quantity)
        Sort_Cache = {Type: Quantity[Type] for Type in File_Type}

        # 使用數量由大到小排序
        Sorted = sorted(Sort_Cache.items(), key=itemgetter(1), reverse=True)
        for Index, (Type, Count) in enumerate(Sorted):
            Show_Table.append([f"[{Index+1}]", Type, Count])

        # 顯示選擇
        print("{:<6} {:<8} {}".format("代號", "檔案類型", "類型數量"))
        for Row in Show_Table:
            print("{:<10} {:<11} {}".format(Row[0], Row[1], Row[2]))

        # 輸入選擇
        self.__Choose(Sorted)

if __name__ == "__main__":
    TypeSelection().Select(True)