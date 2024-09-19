# import threading
import msvcrt
# import time
import json
import os

from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.console import Console
from rich.table import Table
from lxml import etree
import httpx

#! 預計添加: 根據獲取月份, 顯示兌獎期限, 並修改 dev 也就是獲取時顯示的數據, 根據取得區域顯示對應獎項

# 複寫原生打印方式
console = Console()
def print(*args, **kwargs):
    console.print(*args, **kwargs)

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
        self.Prize_claim_period = {
            "1-2": "1-2 月份領獎期限為 4/6 ~ 7/5",
            "3-4": "3-4 月份領獎期限為 6/6 ~ 9/5",
            "5-6": "5-6 月份領獎期限為 8/6 ~ 11/5",
            "7-8": "7-8 月份領獎期限為 10/6 ~ 次年 1/5",
            "9-10": "9-10 月份領獎期限為 12/6 ~ 次年 3/5",
            "11-12": "11-12 月份領獎期限為次年 2/6 ~ 5/5"
        }

class DataProcessing:
    def __init__(self) -> None:
        self.Redemption_Data = None
        self.client = httpx.Client(http2=True)
        self.Headers = {
            "Cache-Control": "no-cache",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        }

    def __Get_Data(self, Uri) -> etree.Element:
        try:
            data = self.client.get(Uri, headers=self.Headers)
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

    def Data_Analysis(self, Uri) -> None:
        link_Data = {}
        Url = Uri.rsplit("/", 1)[0]
        tree = self.__Get_Data(Uri)

        for tr in tree.xpath("//ul[@class='etw-submenu etw-submenu01']/li"):
            title = tr.xpath("./a")[0]
            href = title.get("href")

            if href == "index.html": # 最近期
                link_Data[1] = {
                    "month": title.get("title"),
                    "number": self.__Get_Number(tree)
                }

            elif href == "lastNumber.html": # 上一期
                link_Data[2] = {
                    "month": title.get("title"),
                    "number": self.__Get_Number(
                        self.__Get_Data(f"{Url}/{title.get('href')}")
                    )
                }

        self.Redemption_Data = link_Data

class Comparison(DataProcessing, WinningInstructions):
    def __init__(self, Uri) -> None:
        DataProcessing.__init__(self)
        WinningInstructions.__init__(self)

        self.Uri = Uri
        self.input = ""
        self.winning = {}

        # self.bar = "░" * 10
        # self.wait = "兌獎號碼獲取中 "
        # self.space = " " * (len(self.bar) * len(self.wait))

    def __Comparison_Date(self) -> None:
        print("\n")

        while True:
            if self.input == "":
                print("輸入發票末三碼 [Esc 停止]: ", end="", style="yellow")

            Input = msvcrt.getch().decode()
            if Input == "\x1b":
                print("停止", end="")
                break
            else:
                print(Input, end="")

            try:
                self.input += Input
                if len(self.input) >= 3:
                    print("\n")

                    if self.input.lower() == "dev":
                        print(f"{json.dumps(self.winning, indent=4, ensure_ascii=False)}\n", style="bold bright_cyan")

                    elif not self.input.isnumeric():
                        self.input = ""
                        raise ValueError()

                    else:
                        winning = self.winning.get(self.input)
                        if winning is not None:
                            if winning['level'] == "頭獎":
                                print(
                                    f"中獎了!! 自行確認中獎等級 ({winning['level']}): {winning['number']}\n",
                                    style="bold green"
                                )
                            else:
                                print(
                                    f"自行確認是否中獎 ({winning['level']}): {winning['number']}\n",
                                    style="bold green"
                                )

                    self.input = ""

            except ValueError:
                print("錯誤輸入類型 !!\n")
            except Exception as E:
                print(f"幹啥呢 !!\n")
                break

    def __Select_Date(self) -> None:
        """ (原生進度條實現)
        threading.Thread(target=self.Data_Analysis, args=(self.Uri,)).start()
        while self.Redemption_Data is None:
            print(self.wait, end="")

            for bar in self.bar:
                if self.Redemption_Data is not None: break
                print(bar, end="", flush=True)
                time.sleep(0.1)

            print(f"\r{self.space}\r", end="")
        """

        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("取得數據中...", start=False)
            self.Data_Analysis(self.Uri)
            progress.stop_task(task)

        os.system("cls")

        select_table = Table()
        select_table.add_column("代號", justify="center", style="bold bright_red")
        select_table.add_column("日期", justify="center", style="bold bright_yellow")

        for index, data in self.Redemption_Data.items():
            select_table.add_row(str(index), data["month"])
        print(select_table)

        display_table = Table()
        while True:
            try:
                print("\n輸入[代號]選擇日期: ", end="", style="bold green")
                select = self.Redemption_Data.get( # 取得對應 Key 值
                    int(msvcrt.getch().decode()) # 讀取數字輸入
                )

                if select is None:
                    print("\n錯誤的代號, 請重新選擇", style="bold red")
                else:
                    os.system("cls")

                    #! 如需要根據選取月份, 顯示兌換日期, 需要解析此處選擇的 month
                    display_table.add_column(select["month"], justify="center", style="bold")
                    data = select["number"]

                    # 將數據列表解析為字典 (測試以下寫法 比列導式快一些, 雖然列導式更簡潔) [Key 值為末三碼]
                    for index, number in enumerate(data[:2]): # 這個為, 特別獎, 特獎
                        self.winning[number[-3:]] = {"level": self.Reward_level[index], "number": number}
                    for number in data[2:]: # 這個都是 頭獎
                        self.winning[number[-3:]] = {"level": self.Reward_level[2], "number": number}

                    break

            except ValueError:
                print("\n代號為數字, 請重新選擇", style="bold red")

        for i in range(0, 8): # 顯示 獎勵等級, 獎勵條件 
            display_table.add_row(self.Reward_level[i], self.Reward_conditions[i])
        print(display_table)

        self.__Comparison_Date()

    def __call__(self):
        self.__Select_Date()

if __name__ == "__main__":
    Comparison("https://invoice.etax.nat.gov.tw/")()