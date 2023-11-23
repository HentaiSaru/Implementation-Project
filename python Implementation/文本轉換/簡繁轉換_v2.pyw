from concurrent.futures import *
from tkinter import filedialog
import tkinter as tk
import threading
import chardet
import opencc
import queue
import time
import os

root = tk.Tk()
root.title("簡轉繁 文字轉換器")
Icon = os.path.join(os.getcwd(), "ChineseConversion.ico")
root.iconbitmap(Icon)
root.resizable(False, False)
# 窗口大小
interface_width = 280
interface_height = 180
# 取得使用者的螢幕寬高
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()
# 計算窗口正中間的位置
windowCenterWidth = (window_width - interface_width) / 2
windowCenterHeight = (window_height - interface_height) / 2
# 設置窗口大小與位置
root.geometry(f"{interface_width}x{interface_height}+{int(windowCenterWidth)}+{int(windowCenterHeight)}")
root.configure(background="#BA90C6") # 介面背景色
# 其餘顏色設置
buttonbackground = "#E8A0BF"
buttontrigger = "#C0DBEA"
buttontext = "#FDF4F5"
success = "#00A600"
failure = "#FF2D2D"

class DataProcessing:
    def __init__(self):
        self.Save = queue.Queue() # 保存轉換後要輸出的數據
        self.Work = queue.Queue() # 保存要進行轉換的工作路徑
        self.Allow = ("txt", "ass") # 允許的檔案類型
        self.Converter = opencc.OpenCC("s2twp.json")

    # 過濾文件類型
    def Filter_type(self, path, data):
        if data.endswith(self.Allow):
            self.Work.put(os.path.join(path, data).replace("\\", "/"))

    # 轉換成繁體
    def Text_conversion(self, text) -> str:
        
        return self.Converter.convert(text.strip())

