import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Operation_Recording import Record
from KeyValueTable import PynputKey
from pynput import keyboard
import threading
import time

# 運行觸發
class TriggerRun:
    def __init__(self):
        self.rec = Record()

    def StartRecording(self):
        threading.Thread(target=self.rec.Start_Record).start()

    def EndRecording(self):
        self.rec.Stop_Record()

    def StartPlayback(self):
        print("開始回放")

    def EndPlayback(self):
        print("結束回放")

# 快捷鍵監聽
class KeyboardMonitor(PynputKey):
    def __init__(self):
        self.tr = TriggerRun()
        self.sr_hotkey = []
        self.er_hotkey = []
        self.sp_hotkey = []
        self.ep_hotkey = []
        self.record_key = []

    def __press(self,key):
        self.record_key.append(key)
        if len(self.record_key) == 2:
            if self.sr_hotkey[0] == self.record_key[0] and self.sr_hotkey[1] == self.record_key[1]:
                self.tr.StartRecording()
            elif self.er_hotkey[0] == self.record_key[0] and self.er_hotkey[1] == self.record_key[1]:
                self.tr.EndRecording()
            elif self.sp_hotkey[0] == self.record_key[0] and self.sp_hotkey[1] == self.record_key[1]:
                self.tr.StartPlayback()
            elif self.ep_hotkey[0] == self.record_key[0] and self.ep_hotkey[1] == self.record_key[1]:
                self.tr.EndPlayback()
        
    def __release(self,key):
        if len(self.record_key) > 1:
            self.record_key.clear()

    def __start(self):
        with keyboard.Listener(on_press=self.__press, on_release=self.__release) as listener:
            time.sleep(0.001)
            listener.join()

    def __call__(self, hotkey: dict):
        for Type , Key in hotkey.items():
            if Type == "SR":
                self.sr_hotkey.extend([self.Keytable[Key[0]],self.Keytable[Key[1]]])
            elif Type == "ER":
                self.er_hotkey.extend([self.Keytable[Key[0]],self.Keytable[Key[1]]])
            elif Type == "SP":
                self.sp_hotkey.extend([self.Keytable[Key[0]],self.Keytable[Key[1]]])
            elif Type == "EP":
                self.ep_hotkey.extend([self.Keytable[Key[0]],self.Keytable[Key[1]]])

        self.__start()