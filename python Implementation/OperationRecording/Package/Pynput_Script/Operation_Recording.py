from pynput import keyboard , mouse
from datetime import datetime
import threading
import time
import sys
import os
import re

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Record_Read import InputOutput

# 操作紀錄
class Record:
    def __init__(self):
        self.io = InputOutput()
        self.or_dict = {}
        self.or_list = []

        self.step = 0 # 操作步驟
        self.timing = 0.01 # 沒操作的等待時間
        self.record_steps = 0 # 滑鼠移動多少步紀錄

        self.ST = 0 # 按下時間
        self.ET = 0 # 放開時間

        self.PressKey = None # 鍵盤按下鍵
        self.keyboardSteps = None # 鍵盤操作步驟

        self.Mlistener = None # 滑鼠監聽
        self.Klistener = None # 鍵盤監聽
        self.TimingStart = None # 延時監聽

        self.waitMark = "W" # 等待記號
        self.MouseMark = "M" # 滑鼠記號
        self.KeyboardMark = "K" # 鍵盤記號

    def __Timer(self):
        while self.TimingStart:
            time.sleep(0.1)
            self.timing += 0.01

    # 滑鼠錄製
    def __Mouse_Record(self):
        
        # 點擊位置
        def click(x, y, button, pressed):
            if pressed:
                self.step += 1
                self.or_dict[f"{self.waitMark}-{self.step}"] = [self.timing]
                self.timing = 0.01
                self.ST = time.time()
            else:
                self.ET = time.time()
                self.or_list = [x, y, str(button).split("Button.")[1], (self.ET-self.ST)]
                self.or_dict[f"{self.MouseMark}-{self.step}"] = self.or_list

        def move(x, y):
            self.record_steps += 1

            if self.record_steps == 15:
                self.step += 1
                self.or_dict[f"{self.waitMark}-{self.step}"] = [self.timing]
                self.timing = 0.01

                self.or_list = [x, y, None, 0]
                self.or_dict[f"{self.MouseMark}-{self.step}"] = self.or_list
                self.record_steps = 0

        # 滾動
        def scroll(x, y, none, step):
            self.step += 1
            self.or_dict[f"{self.waitMark}-{self.step}"] = [self.timing]
            self.timing = 0.01

            # 滾動的 step +1 是上滾輪 -1 是下滾輪
            self.or_list = [x, y, step, 0]
            self.or_dict[f"{self.MouseMark}-{self.step}"] = self.or_list

        # 監聽
        with mouse.Listener(on_click=click, on_scroll=scroll, on_move=move) as Mlistener:
            self.Mlistener = Mlistener
            time.sleep(0.001)
            Mlistener.join()

    # 鍵盤錄製 (不支援組合鍵/快捷鍵)
    def __Keyboard_Record(self):
        
        # 按下
        def press(key):
            self.step += 1
            self.or_dict[f"{self.waitMark}-{self.step}"] = [self.timing]
            self.timing = 0.01

            self.ST = time.time()

            New_key = re.sub(r"[<>'\"]", "", str(key))
            try:
                New_key = New_key.split("Key.")[1]
            except:
                pass
            self.PressKey = New_key

            self.or_list = [self.PressKey , 0]
            self.keyboardSteps = f"{self.KeyboardMark}-{self.step}"
            self.or_dict[self.keyboardSteps] = self.or_list

        # 放開
        def release(key):
            self.ET = time.time()
            self.or_list = [self.PressKey , (self.ET-self.ST)]
            self.or_dict[self.keyboardSteps] = self.or_list

        # 監聽
        with keyboard.Listener(on_press=press, on_release=release) as Klistener:
            self.Klistener = Klistener
            time.sleep(0.001)
            Klistener.join()

    # 開始錄製
    def Start_Record(self):
        self.step = 0
        self.timing = 0.01
        self.or_dict.clear()
        self.TimingStart = True

        time.sleep(1) # 避免啟動快捷被錄製
        print("開始錄製")

        threading.Thread(target=self.__Mouse_Record).start()
        threading.Thread(target=self.__Keyboard_Record).start()
        threading.Thread(target=self.__Timer).start()

    # 中止錄製
    def Stop_Record(self):
        try:
            self.TimingStart = False
            self.Mlistener.stop()
            self.Klistener.stop()

            print("結束錄製")

            # 結束會自動輸出
            self.__OutPut_Record()
        except:
            print("沒有進行中的錄製...")

    def __OutPut_Record(self):
        self.io.Save_Script(
            f"Script-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}",
            self.or_dict
        )