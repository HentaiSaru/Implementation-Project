from bs4 import BeautifulSoup
from lxml import etree
import requests

class default:
    def __init__(self):
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
        self.request = requests.Session()
    
    def data(self,url):
        return self.request.get(url,headers=self.headers)
    
    def get_tree(self,url):
        return etree.fromstring(self.data(url).content, etree.HTMLParser())

    def get_bfs(self,url):
        return BeautifulSoup(self.data(url).text,"html.parser")
    
ask_s = default()