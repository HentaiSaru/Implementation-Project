import pyautogui
import win32api
import win32con
import threading
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


# pip install keyboard
import keyboard
# pip install mouse
import mouse

# https://github.com/boppreh/keyboard

class test:
    def __init__(self):
        self.recorded = None
        self.save = []

    def mos(self):
        # 紀錄鍵盤 , 與回放操作
        self.recorded = keyboard.record(until='esc')

    def key(self):
        """ 滑鼠錄製操作 """
        mouse_events = []
        record_steps = 0

        mouse.hook(mouse_events.append)
        mouse.unhook(mouse_events.append)

        for event in mouse_events:

            if str(event).startswith("MoveEvent"):
                record_steps += 1
                if record_steps == 15:
                    self.save.append(event)
                    record_steps = 0
            else:
                self.save.append(event)
                
    def ran(self):
        time.sleep(2)
        # 滑鼠播放
        mouse.play(self.save)
        # 鍵盤輸入
        keyboard.play(self.recorded)
        
t = test()
threading.Thread(target=t.mos).start()
threading.Thread(target=t.key).start()
keyboard.wait('esc')
threading.Thread(target=t.ran).start()

# 紀錄鍵盤 , 與回放操作
#keyboard.add_hotkey('alt+f2', print, args=('被觸發了',))
#keyboard.wait('esc')