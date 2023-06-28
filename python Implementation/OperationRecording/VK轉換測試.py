import keyboard
import pyautogui
import win32api
import win32con
import time


# 模擬按下 'a' 鍵
# win32api.keybd_event(vk, 0, 0, 0)
# win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)

table = "abcdefghijklmnopqrstuvwxyz"
table2 = ['up','left',"down","right"]

def test(key):
    vk = win32api.VkKeyScan(key)
    return vk