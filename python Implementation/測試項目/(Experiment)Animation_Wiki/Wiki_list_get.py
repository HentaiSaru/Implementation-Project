from Search_Settings import ask_s
from urllib.parse import unquote

class wiki_list:
    def __init__(self):
        self.url = "https://zh.wikipedia.org/zh-tw/各年日本動畫列表"
        self.year_list_information = {}

    def UrlPattern(self,URL):
        NewURL = f"https://zh.wikipedia.org{unquote(URL)}"
        return NewURL

    def Data_Request(self):
        tree = ask_s.get_tree(self.url)
        
        for data in tree.xpath("//div[@class='hlist']/ul/li/a"):
            self.year_list_information[data.text] = self.UrlPattern(data.get("href"))

    def Get_List(self):
        self.Data_Request()
        return self.year_list_information

wiki_l = wiki_list()