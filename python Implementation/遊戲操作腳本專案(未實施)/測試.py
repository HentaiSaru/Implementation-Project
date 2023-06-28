import win32gui
import win32api
import win32con
import time

def get_window(hwnd, windows):
    if win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        if title:
            windows.append((hwnd, title))

windows = []
win32gui.EnumWindows(get_window, windows)

for i, (hwnd, title) in enumerate(windows):
    print(f"{i+1}. {title}")
index = int(input("輸入數字選擇: ")) - 1

if index < 0 or index >= len(windows):
    print("錯誤的選項")
else:
    hwnd = windows[index][0]
    print(f"選擇的窗口: {windows[index][1]} (窗口句炳={hwnd})")

  
    # 開啟窗口最大化
    win32gui.ShowWindow(hwnd,win32con.SW_MAXIMIZE)
    
    # 設置操作窗口
    time.sleep(3)
    win32gui.SetForegroundWindow(hwnd)
    # 窗口做標和大小
    print(win32gui.GetWindowRect(hwnd))