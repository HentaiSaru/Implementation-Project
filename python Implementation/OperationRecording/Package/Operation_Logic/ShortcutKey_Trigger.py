from pynput import keyboard
import threading
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Operation_Recording import Record
from KeyValueTable import PynputKey
from Script_Run import PlayBack

# 運行觸發
class TriggerRun:
    def __init__(self):
        self.rec = Record()
        self.play = PlayBack()

    def StartRecording(self):
        threading.Thread(target=self.rec.Start_Record).start()

    def EndRecording(self):
        self.rec.Stop_Record()

    def StartPlayback(self):
        self.play.Script_play()

    def EndPlayback(self):
        self.play.Script_Stop()

# 快捷鍵監聽
class KeyboardMonitor(PynputKey):
    """
    快捷鍵設置
    * hotkey : 字典格式 , 需要設置兩個鍵位
    * 格式 : {"SR":["",""],"ER":["",""],"SP":["",""],"EP":["",""]}
    * SR = 開始錄製 , ER = 結束錄製 , SP 開始回放 , EP 結束回放

    回放腳本設置
    * script : 字串格式 , 一次設置一個腳本回放
    * 格式 : 如果 Script 資料夾內有 , xxx.json 這是錄製的腳本
    * 傳遞時只需要打 , xxx 名子即可 , 不需要打路徑
    """
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

    def __call__(self, hotkey: dict, script: str=None):
        for Type , Key in hotkey.items():
            if Type == "SR":
                self.sr_hotkey.extend([self.Keytable[Key[0]],self.Keytable[Key[1]]])
            elif Type == "ER":
                self.er_hotkey.extend([self.Keytable[Key[0]],self.Keytable[Key[1]]])
            elif Type == "SP":
                self.sp_hotkey.extend([self.Keytable[Key[0]],self.Keytable[Key[1]]])
            elif Type == "EP":
                self.ep_hotkey.extend([self.Keytable[Key[0]],self.Keytable[Key[1]]])

        if script != None:
            self.tr.play.Script_Set(script)

        print("等待觸發快捷鍵...\n")

        self.__start()