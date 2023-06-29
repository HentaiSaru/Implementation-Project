import threading
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Script_Operation import Operate

class PlayBack:
    def __init__(self):
        self.play = Operate()
        self.PlayScript = None
        self.ThreadinDicator = False

    def Script_Set(self, script: str=None):
        self.PlayScript = script

    def Script_play(self):
        if self.PlayScript == None:
            print("未檢測到回放腳本\n請先使用 Script_Set() 設置要回放的腳本")
        elif self.PlayScript != None and not self.ThreadinDicator:
            print("開始回放")
            threading.Thread(target=self.play.Script_Analysis,args=(self.PlayScript,)).start()
            self.ThreadinDicator = True
        elif self.PlayScript != None and self.play.Execution_status and self.play.Suspended_state:
            print("繼續回放")
            self.play.Pause_Operation()
        else:
            print("當前腳本回放中")

    def Script_Stop(self):
        if self.play.Execution_status and not self.play.Suspended_state:
            print("暫停回放")
            self.play.Pause_Operation()
        elif self.play.Execution_status and self.play.Suspended_state:
            print("當前已暫停回放")
        elif not self.play.Execution_status:
            print("沒有回放中的腳本")