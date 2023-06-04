from Search_Settings import R_get
from urllib.parse import unquote
from lxml import etree

class wiki_list:
    def __init__(self):
        self.url = "https://zh.wikipedia.org/zh-tw/各年日本動畫列表"
        self.year_list_information = {}

    def UrlPattern(self,URL):
        NewURL = f"https://zh.wikipedia.org{unquote(URL)}"
        return NewURL

    def Data_Request(self):
        list_data = R_get.data(self.url)
        tree = etree.fromstring(list_data.content, etree.HTMLParser())
        
        for data in tree.xpath("//div[@class='hlist']/ul/li/a"):
            self.year_list_information[data.text] = self.UrlPattern(data.get("href"))

    def Get_List(self):
        self.Data_Request()
        return self.year_list_information

L_wiki = wiki_list()