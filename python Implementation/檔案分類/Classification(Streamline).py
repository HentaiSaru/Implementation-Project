from tkinter import filedialog
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import tkinter as tk
import progressbar
import threading
import shutil
import os

""" 精簡版檔案分類

Versions 1.0.4

[+] 資料夾路徑選取
[+] 設置分類副檔名
[+] 多線程複製輸出
[+] 重複選擇功能
[+] 輸出進度顯示
[+] 完成自動開啟

* 說明

- 輸出的速度取決於硬碟讀寫速度
- 輸出是採複製的方式 , 對原始檔案無影響

"""
root = tk.Tk()

class DataRead:
    def __init__(self):
        self.directory = None
        self.filename = None

        # 保存選擇資料夾後讀取的所有數據
        self.data = {}
        # 保存所有檔案類型
        self.file_type = set()
        # 保存所有檔案數據
        self.all_data = []
        # 保存過濾後檔案數據
        self.filter_data = []
        # 將塞選的類型數據轉回list保存
        self.listtype =[]

    def open_folder(self):

        root.withdraw() # 隱藏主窗口
        folder_path = filedialog.askdirectory(title="資料夾選擇")
        root.destroy() # 消除

        if folder_path:
            self.directory = folder_path
            self.filename = os.path.basename(folder_path)
            self.__read_file()

    def __read_file(self):

        for root, dirs, files in os.walk(self.directory): # 路徑 , 資料夾 , 檔名
            self.data[root] = files

    def filter_files(self):

        filetype = None

        for path , name in self.data.items():

            if len(name) != 0:
                
                for _filter_ in name:
                    Complete = os.path.join(path,_filter_)
                    try:
                        filetype = _filter_.rsplit(".", 1 )[1].strip()
                    except:
                        pass

                    try:
                        self.file_type.add(filetype.lower())
                        self.all_data.append(Complete.replace("\\","/"))
                    except:
                        print("沒有可分類檔案")
                        return

        self.listtype = list(self.file_type)

        print("代號 [0] : ALL")
        for index , Type in enumerate(self.listtype):
            print(f"代號 [{index+1}] : {Type}")

        self.RepeatedSelection()

    def RepeatedSelection(self):  
        Filter = int(input("\n選擇輸出檔案類型 (代號) : "))

        if Filter == 0:
            print(f"你選擇了 : 全部\n")
        else:
            print(f"你選擇了 : {self.listtype[Filter-1]}\n")

        for data in self.all_data:
            if Filter == 0:
                self.filter_data.append(data)
            else:
                if data.endswith(f".{self.listtype[Filter-1]}"):
                    self.filter_data.append(data)
        if Filter == 0:
            output("ALL")
        else:
            output(self.listtype[Filter-1])

class DataEmptyError(Exception):
    pass

class output:
    def __init__(self,choose):
        self.working_status = []

        try:
            if len(data.filter_data) == 0:
                raise DataEmptyError()

            self.save_route = f"{data.directory}/{data.filename} ({choose})"
            os.mkdir(self.save_route)
            self.__copy_deal_with()
        except DataEmptyError:
            print("該路徑下無指定類型文件")
        except:
            self.save_route = f"{data.directory}/{data.filename} ({choose})"
            self.__copy_deal_with()

    def __copy_deal_with(self): 

        for out in data.filter_data:
            convert = out.split("/")
            file_name = f"{convert[-2]}_{convert[-1]}"
            new_path = os.path.join(self.save_route,file_name)
            # 輸出工作
            Work = threading.Thread(target=self.__copy_output,args=(out,new_path))
            self.working_status.append(Work)
            Work.start()

        # 進度條設置
        self.widgets = [
            ' ', progressbar.Bar(marker='■', left='[', right=']'),
            ' ', progressbar.Counter(), f'/{len(self.working_status)}',
        ]

        with progressbar.ProgressBar(widgets=self.widgets, max_value=len(self.working_status)) as bar:
            for index , working in enumerate(self.working_status):
                bar.update(index)
                working.join()

        # 直接開啟存檔位置
        os.startfile(self.save_route)

        Selection = int(input("\n是否再次選擇 ? [1] YES / [0] NO : "))
        if Selection == 1:
            data.RepeatedSelection()

    def __copy_output(self,out,path):
        shutil.copyfile(out,path)

if __name__ == "__main__":
    data = DataRead()
    data.open_folder()
    data.filter_files()