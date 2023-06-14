from urllib.parse import *
import re
class ogcode:
    def __init__(self):
        self.github = r"^https:\/\/github\.com\/.*"
        self.domain = "https://raw.githubusercontent.com/"

    def convert(self,url):
        if re.match(self.github,url):
            convert = url.replace("https://github.com/",self.domain)
            convert = re.sub(r"/blob", "", convert)
            print(f'"{unquote(convert)}"')
        else:
            print("錯誤的網址")