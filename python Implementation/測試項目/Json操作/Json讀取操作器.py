import json
import os

class ReadJson:
    def __init__(self):
        self.Json_name = None
        self.Json_data = None

        self.Json_Operation_A = {}
        self.Json_Operation_B = {}

        self.Operation_Pass = True
        self.Stop_Line = None
        self.Calculate = 0

    def __read_json(self):
        with open(self.Json_name , "r") as file:
            self.Json_data = json.loads(file.read())

    def open_url(self, JsonName: str, StopLine: int, Location: int=0, OutPut: bool=False):
        """
        讀取 Json 值中的 URL , 並開啟網址的方法
        * JsonName 設置要開啟的 Json 檔全名 例 : Test.json
        * StopLine 設置 10 就是開啟 10 個停止一次
        * Location 設置 0 使用 Key 值開啟 , 1 使用 Value 值開啟
        * OutPut 設置是否運行完畢 , 將剩下未開啟的網址進行輸出 , 如果沒有未開啟的網址了 , 就會直接刪除該 Json 檔案
        """
        try:

            if Location < 0 or Location > 1:
                raise ValueError()

            self.Json_name = JsonName
            self.Stop_Line = StopLine

            self.__read_json()

            for key , value in self.Json_data.items():
                if self.Operation_Pass:
                    if self.Calculate > self.Stop_Line:
                        self.Calculate = 0
                        n = input("按下任意鍵繼續測試 [輸入 0 結束] : ")

                        if n == "0":
                            self.Operation_Pass = False
                    else:
                        if Location == 0:
                            os.system(f"start {key}")
                        else:
                            os.system(f"start {value}")

                    self.Calculate += 1
                else:
                    self.Json_Operation_A[key] = value
            if OutPut:
                self.__output_remaining()

        except ValueError:
            print("Location 只有 0 和 1")

    def __output_remaining(self):
        if len(self.Json_Operation_A) > 0:
            with open(self.Json_name , "w") as file:
                file.write(json.dumps(self.Json_Operation_A, indent=4, separators=(',',':')))
        else:
            os.system(f"del /f /s /q {self.Json_name}")


if __name__ == "__main__":
    rj = ReadJson()
    rj.open_url("範圍201-300.json",10,OutPut=True)