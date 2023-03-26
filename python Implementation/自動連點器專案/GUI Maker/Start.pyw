import os
import time
from tkinter import messagebox , ttk
import tkinter as tk
import warnings
from GUIV.InitialV import *
from PIL import Image, ImageTk

"""
Versions 1.0
[+] GUI參數傳遞接口建置
      
後續工作
[+] 製作後續功能

未來修正
[+] 優化快捷鍵感應速度問題
[+] 採用不同的包製作GUI
[+] 優化徒法煉鋼的邏輯判斷
"""
settings = []
SetVerification = {
    "ShortcutKeyA": ['Ctrl','Alt','Shift'],
    "ShortcutKeyB": ["F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12"],
    "MouseButton": ["left", "right","none"],
}

class InvalidIntervalSpeed(Exception):
    pass
class ShortcutKeySettingError(Exception):
    pass
class WrongMouseButtons(Exception):
    pass

try:  
    with open('settings.json', 'r') as f:
        settings = json.load(f)

    #判斷設置
    if settings["UserSettings"]["IntervalSpeed"] < 0.01:
        raise InvalidIntervalSpeed()
    if settings["UserSettings"]["StartShortcutKeyA"] not in SetVerification["ShortcutKeyA"] or settings["UserSettings"]["EndShortcutKeyA"] not in SetVerification["ShortcutKeyA"]:
        raise ShortcutKeySettingError()
    if settings["UserSettings"]["StartShortcutKeyB"] not in SetVerification["ShortcutKeyB"] or settings["UserSettings"]["EndShortcutKeyB"] not in SetVerification["ShortcutKeyB"]:
        raise ShortcutKeySettingError()
    if settings["UserSettings"]["MouseButton"] not in SetVerification["MouseButton"]:
        raise WrongMouseButtons()
    
    Archive = True
    ArchiveRead(settings,Archive)

except InvalidIntervalSpeed:
    messagebox.showerror("設置錯誤", "你設置了無效的間隔速度")
except ShortcutKeySettingError:
    messagebox.showerror("設置錯誤", "你設置了無效的快捷鍵")
except WrongMouseButtons:
    messagebox.showerror("設置錯誤", "你設置了無效滑鼠按鍵")
except FileNotFoundError:
    Archive = False
    ArchiveRead(settings,Archive)
except:
    messagebox.showerror("設置錯誤", "請不要亂改設置檔\n即將刪除你的設置檔")
    os.system("del /f /s /q settings.json >nul 2>&1")
finally:
    #最終呼叫初始GUI介面
    InitialGUI()