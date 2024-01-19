from lxml import etree
import threading
import httpx
import time
import os

class WinningInstructions():
    def __init__(self) -> None:
        self.Reward_level = [
            "特別獎", "特獎", "頭獎",
            "二獎", "三獎", "四獎", "五獎", "六獎"
        ]
        self.Reward_conditions = [
            "8 碼相同獲得 1000 萬", "8 碼相同獲得 200 萬", "8 碼相同獲得 20 萬",
            "頭獎末 7 碼相同 4 萬", "頭獎末 6 碼相同 1 萬",
            "頭獎末 5 碼相同 4 千", "頭獎末 4 碼相同 1 千",
            "頭獎末 3 碼相同 200 元"
        ]
wi = WinningInstructions()

class DataProcessing:
    def __init__(self) -> None:
        self.Session = httpx.Client()
        self.Url = "https://invoice.etax.nat.gov.tw/index.html"
        self.Headers = {
            "Cache-Control": "no-cache",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self.Redemption_Data = None

    def __Get_Data(self, Url) -> etree.Element:
        data = self.Session.get(Url, headers=self.Headers)
        return etree.HTML(data.text)

    def __Get_Number(self, tree) -> list:
        number = tree.xpath("//table[@class='etw-table-bgbox etw-tbig']/tbody[1]")[0].xpath(".//span/text()")
        return number[0:2] + [f'{number[i]}{number[i + 1]}' for i in range(2, len(number), 2)]

    def Data_Analysis(self):
        url = self.Url.rsplit("/", 1)[0]
        tree = self.__Get_Data(self.Url)
        link_Data = []

        for index, tr in enumerate(tree.xpath("//ul[@class='etw-submenu etw-submenu01']/li")):
            title = tr.xpath("./a")[0]

            if index == 0:
                link_Data.append({title.get("title") : self.__Get_Number(tree)})
            elif index == 2:
                link_Data.append({title.get("title") : self.__Get_Number(
                    self.__Get_Data(f"{url}/{title.get('href')}")
                )})
                
        self.Redemption_Data = link_Data

class Comparison(DataProcessing):
    def __init__(self) -> None:
        super().__init__()
        self.winning = None
        self.bar = "░" * 10
        self.wait = "兌獎號碼獲取中 "
        self.space = " " * (len(self.bar) * len(self.wait))

    def __Comparison_Date(self):
        print("\n")

        while True:
            Input = input("輸入發票末三碼 (0 中止): ")
            Length = len(Input)

            try:
                if Input == "0":
                    break
                elif not Input.isnumeric():
                    raise ValueError()
                elif Length != 3:
                    raise IndexError()

                for index, number in enumerate(self.winning):
                    if number.endswith(Input):
                        if index < 2:
                            print(f"自行確認是否中獎 ({wi.Reward_level[index]})[{number}]\n")
                        elif index < 5:
                            print(f"自行確認是否中獎 ({wi.Reward_level[2]})[{number}]\n")

            except ValueError:
                print("錯誤輸入類型 !!\n")
            except IndexError:
                print("錯誤的輸入長度 !!\n")
            except Exception:
                print("幹啥呢 !!\n")
                break

    def Select_Date(self) -> None:
        threading.Thread(target=self.Data_Analysis).start()

        while self.Redemption_Data == None:
            print(self.wait, end="")

            for bar in self.bar:
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
                select = int(input("\n輸入[代號]選擇日期: "))

                if select > length:
                    print("錯誤的代號, 請重新選擇")
                else:
                    os.system("cls")
                    for title, number in self.Redemption_Data[select].items():
                        self.winning = number
                        print(title)
                    break

            except ValueError:
                print("代號為數字, 請重新選擇")

        print("\n{:<9} {}".format(wi.Reward_level[0], wi.Reward_conditions[0]))
        for i in range(1, 8):
            print("{:<10} {}".format(wi.Reward_level[i], wi.Reward_conditions[i]))
        self.__Comparison_Date()

if __name__ == "__main__":
    invoice = Comparison()
    invoice.Select_Date()