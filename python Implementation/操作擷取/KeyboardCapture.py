from pynput import keyboard
import ctypes
import time
import re

class capture:
    def __init__(self):
        self.Input_method_dictionary = {
            "1028": "繁中",
            "2052": "簡中",
            "1033": "英文",
            "1041": "日文",
        }

        self.key_cache = None
        self.Format = r"['<>]"

        self.press_time = None
        self.release_time = None

    # 取得輸入法可以更好判斷 , 輸入了什麼
    def Get_Input(self):
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        thread_id = ctypes.windll.user32.GetWindowThreadProcessId(hwnd, 0)
        layout_id = ctypes.windll.user32.GetKeyboardLayout(thread_id)
        return self.Input_method_dictionary[str(f"{layout_id & 0xFFFF}")]

    def press(self,key):
        SKey = re.sub(self.Format,"",str(key))

        if SKey != self.key_cache:
            self.press_time = time.time() # 按下時間
            print(f"按下鍵 : {SKey}")
            self.key_cache = SKey

    def release(self,key):
        self.key_cache = None # 放開時要清空緩存 (不然會有Bug)
        self.release_time = time.time()
        SKey = re.sub(self.Format,"",str(key))

        print(f"輸入法 : [{self.Get_Input()}] | 放開鍵 : [{SKey}] | ", "持續時間 : [%.3f]\n" %(self.release_time-self.press_time))

class Keyboard(capture):
    def __init__(self):
        super().__init__()

    def __call__(self, delay=0.001):
        self.run(delay)

    def run(self, delay):
        with keyboard.Listener(on_press=self.press, on_release=self.release) as listener:
            time.sleep(delay)
            listener.join()