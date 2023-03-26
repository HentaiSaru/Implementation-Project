import os
import tkinter as tk
from tkinter import filedialog

def FileList():
    global FileList
    FileList = []
    root.withdraw()
    FileSelection = filedialog.askdirectory()
    for root, dirs, files in os.walk(FileSelection):
        for name in files + dirs:
            path = os.path.join(root, name)
            if os.path.isdir(path) and os.path.getsize(path) == 0:continue
            FileList.append(name)

def UPXClassification():
    global FileList , Finally
    Finally = []

    for i in range(len(FileList)):
        FileName , FileExtension = os.path.splitext(FileList[i])
        if FileExtension and (FileExtension == ".exe" or FileExtension == ".dll"):
            if FileList[i] != "upx.exe":
                Finally.append(FileList[i])
        else:continue

def UPXCompression():
    global Finally

    for i in range(len(Finally)):
        os.system("upx -9 --best --ultra-brute --force "+Finally[i])


root = tk.Tk()
root.title("遊俠牌批量壓縮器")
root.geometry("650x500")
root.geometry("+640+320")



#FileList()
#UPXClassification()
#Compression()
root.mainloop()