import keyboard
import pyautogui
import win32api
import win32con
import time
import json


# 模擬按下 'a' 鍵
# win32api.keybd_event(vk, 0, 0, 0)
# win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)

table = "abcdefghijklmnopqrstuvwxyz"
table2 = ['up','left',"down","right"]

def test(key):
    vk = win32api.VkKeyScan(key)
    return vk

# path = "Script/Script-2023-06-29-12-09-49.json"
# 
# script_data = {}
# with open(path , "r") as file:
    # script_data = json.loads(file.read())
# 
# i = 0
# for key , script in script_data.items():
# 
    # if key.split("-")[0] == "M":
# 
        # i += 1
# 
        # if i == 15:
            # x = script[0]
            # y = script[1]
            # win32api.SetCursorPos((x, y))
            # i = 0
# 
        # time.sleep(0.001)

import threading

pause_event = threading.Event()

def trigger():
    if pause_event.is_set(): # 第二次觸發將被暫停
        pause_event.clear()
    else: # 第一次觸發設置,繼續運行
        pause_event.set()

def loop():
    trigger()
    for i in range(1, 101):
        print(i)
        pause_event.wait()
        time.sleep(0.5)

thread = threading.Thread(target=loop)
thread.start()

# 啟動


# 觸發暫停
time.sleep(5)
trigger()

time.sleep(2)
trigger()