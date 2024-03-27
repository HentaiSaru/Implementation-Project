from lxml import etree
import threading
import msvcrt
import httpx
import time
import os

class WinningInstructions:
    def __init__(self) -> None:
        self.Reward_level = [
            "特別獎", "特獎", "頭獎",
            "二獎", "三獎", "四獎", "五獎", "六獎"
        ]
        self.Reward_conditions = [
            "8 碼相同獲得 1000 萬", "8 碼相同獲得 200 萬", 
            "8 碼相同獲得 20 萬", "頭獎末 7 碼相同 4 萬", "頭獎末 6 碼相同 1 萬",
            "頭獎末 5 碼相同 4 千", "頭獎末 4 碼相同 1 千", "頭獎末 3 碼相同 200 元"
        ]

class DataProcessing(WinningInstructions):
    def __init__(self) -> None:
        super().__init__()
        self.Session = httpx.Client()
        self.Url = "https://invoice.etax.nat.gov.tw/index.html"
        self.Headers = {
            "Cache-Control": "no-cache",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        }
        self.Redemption_Data = None

    def __Get_Data(self, Url) -> etree.Element:
        try:
            data = self.Session.get(Url, headers=self.Headers)
            if data.status_code == 200:
                return etree.HTML(data.text)
            else:
                raise Exception()
        except:
            os.system("cls")
            print("網站連接失敗, 檢查網路或伺服器")
            os._exit(0)

    def __Get_Number(self, tree) -> list:
        number = tree.xpath("//table[@class='etw-table-bgbox etw-tbig']/tbody[1]")[0].xpath(".//span/text()")
        return number[0:2] + [f'{number[i]}{number[i + 1]}' for i in range(2, len(number), 2)]

    def Data_Analysis(self):
        link_Data = []
        url = self.Url.rsplit("/", 1)[0]
        tree = self.__Get_Data(self.Url)

        for tr in tree.xpath("//ul[@class='etw-submenu etw-submenu01']/li"):
            title = tr.xpath("./a")[0]
            href = title.get("href")
            
            if href == "index.html": # 最近期
                link_Data.append({title.get("title") : self.__Get_Number(tree)})
            elif href == "lastNumber.html": # 上一期
                link_Data.append({title.get("title") : self.__Get_Number(
                    self.__Get_Data(f"{url}/{title.get('href')}")
                )})

        self.Redemption_Data = link_Data

class Comparison(DataProcessing):
    def __init__(self) -> None:
        super().__init__()
        self.input = ""
        self.winning = None
        self.bar = "░" * 10
        self.wait = "兌獎號碼獲取中 "
        self.space = " " * (len(self.bar) * len(self.wait))

    def __Comparison_Date(self):
        print("\n")

        while True:
            if self.input == "":
                print("輸入發票末三碼 [Esc 中止]: ", end="")

            Input = msvcrt.getch().decode()
            if Input == "\x1b":
                print("中止", end="")
                break
            else:
                print(Input, end="")

            try:
                self.input += Input
                if len(self.input) >= 3:
                    print("\n")

                    if self.input.lower() == "dev":
                        print(f"{self.winning}\n")

                    elif not self.input.isnumeric():
                        self.input = ""
                        raise ValueError()

                    else:
                        for index, number in enumerate(self.winning):
                            if number.endswith(self.input):
                                if index < 2:
                                    print(f"自行確認是否中獎 ({self.Reward_level[index]}): {number}\n")
                                elif index < 5:
                                    print(f"自行確認是否中獎 ({self.Reward_level[2]}): {number}\n")

                    self.input = ""

            except ValueError:
                print("錯誤輸入類型 !!\n")
            except Exception:
                print("幹啥呢 !!\n")
                break

    def Select_Date(self) -> None:
        threading.Thread(target=self.Data_Analysis).start()

        while self.Redemption_Data == None:
            print(self.wait, end="")

            for bar in self.bar:
                if self.Redemption_Data != None: break
                print(bar, end="", flush=True)
                time.sleep(0.1)

            print(f"\r{self.space}", end="")
            print("\r", end="")

        print("{:<6} {}".format("代號", "兌獎日期"))
        for index, Redemption_Data in enumerate(self.Redemption_Data):
            for key in Redemption_Data.keys():
                print("[{}]{:<5} {}".format(index, "", key))

        length = len(self.Redemption_Data)
        while True:
            try:
                print("\n輸入[代號]選擇日期: ", end="")
                select = int(msvcrt.getch().decode())

                if select > length:
                    print("\n錯誤的代號, 請重新選擇")
                else:
                    os.system("cls")
                    for title, number in self.Redemption_Data[select].items():
                        self.winning = number
                        print(title)
                    break

            except ValueError:
                print("\n代號為數字, 請重新選擇")

        print("\n{:<9} {}".format(self.Reward_level[0], self.Reward_conditions[0]))
        for i in range(1, 8):
            print("{:<10} {}".format(self.Reward_level[i], self.Reward_conditions[i]))
        self.__Comparison_Date()

if __name__ == "__main__":
    invoice = Comparison()
    invoice.Select_Date()