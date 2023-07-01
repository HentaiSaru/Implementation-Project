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


# pip install keyboard
import keyboard
# pip install mouse
import mouse

# https://github.com/boppreh/keyboard

# 紀錄鍵盤 , 與回放操作
recorded = keyboard.record(until='alt+f2')
# print("紀錄")
# time.sleep(5)
# keyboard.play(recorded)
for i in range(1,5+1):
    print(f"\r回放 : {i}s" , end="" , flush=True)
    time.sleep(1)
keyboard.play(recorded)
input("暫停")

mouse_events = []
record_steps = 0

mouse.hook(mouse_events.append)

keyboard.wait('esc')

mouse.unhook(mouse_events.append)

save = []

for event in mouse_events:

    if str(event).startswith("MoveEvent"):
        record_steps += 1
        if record_steps == 15:
            save.append(event)
            record_steps = 0
    else:
        save.append(event)

#mouse.play(save)

#keyboard.add_hotkey('alt+f2', print, args=('被觸發了',))
# 紀錄鍵盤 , 與回放操作
#keyboard.wait('esc')