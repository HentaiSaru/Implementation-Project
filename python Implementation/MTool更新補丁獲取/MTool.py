from lxml import etree
import requests
import os

class UpdateDetection:
    def __init__(self):
        self.url = "https://trs.mtool.app/release.php?lang=chs"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Cookie":"7F2210D0_inc=1; supportKey=00000000000000000000000000000000; from=7F2210D0",
            "Host":"trs.mtool.app",
            "Referer":"https://afdian.net/",
        }
        self.session = requests.Session()

        self.version = None
        self.update_patch = None
        self.full_patch = None

        self.Data_processing()

    def Get_page_data(self):
        request = self.session.get(self.url, headers=self.headers)
        return etree.fromstring(request.content, etree.HTMLParser())
    
    def Data_processing(self):
        tree = self.Get_page_data()
        # 版本號
        self.version = tree.xpath("//h4/text()")[1].split(": ")[1].strip()
        # 更新補丁
        self.update_patch = f"https://trs.mtool.app/{tree.xpath('//p/a')[2].get('href')}"
        # 完整補丁
        self.full_patch = f"https://trs.mtool.app/{tree.xpath('//p/a')[3].get('href')}"

    def Get_version(self):
        print(self.version)

    def Get_UP(self):
        os.system(f"start {self.update_patch}")

    def Get_FP(self):
        os.system(f"start {self.full_patch}")

if __name__ == "__main__":
    check = UpdateDetection()

    # 獲取更新連結
    check.Get_UP()

    # 獲取完整連結 (有BUG , 確定取得是完整下載連結 , 但實際上只下載更新補丁)
    # check.Get_FP()