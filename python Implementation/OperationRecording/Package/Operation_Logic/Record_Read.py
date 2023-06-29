import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from StopCompletely import Exit

#Todo - 腳本保存 與 腳本讀取 -

class InputOutput:
    def __init__(self):
        self.exit = Exit()
        self.script_path = "{}\\Script".format(os.path.dirname(os.path.abspath(__file__)).rsplit("\\",2)[0])
        self.script_data = {}

        # 判斷腳本目錄是否存在 , 不存在創建
        if not os.path.exists(self.script_path):
            os.mkdir(self.script_path)

    def Save_Script(self, save_name: str, save_data: dict):
        save_path = os.path.join(self.script_path,f"{save_name}.json")

        with open(save_path , "w") as file:
            file.write(json.dumps(save_data))

        print(f"{save_name}.json 腳本以保存")

    def Read_Script(self, save_name: str):
        save_path = os.path.join(self.script_path,f"{save_name.rsplit('.json',1)[0]}.json")

        try:

            with open(save_path , "r") as file:
                self.script_data = json.loads(file.read())

            return self.script_data
        
        except:
            print("找不到設置腳本\n強制中止程式")
            self.exit.ex()