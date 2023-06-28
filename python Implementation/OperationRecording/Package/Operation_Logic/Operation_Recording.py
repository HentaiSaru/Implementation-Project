import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pynput import keyboard , mouse
from Record_Read import InputOutput
from datetime import datetime
import threading
import time
import re

# 操作紀錄
class Record:
    def __init__(self):
        self.io = InputOutput()
        self.or_dict = {}
        self.or_list = []

        self.step = 0
        self.timing = 0
        self.ST = 0
        self.ET = 0
        self.Mlistener = None
        self.Klistener = None
        self.TimingStart = None

        self.waitMark = "W"
        self.MouseMark = "M"
        self.KeyboardMark = "K"

    def __Timer(self):
        while self.TimingStart:
            time.sleep(1)
            self.timing += 1

    # 滑鼠錄製
    def __Mouse_Record(self):
        
        # 點擊位置
        def click(x, y, button, pressed):
            if pressed:
                self.step += 1
                self.or_dict[f"{self.waitMark}-{self.step}"] = [self.timing]
                self.timing = 0
                self.ST = time.time()
            else:
                self.ET = time.time()
                self.step += 1
                self.or_list = [x, y, str(button).split("Button.")[1], (self.ET-self.ST)]
                self.or_dict[f"{self.MouseMark}-{self.step}"] = self.or_list

        # 滾動
        def scroll(x, y, none, step):
            self.step += 1
            self.or_dict[f"{self.waitMark}-{self.step}"] = [self.timing]
            self.timing = 0

            # 滾動的 step +1 是上滾輪 -1 是下滾輪
            self.step += 1
            self.or_list = [x, y, step, 0]
            self.or_dict[f"{self.MouseMark}-{self.step}"] = self.or_list

        # 監聽
        with mouse.Listener(on_click=click, on_scroll=scroll) as Mlistener:
            self.Mlistener = Mlistener
            time.sleep(0.01)
            Mlistener.join()

    # 鍵盤錄製 (不支援組合鍵/快捷鍵)
    def __Keyboard_Record(self):
        
        # 按下
        def press(key):
            self.step += 1
            self.or_dict[f"{self.waitMark}-{self.step}"] = [self.timing]
            self.timing = 0
            self.ST = time.time()

        # 放開
        def release(key):
            self.ET = time.time()
            self.step += 1
            New_key = re.sub(r"[<>'\"]", "", str(key))
            try:
                New_key = New_key.split("Key.")[1]
            except:
                pass

            self.or_list = [New_key , (self.ET-self.ST)]
            self.or_dict[f"{self.KeyboardMark}-{self.step}"] = self.or_list

        # 監聽
        with keyboard.Listener(on_press=press, on_release=release) as Klistener:
            self.Klistener = Klistener
            time.sleep(0.01)
            Klistener.join()

    # 開始錄製
    def Start_Record(self):
        self.step = 0
        self.timing = 0
        self.or_dict.clear()
        self.TimingStart = True

        time.sleep(1) # 避免啟動快捷被錄製
        print("開始錄製")

        threading.Thread(target=self.__Mouse_Record).start()
        threading.Thread(target=self.__Keyboard_Record).start()
        threading.Thread(target=self.__Timer).start()

    # 中止錄製
    def Stop_Record(self):
        self.TimingStart = False
        self.Mlistener.stop()
        self.Klistener.stop()

        print("結束錄製")

        # 結束會自動輸出
        self.__OutPut_Record()

    def __OutPut_Record(self):
        self.io.Save_Script(
            f"Script-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}",
            self.or_dict
        )