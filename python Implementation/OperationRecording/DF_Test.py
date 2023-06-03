import win32gui
import win32api
import win32con
import time

# 獲取目標窗口的句柄
hwnd = win32gui.FindWindow(None, "本機")

while True:
    time.sleep(1)
    _ , _ , W_w , W_h = win32gui.GetClientRect(hwnd)
    UL_x , UL_y , BR_x , BR_y = win32gui.GetWindowRect(hwnd)

    print(f"窗口寬: {W_w} , 窗口高: {W_h}")
    print(f"左上X: {UL_x} , 左上Y : {UL_y} , 右下x : {BR_x} , 右下y : {BR_y}")