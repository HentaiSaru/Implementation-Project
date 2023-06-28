import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Record_Read import InputOutput
from KeyValueTable import Win32Key
import win32api
import win32con
import time

# 回放操作
class PlayBack(Win32Key):
    def __init__(self):
        self.script = {}
        self.io = InputOutput()

    # 讀取腳本
    def Read_Script(self, script):
        self.script = self.io.Read_Script(script)

    # 腳本解析
    def Script_Analysis(self, script):
        self.Read_Script(script)

        for Type , Value in self.script.items():
            TypeAnalysis = Type.split("-")[0]

            if TypeAnalysis == "M":
                self.Mouse_Operation(Value)
            elif TypeAnalysis == "K":
                self.Keyboard_Operation(Value)
            elif TypeAnalysis == "W":
                time.sleep((Value[0]/2))

    # 滑鼠操作
    def Mouse_Operation(self, operate):
        x=operate[0]
        y=operate[1]
        button=operate[2]
        during=operate[3]

        if during < 0:
            during = 0

        win32api.SetCursorPos((x, y))

        if isinstance(button,int):
            button = str(button)
            if button == "1":
                win32api.mouse_event(self.MouseKT_D[button], 0, 0, 120, 0)
            elif button == "-1":
                win32api.mouse_event(self.MouseKT_D[button], 0, 0, -120, 0)
        elif button != None:

            if during > 1:
                click_time = time.time()
                while time.time() - click_time < during:
                    time.sleep(0.05)
                    win32api.mouse_event(self.MouseKT_D[button], 0, 0, 0, 0)
                win32api.mouse_event(self.MouseKT_U[button], 0, 0, 0, 0)
            else:
                win32api.mouse_event(self.MouseKT_D[button], 0, 0, 0, 0)
                time.sleep(during)
                win32api.mouse_event(self.MouseKT_U[button], 0, 0, 0, 0)

        time.sleep(0.001)

    # 鍵盤操作
    def Keyboard_Operation(self, operate):
        keys=operate[0]
        during=operate[1]

        if during < 0:
            during = 0

        try:
            vk = win32api.VkKeyScan(keys)

            if during > 1:
                press_time = time.time()
                while time.time() - press_time < during:
                    win32api.keybd_event(vk, 0, 0, 0)
                    time.sleep(0.04)
                win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)
            else:
                win32api.keybd_event(vk, 0, 0, 0)
                time.sleep(during)
                win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)
        except:
            try:
                if during > 1:
                    press_time = time.time()
                    while time.time() - press_time < during:
                        win32api.keybd_event(self.KeyboardKT[keys], 0, 0, 0)
                        time.sleep(0.04)
                    win32api.keybd_event(self.KeyboardKT[keys], 0, win32con.KEYEVENTF_KEYUP, 0)
                else:
                    win32api.keybd_event(self.KeyboardKT[keys], 0, 0, 0)
                    time.sleep(during)
                    win32api.keybd_event(self.KeyboardKT[keys], 0, win32con.KEYEVENTF_KEYUP, 0)
            except:
                print(f"[{keys}] 未註冊的 鍵盤值...")
                pass

play = PlayBack()
play.Script_Analysis("Script-2023-06-29-02-44-26")