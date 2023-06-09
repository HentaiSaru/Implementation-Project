from datetime import datetime
from lxml import etree
import requests
import re
import os

class AutomaticDetection:
    def __init__(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
        self.request = requests.Session()

        self.NameFormat = r"【(.*?)】"
        self.TimestampFormat = r"\s+"

        self.timestamp = {}
        self.outputbox = []
        self.__Read_timestamp()

    def __Read_timestamp(self):
        try:
            with open("timestamp","r" , encoding="utf-8") as f:
                for data in f.readlines():
                    stamp = re.sub(self.TimestampFormat,"",data).split("Latest:")
                    self.timestamp[stamp[0]] = stamp[1]
        except:
            with open("timestamp","w", encoding="utf-8") as f:
                f.write(" ")

    def Output_timestamp(self):
        if len(self.outputbox) > 0:
            with open("timestamp","w", encoding="utf-8") as f:
                for index , date in enumerate(self.outputbox):
                    if index == len(self.outputbox) - 1:
                        f.write(f"{date}")
                    else:
                        f.write(f"{date}\n")
            self.outputbox.clear()

    def __Time_judgment(self,data,url):
        handle = data.split(" Latest: ")
        try:
            timestamp = datetime.strptime(self.timestamp[handle[0]], "%Y-%m-%d")
            lastdate = datetime.strptime(handle[1], "%Y-%m-%d")

            if lastdate > timestamp:
                os.system(f"start {url}")

            self.outputbox.append(data)
        except:
            self.outputbox.append(data)

    def __Get_information(self,url):
        try:
            request = self.request.get(url,headers=self.headers)
            return etree.fromstring(request.content , etree.HTMLParser())
        except requests.exceptions.ConnectionError:
            os._exit(0)

    def __Information_processing(self,url):
        tree = self.__Get_information(url)
        Name = re.search(self.NameFormat , tree.xpath("//h1[@class='entry-title']/text()")[0])
        Latest_date = tree.xpath("//time[@class='entry-date published updated']/text()")
        return f"【{Name.group(1)}】 Latest: {Latest_date[0]}"

    def Detection(self,url):
        self.__Time_judgment(self.__Information_processing(url) , url)

auto = AutomaticDetection()