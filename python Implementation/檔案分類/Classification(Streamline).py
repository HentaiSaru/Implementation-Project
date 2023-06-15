from tkinter import filedialog
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from tqdm import tqdm
import tkinter as tk
import threading
import shutil
import os

""" 精簡版檔案分類

Versions 1.0.2

[+] 資料夾路徑選取
[+] 設置分類副檔名
[+] 多線程複製輸出
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
        self.data = {}

        self.file_type = set()

        self.all_data = []
        self.filter_data = []

    def open_folder(self):

        root.withdraw() # 隱藏主窗口
        folder_path = filedialog.askdirectory(title="資料夾選擇")
        root.destroy() # 消除

        if folder_path:
            self.directory = folder_path
            self.filename = os.path.basename(folder_path)
            self.read_file()

    def read_file(self):

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

        listtype = list(self.file_type)
        for index , Type in enumerate(listtype):
            print(f"類型 [{index+1}] : {Type}")

        Filter = int(input("\n輸入檔案類型 (數字) : "))
        print(f"你選擇了 : {listtype[Filter-1]}\n")

        for data in self.all_data:
            if data.endswith(f".{listtype[Filter-1]}"):
                self.filter_data.append(data)

        output()

class DataEmptyError(Exception):
    pass

class output:
    def __init__(self):
        self.working_status = []

        try:
            if len(data.filter_data) == 0:
                raise DataEmptyError()

            self.save_route = f"{data.directory}/{data.filename}-分類合併"
            os.mkdir(self.save_route)
            self.copy_deal_with()
        except DataEmptyError:
            print("該路徑下無指定類型文件")
        except:
            self.save_route = f"{data.directory}/{data.filename}-分類合併"
            self.copy_deal_with()

    def copy_deal_with(self):

        for out in data.filter_data:
            convert = out.split("/")
            file_name = f"{convert[-2]}_{convert[-1]}"
            new_path = os.path.join(self.save_route,file_name)
            # 輸出工作
            Work = threading.Thread(target=self.copy_output,args=(out,new_path))
            self.working_status.append(Work)
            Work.start()

        # 等待真實操作全部完成
        pbar = tqdm(total=len(self.working_status),desc="開始合併輸出")
        for working in self.working_status:
            pbar.update(1)
            working.join()
        pbar.close()

        # 直接開啟存檔位置
        os.startfile(self.save_route)

    def copy_output(self,out,path):
        shutil.copyfile(out,path)

if __name__ == "__main__":
    data = DataRead()

    data.open_folder()
    data.filter_files()