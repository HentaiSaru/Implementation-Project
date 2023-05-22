from PyQt6.QtWidgets import *
from tqdm import tqdm
import threading
import shutil
import sys
import os

""" 簡易版檔案分類

Versions 1.0

[+] 選取資料夾路徑
[+] 設置分類副檔名
[+] 多線程複製輸出

"""

app = QApplication([])

class DataRead:
    def __init__(self):
        self.directory = None
        self.filename = None
        self.data = {}
        self.filter_data = []

    def open_folder(self):

        folder_path = QFileDialog.getExistingDirectory(None, "選擇檔案夾")

        if folder_path:
            self.directory = folder_path
            self.filename = os.path.basename(folder_path)
            self.read_file()

    def read_file(self):

        for root, dirs, files in os.walk(self.directory): # 路徑 , 資料夾 , 檔名
            self.data[root] = files

    def filter_files(self,filter):
        
        for path , name in self.data.items():

            if len(name) != 0:

                for _filter_ in name:
                    Complete = os.path.join(path,_filter_)
                    if Complete.endswith(f".{filter}"):
                        self.filter_data.append(Complete.replace("\\","/"))

class output:
    def __init__(self):
        try:
            convert = data.filter_data[0].split("/")
            self.save_route = f"{convert[0]}/{convert[1]}/{convert[2]}/{data.filename}-分類合併"
            os.mkdir(self.save_route)
            self.copy_deal_with()
        except:
            print("該路徑無指定類型文件")

    def copy_deal_with(self):

        pbar = tqdm(total=len(data.filter_data),desc="開始合併輸出")

        for out in data.filter_data:
            convert = out.split("/")
            file_name = f"{convert[-2]}_{convert[-1]}"
            new_path = os.path.join(self.save_route,file_name)

            threading.Thread(target=self.copy_output,args=(out,new_path)).start()
            pbar.update(1)

        choose = QMessageBox.question(None, "輸出完畢", "是否開啟存檔位置",QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if choose == QMessageBox.StandardButton.Yes:
            os.startfile(self.save_route)

    def copy_output(self,out,path):
        shutil.copyfile(out,path)

if __name__ == "__main__":
    data = DataRead()

    data.open_folder()
    data.filter_files(input("副檔名:"))

    output()
    app.exec()