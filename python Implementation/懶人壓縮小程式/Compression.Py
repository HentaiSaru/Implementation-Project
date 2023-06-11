from tkinter import filedialog , messagebox
import tkinter as tk
import threading
import time
import os

"""
Versions 1.0
[+] 簡易懶人壓縮軟體

未來修正
[+] 因個人用途無特別規劃
"""
root = tk.Tk()
root.title("遊俠牌批量壓縮器(非加殼)")
root.iconbitmap("./Compression.ico")
WindowWidth = 850
WindowHeight = 700
root.geometry(f"{WindowWidth}x{WindowHeight}")  # 窗口大小
window_width = root.winfo_screenwidth()         # 取得螢幕寬度
window_height = root.winfo_screenheight()       # 取得螢幕高度
root.geometry(f'+{int(window_width / 3)}+{int(window_height / 3)-160}') # 窗口位置
root.resizable(False, False)

root.configure(background='#A4EBF3') # 整體背景色
OuterFrameColor = "#F4F9F9"
Displayboxcolor = "#20262E"
ImportTextColor = "#CD5888"
Compressbuttonbackgroundcolor = "#BFACE2"
Compressbuttonnormal = "#F0EEED"
Compressbuttontorun = "#DF2E38"

# 最外層的框架
OuterFrame = tk.Canvas(root, width=WindowWidth-20, height=WindowHeight-50, bd=0, highlightthickness=0, bg=OuterFrameColor)
OuterFrame.place(x=WindowWidth-840,y=WindowHeight-660)
# 頂層框架
TopFrame = tk.Canvas(OuterFrame, width=WindowWidth-60,height=WindowHeight-620, bd=0, highlightthickness=0 , bg=OuterFrameColor)
TopFrame.place(x=20,y=0)
# 左側框架
LeftFrame = tk.Canvas(OuterFrame,height=WindowHeight-250,width=350, bd=0, highlightthickness=0, bg=OuterFrameColor)
LeftFrame.place(x=20,y=90)
# 右側框架
RightFrame = tk.Canvas(OuterFrame,height=WindowHeight-250, width=440,bd=0, highlightthickness=0, bg=OuterFrameColor)
RightFrame.place(x=370,y=90)
# 中間框架(本來要做其他功能的)
MiddleFrame = tk.Canvas(OuterFrame, width=20,height=WindowHeight-250, bd=0, highlightthickness=0, bg="#CCF2F4")
MiddleFrame.place(x=350,y=90)
# 底層框架
UnderlyingFramework = tk.Canvas(OuterFrame, width=WindowWidth-60,height=WindowHeight-610, bd=0, highlightthickness=0, bg=OuterFrameColor)
UnderlyingFramework.place(x=20,y=550)

