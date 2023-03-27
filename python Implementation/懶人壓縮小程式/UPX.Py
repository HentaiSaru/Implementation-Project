import os
import threading
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

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

def Home():

    def ImportSeparately():
        global SeparateList , State
        State = True
        SeparateList = []
        RightText.delete("1.0", "end")
        FileSelection = filedialog.askdirectory()
        for root, dirs, files in os.walk(FileSelection):
            for name in files + dirs:
                RightText.insert("end", f"{name}\n\n")
                if root == len(files):
                    RightText.insert("end")
                path = os.path.join(root, name)
                if os.path.isdir(path) and os.path.getsize(path) == 0:continue
                SeparateList.append(path)

    def IntegrationImport():
        global IntegrationList , State
        State = False
        IntegrationList = []
        LeftText.delete("1.0", "end")
        FileSelection = filedialog.askdirectory()
        for root, dirs, files in os.walk(FileSelection):
            for name in files + dirs:
                LeftText.insert("end", f"{name}\n")
                if root == len(files):
                    LeftText.insert("end")
                path = os.path.join(root, name)
                if os.path.isdir(path) and os.path.getsize(path) == 0:continue
                IntegrationList.append(path)
    

    def RARCopression():
        #WinRAR a -ri15:0.00001 -m5 -mt24 -md1g  "test.rar" "R:\自寫連點器測試" "[檔名].rar" "[被壓縮檔]"

        pass

    def UPXCompression():
        try:
            global SeparateList
            UPXCompression.config(fg=Compressbuttontorun,bg=Compressbuttonbackgroundcolor)
            UPX(SeparateList,"Compression")
        except:
            messagebox.showerror("設置錯誤", "未檢測到文件")
            UPXCompression.config(fg=Compressbuttonnormal,bg=Compressbuttonbackgroundcolor)

    def UPXRestore():
        try:
            global SeparateList
            UPXRestore.config(fg=Compressbuttontorun,bg=Compressbuttonbackgroundcolor)
            UPX(SeparateList,"Restore")
        except:
            messagebox.showerror("設置錯誤", "未檢測到文件")
            UPXRestore.config(fg=Compressbuttonnormal,bg=Compressbuttonbackgroundcolor)

    def UPX(Text,Work):
        k = {"exe","dll","ocx","bpl","cpl","sys","ax","acm","drv","tlb"}
        Finally = []
        if len(Text) != 0:
            for i in range(len(Text)):
                FileExtension = Text[i].split(".")
                if FileExtension[-1] in map(str.lower, k) and FileExtension[-2] != "upx":
                    Format = '"'+Text[i]+'"'
                    Finally.append(Format)
                else:continue

            for i in range(len(Finally)):
                time.sleep(0.1)
                if Work == "Compression":
                    upx = "upx -9 --best --ultra-brute --force {}".format(Finally[i])
                    threading.Thread(target=os.system, args=(upx,)).start()
                    UPXCompression.config(fg=Compressbuttonnormal,bg=Compressbuttonbackgroundcolor)
                elif Work == "Restore":
                    upx = "upx -d --force {}".format(Finally[i])
                    threading.Thread(target=os.system, args=(upx,)).start()
                    UPXRestore.config(fg=Compressbuttonnormal,bg=Compressbuttonbackgroundcolor)

    OuterFrame = tk.Canvas(root, width=WindowWidth-20, height=WindowHeight-50, bd=0, highlightthickness=0, bg=OuterFrameColor)
    OuterFrame.place(x=WindowWidth-840,y=WindowHeight-660)

    TopFrame = tk.Canvas(OuterFrame, width=WindowWidth-60,height=WindowHeight-620, bd=0, highlightthickness=0 , bg=OuterFrameColor)
    TopFrame.place(x=20,y=0)

    AloneData = tk.Button(TopFrame, text="導入單檔壓縮")
    AloneData.config(font=("Arial Bold", 25), width=10, height=1, fg="#609EA2" , border=3, relief='groove', bg=OuterFrameColor ,command=ImportSeparately)
    AloneData.place(in_=TopFrame, x=470 , y=10)

    IntegrateData = tk.Button(TopFrame, text="導入整合壓縮")
    IntegrateData.config(font=("Arial Bold", 25), width=10, height=1, fg="#609EA2" , border=3, relief='groove', bg=OuterFrameColor ,command=IntegrationImport)
    IntegrateData.place(in_=TopFrame, x=55 , y=10)


    LeftFrame = tk.Canvas(OuterFrame,height=WindowHeight-250,width=350, bd=0, highlightthickness=0, bg=OuterFrameColor)
    LeftFrame.place(x=20,y=90)
    LeftText = tk.Text(LeftFrame,bg=Displayboxcolor,fg=ImportTextColor)
    LeftText.config(font=("Arial", 13),bd=0)
    LeftText.insert("end", f"\n\n\n\n\tUPX不支援整合壓縮")
    LeftText.place(in_=LeftFrame,x=0,y=0)

    MiddleFrame = tk.Canvas(OuterFrame, width=20,height=WindowHeight-250, bd=0, highlightthickness=0, bg="#CCF2F4")
    MiddleFrame.place(x=350,y=90)

    RightFrame = tk.Canvas(OuterFrame,height=WindowHeight-250, width=440,bd=0, highlightthickness=0, bg=OuterFrameColor)
    RightFrame.place(x=370,y=90)
    RightText = tk.Text(RightFrame,bg=Displayboxcolor,fg=ImportTextColor)
    RightText.config(font=("Arial", 13),bd=0)
    RightText.place(in_=RightFrame,x=0,y=0)

    UnderlyingFramework = tk.Canvas(OuterFrame, width=WindowWidth-60,height=WindowHeight-610, bd=0, highlightthickness=0, bg=OuterFrameColor)
    UnderlyingFramework.place(x=20,y=550)
    UPXCompression = tk.Button(UnderlyingFramework,text="UPX壓縮",command=UPXCompression)
    UPXCompression.config(font=('Arial',15,'bold'), width=13, height=2, fg=Compressbuttonnormal , border=2, relief='groove', bg=Compressbuttonbackgroundcolor)
    UPXCompression.place(x=0,y=10)

    UPXRestore = tk.Button(UnderlyingFramework,text="UPX還原",command=UPXRestore)
    UPXRestore.config(font=('Arial',15,'bold'), width=13, height=2, fg=Compressbuttonnormal , border=2, relief='groove', bg=Compressbuttonbackgroundcolor)
    UPXRestore.place(x=180,y=10)


Home()
root.mainloop()