class UICreation(DataProcessing):
    def __init__(self):
        super().__init__()
        self.Content_items = None
        self.Content_frame = None
        self.Success = "Success"
        self.Failure = "Failure"

        self.Scrollbar = None
        self.Scrollbar_frame = None

        self.File_button = None
        self.Document_button = None

        self.Output_Name = None
        self.Create_button = None
        self.Override_button = None

        self.lock = threading.Lock()

    # 初始選擇 UI
    def Initial_UI(self):
        self.File_button = tk.Button(
            root, text="選擇文件", font=("Arial Bold", 22),
            height=1, width=12, border=2, relief="groove",
            fg=buttontext, bg=buttonbackground, command=lambda: self.__Select_File(self.File_button)
        )

        self.Document_button = tk.Button(
            root, text="選擇文檔", font=("Arial Bold", 22),
            height=1, width=12, border=2, relief="groove",
            fg=buttontext, bg=buttonbackground, command=lambda: self.__Select_Document(self.File_button)
        )

        # 選擇文件按鈕
        self.File_button.place(x=27, y=15)
        # 選擇文檔按鈕
        self.Document_button.place(x=27, y=85)

        # 宣告框架
        self.Content_frame = tk.Frame(root, width=1060, height=605)
        self.Content_frame.pack_propagate(False) # 禁止大小變動
        self.Scrollbar_frame = tk.Frame(root, width=20, height=605, bg=buttontext)

        # 宣告 (文字框 / 滾動條)
        self.Scrollbar = tk.Scrollbar(self.Scrollbar_frame, width=20, cursor="hand2", relief="raised")
        self.Content_items = tk.Text(
            self.Content_frame, font=("KaiTi", 24), fg=buttontext, bg=buttonbackground, yscrollcommand=self.Scrollbar.set
        )
        # 設置標籤
        self.Content_items.tag_configure(self.Success, foreground=success)
        self.Content_items.tag_configure(self.Failure, foreground=failure)
        # 設置可通過滾動條拉動文字框
        self.Scrollbar.config(command=self.Content_items.yview)

    # 開啟資料夾    
    def __Select_File(self, button):
        try:
            button.config(fg=buttontrigger, bg=buttonbackground)
            data = filedialog.askdirectory()

            if not data:raise FileNotFoundError

            analyze = {} # 遍歷所有數據
            for root, dirs, files in os.walk(data):
                analyze[root] = files

            self.__Data_Analysis(analyze, button) 

        except FileNotFoundError:
            button.config(fg=buttontext, bg=buttonbackground)
            pass
        except Exception as e:
            print(e)

    # 開啟檔案    
    def __Select_Document(self, button):
        try:
            button.config(fg=buttontrigger, bg=buttonbackground)
            data = filedialog.askopenfilename()

            if not data:raise FileNotFoundError

            analyze = {}
            analyze[os.path.dirname(data)] = os.path.basename(data)
            self.__Data_Analysis(analyze, button)

        except FileNotFoundError:
            button.config(fg=buttontext, bg=buttonbackground)
            pass
        except Exception as e:
            print(e)

    # 數據解析
    def __Data_Analysis(self, data, button):
        button.config(fg=buttontext, bg=buttonbackground)

        # 導入工作並分類
        for path, name in data.items():
            if isinstance(name, list):
                for Filter in name:
                    self.Filter_type(path, Filter.strip())

            elif isinstance(name, str):
                self.Filter_type(path, name.strip())

        # 讀取工作
        while not self.Work.empty():
            work = self.Work.get()
            self.Content_items.insert(tk.END, f"{work}\n")

        self.__Display_Data()

    # 顯示數據
    def __Display_Data(self):
        # 變更窗口大小      
        root.geometry(f"{interface_width*4}x{interface_height*4}+{int(windowCenterWidth/2+150)}+{int(windowCenterHeight/2-50)}")
        # 刪除選擇檔案按鈕
        self.File_button.destroy()
        self.Document_button.destroy()

        # 顯示框架
        self.Content_frame.place(x=20, y=20)
        self.Scrollbar_frame.place(x=1080, y=20)

        # 顯示滾動條
        self.Scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.Scrollbar.place(relheight=1.0, relwidth=1.0)

        # 唯讀禁止修改
        self.Content_items.config(state="disabled")
        # 顯示文本
        self.Content_items.pack(fill=tk.BOTH, expand=True)

        self.Create_button = tk.Button(
            root, text="新建輸出", font=("Arial Bold", 20),
            height=1, width=10, border=2, relief="groove",
            fg=buttontext, bg=buttonbackground, command=lambda: self.__Conversion_Trigger("create")
        )
        self.Override_button = tk.Button(
            root, text="覆蓋輸出", font=("Arial Bold", 20),
            height=1, width=10, border=2, relief="groove",
            fg=buttontext, bg=buttonbackground, command=lambda: self.__Conversion_Trigger("override")
        )
        self.Create_button.place(x=720, y=645)
        self.Override_button.place(x=920, y=645)

    def __Conversion_Trigger(self, OutType):
        # 重新啟用寫入
        self.Content_items.config(state="normal")
        # 獲取文本數據
        data = self.Content_items.get("1.0", tk.END).splitlines()
        # 刪除文本數據
        self.Content_items.delete("1.0", tk.END)

        # 為了可以轉換後立即更新UI, 採取此方式, 但運行過多項目會卡
        for index, work in enumerate(data, start=1):
            if work != "":
                threading.Thread(target=self.__Conversion_output, args=(index, work, OutType)).start()

        # 消除按鈕
        self.Create_button.destroy()
        self.Override_button.destroy()
        # 等待所有線程完成
        threading.Thread(target=self.__Thread_Wait).start()

    # 轉換後輸出
    def __Conversion_output(self, index, work, OutType):

        self.lock.acquire() # 線程鎖

        if OutType == "create":
            File_name = os.path.basename(work)
            directory = os.path.dirname(work)
            self.Output_Name = os.path.join(directory, f"(繁體轉換){File_name}")
        elif OutType == "override":
            self.Output_Name = work
            
        try:
            with open(work, "rb") as file: # 以二進制讀取
                text = file.read() # 獲取文本
                encode = chardet.detect(text)["encoding"] # 解析編碼
                #text.decode(encode["encoding"]).encode("utf-8") # 進行解碼後, 編碼成 utf-8
                if encode.startswith("UTF-8"):
                    with ThreadPoolExecutor(max_workers=100) as executor: # 多線程
                        for txt in file: 
                            self.Save.put(executor.submit(self.Text_conversion, txt).result())

            # 輸出
            with open(self.Output_Name, "w", encoding="utf-8") as output:
                while not self.Save.empty():
                    output.write(self.Save.get() + "\n")

            # 完成展示
            self.Content_items.insert(float(index), f"[{index}]=>{os.path.basename(work)} - 轉換完成\n", self.Success)
            # 自動滾動到最下方
            self.Content_items.yview_moveto(1.0)
            # 檔名轉換
            os.rename(self.Output_Name, self.Text_conversion(self.Output_Name))

        except UnicodeDecodeError:
            self.Content_items.insert(float(index), f"[{index}]=>{os.path.basename(work)} - 解碼錯誤\n", self.Failure)
            self.Content_items.yview_moveto(1.0)
        except Exception as e:
            self.Content_items.insert(float(index), f"[例外錯誤]=>{e}\n", self.Failure)
            self.Content_items.yview_moveto(1.0)

        self.lock.release() # 線程鎖釋放

    # 重置選擇
    def __UI_Reset(self):
        # 清除所有物件
        [widget.destroy() for widget in root.winfo_children()]
        # 回歸原始大小
        root.geometry(f"{interface_width}x{interface_height}+{int(windowCenterWidth)}+{int(windowCenterHeight)}") 
        # 重新創建 UI
        ui.Initial_UI()

    # 等待全部輸出完成
    def __Thread_Wait(self):

        while True:
            if threading.active_count() <= 2:
                Reset = tk.Button(
                    root, text="重置選擇", font=("Arial Bold", 20),
                    height=1, width=10, border=2, relief="groove",
                    fg=buttontext, bg=buttonbackground, command=self.__UI_Reset
                )
                Reset.place(x=920, y=645)
                break
            time.sleep(1)

if __name__ == "__main__":
    ui = UICreation()
    ui.Initial_UI()
    root.mainloop()