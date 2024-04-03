from concurrent.futures import *
from tkinter import filedialog
import tkinter as tk
import threading
import chardet
import opencc
import queue
import time
import os

class DataProcessing:
    def __init__(self):
        self.Output_Name = None # 保存輸出名
        self.Output_Rename = None # 保存更改後名
        self.Save = queue.Queue() # 保存轉換後要輸出的數據
        self.Work = queue.Queue() # 保存要進行轉換的工作路徑
        self.lock = threading.Lock()

        self.Converter = opencc.OpenCC("s2twp.json") # 調用 簡體 轉 繁體
        self.Allow = {"po", "txt", "srt", "ass", "ssa", "lng", "lang"} # 允許的檔案類型

        # 文本轉換
        self.Text_conversion = lambda text: self.Converter.convert(text.strip())

        # 計算完成結束時間
        self.ET = lambda start_time: round(time.time() - start_time, 3)

        # 比較字串是否相等
        self.Comp = lambda T1, T2: T1 == T2

    # 過濾文件類型
    def Filter_type(self, path, data):
        if data.rsplit(".", 1)[-1] in self.Allow:
            self.Work.put(os.path.join(path, data).replace("\\", "/"))

class GUI(DataProcessing, tk.Tk):
    def __init__(self):
        DataProcessing.__init__(self)
        tk.Tk.__init__(self, className="文本簡繁轉換器 V2")

        Icon = os.path.join(os.getcwd(), "ChineseConversion.ico")
        self.iconbitmap(Icon)
        self.resizable(0, 0)
        
        # 窗口大小
        self.Win_Width = 280
        self.Win_Height = 235
        # 使用者的螢幕寬高
        self.Win_Cur_Width = lambda: self.winfo_screenwidth()
        self.Win_Cur_Height = lambda: self.winfo_screenheight()

        # 設置窗口大小與位置
        self.geometry(f"{self.Win_Width}x{self.Win_Height}+{int((self.Win_Cur_Width() - self.Win_Width) / 2)}+{int((self.Win_Cur_Height() - self.Win_Height) / 2)}")

        # 設置顏色
        self.failure = "#FF2D2D"
        self.success = "#00A600"
        self.buttontext = "#FDF4F5"
        self.buttontrigger = "#C0DBEA"
        self.buttonbackground = "#E8A0BF"
        self.configure(background="#BA90C6") # 介面背景色

        # 內容顯示框架
        self.Content_frame = tk.Frame(self, width=1060, height=605)
        self.Content_frame.pack_propagate(False) # 禁止大小變動

        # 滾動條框加
        Scrollbar_style = {"cursor": "hand2", "relief": "raised"}
        self.Scrollbar_frame = tk.Frame(self, width=20, height=605, bg=self.buttontext)
        self.ScrollbarY = tk.Scrollbar(self.Scrollbar_frame, Scrollbar_style, width=20)

        # (文字框 / 滾動條)
        self.Content_items = tk.Text(
            self.Content_frame, font=("KaiTi", 24), fg=self.buttontext, bg=self.buttonbackground,
            yscrollcommand=self.ScrollbarY.set
        )

        # 設置標籤 (顯示顏色)
        self.Success = "Success"
        self.Failure = "Failure"
        self.Content_items.tag_configure(self.Success, foreground=self.success)
        self.Content_items.tag_configure(self.Failure, foreground=self.failure)

        # 設置通過滾動條拉動文字框
        self.ScrollbarY.config(command=self.Content_items.yview)

        Button_style = {
            "height": 1, "width": 12, "border": 2,
            "cursor": "hand2", "font": ("Arial Bold", 22),
            "relief": "groove", "fg": self.buttontext, "bg": self.buttonbackground
        }

        self.Text_button = tk.Button(self, Button_style, text="文本輸入", command=lambda: self.Display_Data(True))
        self.File_button = tk.Button(self, Button_style, text="選擇文件", command=self.Select_File)
        self.Document_button = tk.Button(self, Button_style, text="選擇文檔", command=self.Select_Document)
        self.Input_Button_box = [self.Text_button, self.File_button, self.Document_button]

        Button_style.update({ "width": 10, "font": ("Arial Bold", 20) }) # 更新樣式
        self.Create_button = tk.Button(self, Button_style, text="新建輸出", command=lambda: self.Conversion_Trigger("create"))
        self.Override_button = tk.Button(self, Button_style, text="覆蓋輸出", command=lambda: self.Conversion_Trigger("override"))
        self.Output_Button_box = [self.Create_button, self.Override_button]
        self.Reset = tk.Button(self, Button_style, text="重置選擇", command=self.UI_Reset)

    # 運行創建
    def __call__(self):
        self.Text_button.place(x=27, y=15) # 文字輸入
        self.File_button.place(x=27, y=85) # 選擇文件
        self.Document_button.place(x=27, y=155) # 選擇文檔
        self.mainloop()

    # 開啟資料夾    
    def Select_File(self):
        try:
            self.File_button.config(fg=self.buttontrigger, bg=self.buttonbackground)
            data = filedialog.askdirectory()

            if not data:raise FileNotFoundError

            analyze = {} # 遍歷所有數據
            for dirpath, dirnames, filenames in os.walk(data):
                analyze[dirpath] = filenames

            self.Data_Analysis(analyze, self.File_button) 

        except FileNotFoundError:
            self.File_button.config(fg=self.buttontext, bg=self.buttonbackground)
            pass
        except Exception as e:
            print(f"Exception: {e}")

    # 開啟檔案    
    def Select_Document(self):
        try:
            self.Document_button.config(fg=self.buttontrigger, bg=self.buttonbackground)
            data = filedialog.askopenfilename()

            if not data:raise FileNotFoundError

            analyze = {}
            analyze[os.path.dirname(data)] = os.path.basename(data)
            self.Data_Analysis(analyze, self.Document_button)

        except FileNotFoundError:
            self.Document_button.config(fg=self.buttontext, bg=self.buttonbackground)
            pass
        except Exception as e:
            print(f"Exception: {e}")

    # 數據解析
    def Data_Analysis(self, data, button):
        button.config(fg=self.buttontext, bg=self.buttonbackground)

        # 導入工作並分類
        for Path, Name in data.items():
            if isinstance(Name, list):
                for name in Name:
                    self.Filter_type(Path, name.strip())

            elif isinstance(Name, str):
                self.Filter_type(Path, Name.strip())

        # 讀取工作
        while not self.Work.empty():
            work = self.Work.get()
            self.Content_items.insert(tk.END, f"{work}\n") # 插入文本

        self.Display_Data(False)

    # 顯示數據
    def Display_Data(self, direct):
        # 變更窗口大小
        Win_Width = self.Win_Width * 4
        Win_Height = (self.Win_Height - 55) * 4
        self.geometry(f"{Win_Width}x{Win_Height}+{int((self.Win_Cur_Width() - Win_Width) / 2)}+{int((self.Win_Cur_Height() - Win_Height ) / 2)}")

        # 刪除選擇按鈕
        for button in self.Input_Button_box:
            button.destroy()

        # 顯示框架
        self.Content_frame.place(x=20, y=20)
        self.Scrollbar_frame.place(x=1080, y=20)

        # 顯示滾動條
        self.ScrollbarY.pack(side=tk.RIGHT, fill=tk.Y)
        self.ScrollbarY.place(relheight=1.0, relwidth=1.0)

        # 顯示文本
        self.Content_items.pack(fill=tk.BOTH, expand=True)

        if direct:
            def trigger(event):
                TexT = self.Content_items.get("1.0", "end-1c").splitlines()
                self.Content_items.delete("1.0", "end")
                with ThreadPoolExecutor(max_workers=300) as executor:
                    length = len(TexT) - 1 # 取得結尾得長度
                    for index, text in enumerate(TexT):
                        self.Content_items.insert("end", executor.submit(self.Text_conversion, text).result() + ("" if index == length else "\n"))

            self.Content_items.config(font=("Courier", 12))
            self.Reset.place(x=920, y=645)

            self.bind("<Control-v>", trigger) # 貼上觸發
        else:
            # 唯讀禁止修改
            self.Content_items.config(state="disabled")
            # 新建輸出按鈕
            self.Create_button.place(x=720, y=645)
            # 覆蓋輸出按鈕
            self.Override_button.place(x=920, y=645)

    # 觸發轉換
    def Conversion_Trigger(self, OutType):
        # 重新啟用寫入
        self.Content_items.config(state="normal")
        # 獲取文本數據
        data = self.Content_items.get("1.0", "end-1c").splitlines()
        # 刪除文本數據
        self.Content_items.delete("1.0", "end")

        # 為了可以轉換後立即更新UI, 採取此方式, 但運行過多項目會卡
        for index, work in enumerate(data, start=1):
            if work != "":
                threading.Thread(target=self.Conversion_output, args=(index, work, OutType)).start()

        # 刪除輸出按鈕
        for button in self.Output_Button_box:
            button.destroy()
        # 等待所有線程完成
        threading.Thread(target=self.Thread_Wait).start()

    # 轉換後輸出
    def Conversion_output(self, index, work, OutType):

        self.lock.acquire() # 線程鎖
        Start = time.time()

        Directory = os.path.dirname(work)
        FileName = os.path.basename(work)

        if OutType == "create":
            self.Output_Name = os.path.join(Directory, f"(繁體轉換){FileName}")
            self.Output_Rename = os.path.join(Directory, f"(繁體轉換){self.Text_conversion(FileName)}")
        elif OutType == "override":
            self.Output_Name = work
            self.Output_Rename = os.path.join(Directory, self.Text_conversion(FileName))

        try:
            encode = None
            decode_text = None
            with open(work, "rb") as file: # 以二進制讀取
                text = file.read() # 獲取文本
                encode = chardet.detect(text)["encoding"].lower() # 解析編碼類型
                with ThreadPoolExecutor(max_workers=100) as executor:
                    if self.Comp(encode, "utf-8") or self.Comp(encode, "ascii"):
                        decode_text = text.decode("utf-8").splitlines() # 轉換成字串, 並將其序列化
                    elif self.Comp(encode, "utf-16"): # 假設都是 LE 類型的, 無特別處理 BE
                        decode_text = text.decode("utf-16").splitlines()
                    elif self.Comp(encode, "big5"):
                        decode_text = text.decode(encode).encode("utf-8").decode("utf-8").splitlines()
                    else:
                        raise UnicodeDecodeError(encode, b"", 0, 1, "不支援的編碼")

                    # 解碼完成後進行轉換
                    for txt in decode_text:
                        self.Save.put(executor.submit(self.Text_conversion, txt).result())

            # 輸出
            with open(self.Output_Name, "w", encoding=encode) as output:
                while not self.Save.empty():
                    output.write(self.Save.get() + ("\n" if not self.Save.empty() else ""))

            # 完成展示
            self.Content_items.insert(float(index), f"({index}) {os.path.basename(work)} => [Success | {self.ET(Start)}]\n", self.Success)
            # 自動滾動到最下方
            self.Content_items.yview_moveto(1.0)
            # 檔名轉換
            os.rename(self.Output_Name, self.Output_Rename)

        except UnicodeDecodeError as e:
            self.Content_items.insert(float(index), f"({index}) {os.path.basename(work)} => [Failure | {e}]\n", self.Failure)
            self.Content_items.yview_moveto(1.0)
        except Exception as e:
            self.Content_items.insert(float(index), f"(Exception) => {e}\n", self.Failure)
            self.Content_items.yview_moveto(1.0)

        self.lock.release() # 線程鎖釋放

    # 等待全部輸出完成
    def Thread_Wait(self):

        while True:
            if threading.active_count() <= 2:
                self.Reset.place(x=920, y=645)
                break
            time.sleep(0.1)

    # 重置選擇
    def UI_Reset(self):
        # 清除子物件
        # [widget.destroy() for widget in self.winfo_children()]

        self.destroy() # 清除所有物件
        GUI().__call__() # 重新實例化

if __name__ == "__main__":
    GUI().__call__()