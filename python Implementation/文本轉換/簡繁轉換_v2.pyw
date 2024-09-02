import os
import time
import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from concurrent.futures import ThreadPoolExecutor

import opencc
import chardet
import pyperclip

"""
>   Versions 1.0.1 - V2

//  [ 簡轉繁 轉換器 ]

        ~ (開發/運行環境):
        $ Windows 11 23H2
        $ Python 3.12.5 64-bit

        ~ 第三方庫:
        $ opencc
        $ chardet
        $ pyperclip

        ~ 功能說明:
        ^ 文本輸入
        ^ 文件輸入
        ^ 文檔輸入
        ^ 結果顯示
        ^ 多線程轉換

        ~ 使用說明:
        & 文本輸入:
        & 將需轉換文字貼上至, 文本輸入框 (用快捷 Ctrl + v) 貼上才會觸發轉換
        & 一貼上後就會立即轉換結果, 並將結果顯示於文本框中, 同時會自動添加結果到剪貼簿當中
        & 代表可立即貼上到所需地方, 不用再次手動複製轉換結果, 點選其他窗口後, 再次回到轉換器, 會自動清除先前內容

        Todo 選擇文件:
        & 選擇一個資料夾, 會根據 Allow 參數中, 允許的類型將導入結果, 顯示在文本框中
        & 接著就可以選擇, 要使用覆蓋原檔案輸出, 還是創建新檔案輸出, 新檔案會創建在導入的目錄中
        & 轉換時會顯示轉換結果, 告知轉換成功狀態, 與轉換消耗時間, 失敗通常會顯示原因

        Todo 選擇檔案:
        & 功能基本同上, 只是變成選擇單個檔案, 但也會受到 Allow 的允許類型影響

        ~ 更新說明:
        [~] 轉換修改為維持原始格式
        [+] 文本輸入轉換, 自動清除先前轉換結果
"""

class DataProcessing:
    def __init__(self):
        self.Output_Name = None # 保存輸出名
        self.Output_Rename = None # 保存更改後名
        self.Save = queue.Queue() # 保存轉換後要輸出的數據
        self.Work = queue.Queue() # 保存要進行轉換的工作路徑
        self.lock = threading.Lock()

        self.Converter = opencc.OpenCC("s2twp.json") # 調用 簡體 轉 繁體
        self.Allow = {"po", "txt", "srt", "ass", "ssa", "lng", "lang", "json"} # 允許的檔案類型

        # 文本轉換
        self.Text_conversion = lambda text: self.Converter.convert(text)

        # 計算完成結束時間
        self.ET = lambda start_time: round(time.time() - start_time, 3)

        # 比較字串是否相等
        self.Comp = lambda T1, T2: T1 == T2

    # 過濾文件類型
    def Filter_type(self, path, data):
        if data.rsplit(".", 1)[-1] in self.Allow:
            self.Work.put(os.path.join(path, data).replace("\\", "/"))

class GUI(DataProcessing, tk.Tk):
    __slots__ = (
        "Output_Name", "Output_Rename", 
        "Save", "Work", "lock", "ET",
        "Converter", "Allow", "Comp",
        "Text_conversion",
        "Scrollbar_style",
        "Button_style",
        "Content_items",
    )
    
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
        self.Document_button = tk.Button(self, Button_style, text="選擇檔案", command=self.Select_Document)
        self.Input_Button_box = [self.Text_button, self.File_button, self.Document_button]

        Button_style.update({ "width": 10, "font": ("Arial Bold", 20) }) # 更新樣式
        self.Create_button = tk.Button(self, Button_style, text="新建輸出", command=lambda: self.Conversion_Trigger("create"))
        self.Override_button = tk.Button(self, Button_style, text="覆蓋輸出", command=lambda: self.Conversion_Trigger("override"))
        self.Output_Button_box = [self.Create_button, self.Override_button]
        self.Reset = tk.Button(self, Button_style, text="重置選擇", command=self.UI_Reset)

        # 用於文本輸入時, 自動清除內容
        self.WaitClear = False

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
            data = filedialog.askdirectory(title="選擇資料夾")

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
            data = filedialog.askopenfilename(title="選擇單獨檔案")

            if not data:raise FileNotFoundError

            analyze = {}
            analyze[os.path.dirname(data)] = os.path.basename(data)
            self.Data_Analysis(analyze, self.Document_button)

        except FileNotFoundError:
            self.Document_button.config(fg=self.buttontext, bg=self.buttonbackground)
            pass
        except Exception as e:
            print(f"Exception: {e}")

    # 取得文本框數據
    def GetText(self, DEL: bool=True, END: str="end-1c"):
        Text = self.Content_items.get("1.0", END).splitlines(); Exist = len(Text) > 0
        self.Content_items.delete("1.0", "end") if DEL and Exist else None
        return Text if Exist and Text[0] != "" else False

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

        # 判斷讀取的狀態 (只取一個小範圍)
        if self.GetText(False, "2.0"):
            self.Display_Data(False)
        else:
            messagebox.showerror("格式錯誤", "無可轉換的檔案格式")

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
            def trigger(event): # 觸發後先讀取文本
                TexT = self.GetText()
                with ThreadPoolExecutor(max_workers=1000) as executor:
                    scrapbook = ""
                    length = len(TexT) - 1 # 取得結尾得長度
                    for index, text in enumerate(TexT): # 使用線程池 以多線程進行轉換
                        change = executor.submit(self.Text_conversion, text).result() + ("" if index == length else "\n")
                        scrapbook += change # 結果合併成一個字串
                        self.Content_items.insert("end", change) # 結果插入文本框
                    pyperclip.copy(scrapbook) # 將結果添加到使用者 剪貼簿

            # 焦點狀態
            def focus_in(event):
                if self.WaitClear:
                    self.WaitClear = False
                    self.GetText() # 清除內容

            # 離開焦點
            def focus_out(event):
                self.WaitClear = True

            self.Content_items.config(font=("Courier", 12))
            self.Reset.place(x=920, y=645)

            self.Content_items.bind("<FocusIn>", focus_in)
            self.Content_items.bind("<FocusOut>", focus_out)
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
        TexT = self.GetText()

        # 為了可以轉換後立即更新UI, 採取此方式, 但運行過多項目會卡
        for index, work in enumerate(TexT, start=1):
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

                #! 等待後續修正 處理更多編碼, 語法優化
                with ThreadPoolExecutor(max_workers=1000) as executor:
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