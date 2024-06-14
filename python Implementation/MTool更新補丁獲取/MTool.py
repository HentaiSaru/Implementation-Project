from datetime import datetime
from lxml import etree
import requests
import os

class UpdateDetection:
    def __init__(self):
        self.url = "https://trs.mtool.app/release.php?lang=chs"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Cookie":"supportKey=00000000000000000000000000000000; from=66D39A34",
            "Cache-Control":"no-cache",
            "Host":"trs.mtool.app",
        }
        self.session = requests.Session()

        self.version = None
        self.update_patch = None
        self.full_patch = None

        self.Data_processing()

    def Get_page_data(self):
        request = self.session.get(self.url, headers=self.headers)
        return etree.HTML(request.text)
    
    def Data_processing(self):
        tree = self.Get_page_data()

        # 版本號
        title = tree.xpath("//h4")[0]
        self.version = "Version : {}{}".format(
            title.xpath("./text()")[0].split(": ")[1],
            datetime.fromtimestamp(int(title.xpath("./span/text()")[0])).strftime("%Y-%m-%d %H:%M:%S")
        )
        # 更新補丁
        self.update_patch = "{}".format(tree.xpath('//a[@class="goAfterClick"]/@href')[0])

    def Get_version(self):
        print(self.version)

    # 啟動下載更新補丁
    def Get_UP(self):
        os.system(f"start {self.update_patch}")

if __name__ == "__main__":
    check = UpdateDetection()

    check.Get_version()
    check.Get_UP()