def Home():
    os.system("color 9f")

    # 單獨導入所有文件,將每個文件丟至List
    def ImportAsSeparateFiles():
        global SeparateList , State
        State = True
        SeparateList = [] # 保存每個檔案路徑
        RightText.delete("1.0", "end") # 開啟時將兩邊GUI文本的內容清空 第一行第0個~最後一個
        LeftText.delete("1.0", "end")
        FileSelection = filedialog.askdirectory() # 開啟資料夾選擇窗口
        for root, dirs, files in os.walk(FileSelection): # 路徑,空資料夾,文檔
            for name in files + dirs:
                RightText.insert("end", f"{name}\n\n") # f""是一種格式化字串的方式,這行是在每行的最後插入字串並且換行
                if root == len(files): # 當取的的檔案路徑 == 檔案的長度,也就是最後一個了
                    RightText.insert("end") # 就不會輸入任何字串
                path = os.path.join(root, name) # 取得路徑位置+檔名
                if os.path.isdir(path) and os.path.getsize(path) == 0:continue # 將空白目錄過濾
                SeparateList.append(path)
    # 導入所有文件作為集成壓縮
    def ImportAsIntegratedFile():
        try:
            global IntegrationList , State
            State = False
            RightText.delete("1.0", "end")
            LeftText.delete("1.0", "end")
            FileSelection = filedialog.askdirectory()
            for root, dirs, files in os.walk(FileSelection):
                for name in files + dirs:
                    LeftText.insert("end", f"{name}\n")
                    if root == len(files):
                        LeftText.insert("end")
                    path = os.path.join(root, name)
            if os.path.isdir(path) and os.path.getsize(path) == 0:pass
            IntegrationList = root # 這邊是直接取得完整的所有檔案路徑
        except:pass

    # UPX壓縮觸發
    def UPXCompression():
        try:
            global SeparateList
            UPXCompression.config(fg=Compressbuttontorun,bg=Compressbuttonbackgroundcolor)
            UPXRun(SeparateList,"Compression")
        except Exception as e:
            print("Debug: {}".format(e))
            messagebox.showerror("設置錯誤", "未檢測到文件")
            LeftText.insert("end", f"\n\n\n\n\tUPX不支援整合壓縮")
            UPXCompression.config(fg=Compressbuttonnormal,bg=Compressbuttonbackgroundcolor)
    # UPX壓縮還原觸發
    def UPXRestore():
        try:
            global SeparateList
            UPXRestore.config(fg=Compressbuttontorun,bg=Compressbuttonbackgroundcolor)
            UPXRun(SeparateList,"Restore")
        except Exception as e:
            print("Debug: {}".format(e))
            messagebox.showerror("設置錯誤", "未檢測到文件")
            LeftText.insert("end", f"\n\n\n\n\tUPX不支援整合壓縮")
            UPXRestore.config(fg=Compressbuttonnormal,bg=Compressbuttonbackgroundcolor)
    # UPX壓縮運行
    def UPXRun(Text,Work):
        k = {"exe","dll","ocx","bpl","cpl","sys","ax","acm","drv","tlb"} # UPX支援格式
        Finally = []
        if len(Text) != 0: # 非必要判斷
            for i in range(len(Text)): 
                FileExtension = Text[i].split(".") # 將檔案副檔名與前面切片
                if FileExtension[-1] in map(str.lower, k) and FileExtension[-2] != "upx": # 判斷附檔名是否在支援格式中,後面是一開始寫的架構,避免壓縮到upx.exe自己
                    Format = '"'+Text[i]+'"' # 加上格式後,一個一個丟入列表
                    Finally.append(Format)
                else:continue

            os.system("cls")
            for i in range(len(Finally)): # 開始輸出列表
                time.sleep(0.1)
                if Work == "Compression": # 判斷是要還原還是壓縮
                    UPXCompression.config(fg=Compressbuttonnormal,bg=Compressbuttonbackgroundcolor)
                    upx = "upx -9 --best --ultra-brute --force {}".format(Finally[i]) # 加殼後容易損壞(刪除)
                    threading.Thread(target=os.system, args=(upx,)).start()
                elif Work == "Restore":
                    UPXRestore.config(fg=Compressbuttonnormal,bg=Compressbuttonbackgroundcolor)
                    upx = "upx -d --force {}".format(Finally[i])
                    threading.Thread(target=os.system, args=(upx,)).start()
    

    # State True 為各別輸出 反之 整合輸出(RAR壓縮觸發)
    def RARCopression():
        try:
            global IntegrationList , SeparateList , State
            RARCompression.config(fg=Compressbuttontorun,bg=Compressbuttonbackgroundcolor) # 按下按鈕時變色
            if State: # 判斷是單獨壓縮還是集成壓縮
                RARRespective(SeparateList) # True是單獨,呼叫單獨壓縮方式,傳遞單獨壓縮的列表
            else:RARFusion(IntegrationList) # 反之集成壓縮,給予完整所有路徑
        except Exception as e:
            print("Debug: {}".format(e))
            messagebox.showerror("設置錯誤", "未檢測到文件")
            RARCompression.config(fg=Compressbuttonnormal,bg=Compressbuttonbackgroundcolor)
    # RAR集成壓縮運行
    def RARFusion(Text):
        try:
            Format = '"'+Text.split("\\")[0]+'"' # 壓縮檔案的路徑格式,通常到檔案最後就會變成\,所以將其切片取前面
            os.system("cls")
            RARFormat = '"'+Text.split(":/")[0]+":/"+Text.split(":/")[1].split("\\")[0]+".rar"+'"' # 壓縮檔名的格式
            WinRAR = 'rar a -ri15:0.00001 -m5 -mt24 -md1g  {} {}'.format(RARFormat,Format) # 壓縮指令,並將兩個格式加上
            RARCompression.config(fg=Compressbuttonnormal,bg=Compressbuttonbackgroundcolor) # 按鈕便回原本顏色
            threading.Thread(target=os.system, args=(WinRAR,)).start() # 啟用運行壓縮線程
            time.sleep(0.5)
            messagebox.showinfo("開始壓縮","請稍後...\n檔案將保存於 : {}".format(RARFormat)) # 輸出開始壓縮,並將檔案壓縮位置輸出
        except:pass
    # RAR個別壓縮運行
    def RARRespective(Text):
        try:
            RARCompression.config(fg=Compressbuttonnormal,bg=Compressbuttonbackgroundcolor)
            os.system("cls")
            for i in range(len(Text)): # 因為是個別所以是迴圈,一個一個輸入
                Format = '"'+Text[i]+'"'
                RARFormat = '"'+Text[i].split(":/")[0]+":/"+Text[i].split(":/")[1].split("\\")[1]+".rar"+'"'
                WinRAR = 'rar a -ri15:0.00001 -m5 -mt24 -md1g  {} {}'.format(RARFormat ,Format)
                threading.Thread(target=os.system, args=(WinRAR,)).start()
            messagebox.showinfo("壓縮完成","\n檔案將保存於 : {}".format(RARFormat))
        except:pass


    # ZIP壓縮觸發
    def ZIPCompression():
        try:
            global IntegrationList , SeparateList , State
            ZipCompression.config(fg=Compressbuttontorun,bg=Compressbuttonbackgroundcolor)
            if State:ZIPRespective(SeparateList)
            else:ZIPFusion(IntegrationList)
        except:
            messagebox.showerror("設置錯誤", "未檢測到文件")
            ZipCompression.config(fg=Compressbuttonnormal,bg=Compressbuttonbackgroundcolor)  
    # ZIP集成壓縮
    def ZIPFusion(Text):
        try:
            Format = '"'+Text.split("\\")[0]+'"'
            os.system("cls")
            ZIPFormat = '"'+Text.split(":/")[0]+":/"+Text.split(":/")[1].split("\\")[0]+".7z"+'"'
            ZIP = '7z a {} {} -t7z -m0=lzma2 -mx=9 -mfb=128 -md=1024m -ms=1g -mmt=24'.format(ZIPFormat,Format)
            ZipCompression.config(fg=Compressbuttonnormal,bg=Compressbuttonbackgroundcolor)           
            threading.Thread(target=os.system, args=(ZIP,)).start()
            time.sleep(0.5)
            messagebox.showinfo("開始壓縮","請稍後...\n檔案將保存於 : {}".format(ZIPFormat))
        except:pass
    # ZIP個別壓縮
    def ZIPRespective(Text):
        try:
            os.system("cls")
            ZipCompression.config(fg=Compressbuttonnormal,bg=Compressbuttonbackgroundcolor)
            for i in range(len(Text)):
                Format = '"'+Text[i]+'"'
                ZIPFormat = '"'+Text[i].split(":/")[0]+":/"+Text[i].split(":/")[1].split("\\")[1]+".7z"+'"'
                ZIP = '7z a {} {} -t7z -m0=lzma2 -mx=9 -mfb=128 -md=1024m -ms=1g -mmt=24'.format(ZIPFormat,Format)
                threading.Thread(target=os.system, args=(ZIP,)).start()
            messagebox.showinfo("壓縮完成","\n檔案將保存於 : {}".format(ZIPFormat))
        except:pass
        

    # 個別壓縮導入按鈕
    AloneData = tk.Button(TopFrame,text="導入單檔壓縮")
    AloneData.config(font=("Arial Bold", 25), width=10, height=1, fg="#609EA2" , border=3, relief='groove', bg=OuterFrameColor ,command=ImportAsSeparateFiles)
    AloneData.place(x=470,y=10)
    # 整合壓縮導入按鈕
    IntegrateData = tk.Button(TopFrame,text="導入整合壓縮")
    IntegrateData.config(font=("Arial Bold", 25), width=10, height=1, fg="#609EA2" , border=3, relief='groove', bg=OuterFrameColor ,command=ImportAsIntegratedFile)
    IntegrateData.place(x=55,y=10)

    # 左側文字框
    LeftText = tk.Text(LeftFrame,bg=Displayboxcolor,fg=ImportTextColor)
    LeftText.config(font=("Arial", 13),bd=0)
    LeftText.insert("end", f"\n\n\n\n\tUPX不支援整合壓縮")
    LeftText.place(x=0,y=0)
    # 右側文字框
    RightText = tk.Text(RightFrame,bg=Displayboxcolor,fg=ImportTextColor)
    RightText.config(font=("Arial", 13),bd=0)
    RightText.insert("end", f"單檔壓縮主要適用於UPX壓縮\nUPX是針對EXE和Dll的壓縮\n壓縮前請自行備份\n壓縮後低機率損毀")
    RightText.place(x=0,y=0)

    # 底層UPX壓縮按鈕
    UPXCompression = tk.Button(UnderlyingFramework,text="UPX壓縮",command=UPXCompression)
    UPXCompression.config(font=('Arial',15,'bold'),width=13,height=2,fg=Compressbuttonnormal,border=2,relief='groove',bg=Compressbuttonbackgroundcolor)
    UPXCompression.place(x=0,y=10)
    # 底層UPX壓縮還原按鈕
    UPXRestore = tk.Button(UnderlyingFramework,text="UPX還原",command=UPXRestore)
    UPXRestore.config(font=('Arial',15,'bold'),width=13,height=2,fg=Compressbuttonnormal,border=2,relief='groove',bg=Compressbuttonbackgroundcolor)
    UPXRestore.place(x=180,y=10)
    # 底層PAR壓縮按鈕
    RARCompression = tk.Button(UnderlyingFramework,text="RAR壓縮",command=RARCopression)
    RARCompression.config(font=('Arial',15,'bold'), width=13, height=2,fg=Compressbuttonnormal,border=2,relief='groove',bg=Compressbuttonbackgroundcolor)
    RARCompression.place(x=360,y=10)
    # 底層Zip壓縮按鈕
    ZipCompression = tk.Button(UnderlyingFramework,text="ZIP壓縮",command=ZIPCompression)
    ZipCompression.config(font=("Arial",15,'bold'),width=13,height=2,fg=Compressbuttonnormal,border=2,relief='groove',bg=Compressbuttonbackgroundcolor)
    ZipCompression.place(x=540,y=10)

Home()  # 呼叫首頁GUI(原本預計可由頂部切換不同GUI介面)
root.mainloop()