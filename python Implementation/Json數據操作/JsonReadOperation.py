import json
import time
import os

class ReadJson:
    def __init__(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.Json_name = None
        self.Json_data = None

        self.Json_Operation_A = {}
        self.Json_Operation_B = {}
        self.Json_special = []

        self.Operation_Pass = True
        self.Stop_Line = None
        self.Calculate = 0

    def __read_json(self):
        try:
            with open(self.Json_name , "r" , encoding="utf-8") as file:
                self.Json_data = json.loads(file.read())
            return True
        except:
            print("找不到設置的 Json 文件")
            return False

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

            state = self.__read_json()

            if state:
                amount = len(self.Json_data)

                for key , value in self.Json_data.items():
                    if self.Operation_Pass:
                        if self.Calculate == self.Stop_Line:
                            self.Calculate = 0
                            amount -= self.Stop_Line
                            n = input(f"按下Enter繼續測試 [剩餘:{amount}] [輸入 0 結束] : ")

                            if n == "0":
                                self.Operation_Pass = False
                        else:
                            if Location == 0:
                                os.system(f"start {key}")
                            else:
                                os.system(f"start {value}")
                            time.sleep(0.3)
                        self.Calculate += 1
                    else:
                        self.Json_Operation_A[key] = value

                if OutPut:
                    self.__output_delete(self.Json_Operation_A)

        except ValueError:
            print("Location 只有 0 和 1")

    def cookie_parsing(self, JsonName: str, ShowDict: bool=False, OutPut: bool=False):
        """
        讀取 Json 格式的 Cookie , 並分類出有用的部份
        * JsonName 設置要開啟的 Json 檔全名 例 : Test.json
        * ShowDict 解析後以字典打印
        * OutPut 將轉換成功的字典輸出
        """
        self.Json_name = JsonName
        state = self.__read_json()

        if state:

            for cookie in self.Json_data:
                name = cookie["name"]
                value = cookie["value"]
                self.Json_Operation_A[name] = value

            if ShowDict:
                print(self.Json_Operation_A)

            if OutPut:
                self.__output(self.Json_Operation_A)
                
    def cookie_parsing_2(self, JsonName: str, ShowDict: bool=False, OutPut: bool=False):
        """
        讀取 Json 格式的 Cookie , 保留原數據格式解析方法
        * JsonName 設置要開啟的 Json 檔全名 例 : Test.json
        * ShowDict 解析後以字典打印
        * OutPut 將轉換成功的字典輸出
        """
        self.Json_name = JsonName
        state = self.__read_json()
    
        if state:

            for cookie in self.Json_data:
                special_dict = {}
                special_dict["name"] = cookie["name"]
                special_dict["value"] = cookie["value"]
                self.Json_special.append(special_dict)

            if ShowDict:
                print(self.Json_special)

            if OutPut:
                self.__output(self.Json_special)
                
    def json_to_txt(self, JsonName: str, Location: int=0, Delete: bool=False):
        """
        將 Json 檔 Key 或 Value 的值 , 變成 txt 文字輸出
        * JsonName 設置要開啟的 Json 檔全名 例 : Test.json
        * Location 設置轉換的值 [0 使用 Key , 1 使用 Value , 2 使用全部]
        * Delete 是否將原始的 Json 檔案刪除
        """
        try:
            if Location < 0 or Location > 2:
                raise ValueError()
            
            self.Json_name = JsonName
            state = self.__read_json()
            
            if state:
                with open(self.Json_name.replace(".json",".txt"), "w", encoding="utf-8") as file:
                    for index , (key , value) in enumerate(self.Json_data.items()):
                        if Location == 0:
                            file.write(key)
                        elif Location == 1:
                            file.write(value)
                        elif Location == 2: 
                            file.write(f"[{key}] : [{value}]")
                        if index != len(self.Json_data) - 1: # 最後一行以前都換行
                            file.write("\n")
                if Delete:
                    os.system(f"del /f /s /q {self.Json_name} >nul 2>&1")
                    print(f"已刪除 {self.Json_name}")
                print("輸出完成...")
            
        except ValueError:
            print("Location 只有 0 和 1")

    def __output(self, data):
        if len(data) > 0:
            with open(self.Json_name , "w" , encoding="utf-8") as file:
                file.write(json.dumps(data, indent=4, separators=(',',':')))
            print("輸出完成...")

    def __output_delete(self, data):
        if len(data) > 0:
            with open(self.Json_name , "w" , encoding="utf-8") as file:
                file.write(json.dumps(data, indent=4, separators=(',',':')))
            print("輸出完成...")
        else:
            os.system(f"del /f /s /q {self.Json_name} >nul 2>&1")
            print(f"已刪除 {self.Json_name}")

if __name__ == "__main__":
    rj = ReadJson()
    # 開啟網頁連結
    # rj.open_url("範圍201-300.json",20,OutPut=True)
    
    # 解析 cookie (只保留數值)
    # rj.cookie_parsing("Cookies.json",OutPut=True)
    
    # 解析 cookie (保留 name 和 value 的 key 值)
    # rj.cookie_parsing_2("Cookies.json",OutPut=True)
    
    # 將 Json 文件內容轉成 txt
    rj.json_to_txt("可用網址.json" , Delete=True)