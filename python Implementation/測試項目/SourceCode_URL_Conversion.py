import re
class ogcode:
    def __init__(self):
        self.github = r"^https:\/\/github\.com\/.*"
        self.domain = "https://raw.githubusercontent.com/"

    def convert(self,url):
        if re.match(self.github,url):
            convert = url.replace("https://github.com/",self.domain)
            convert = re.sub(r"/blob", "", convert)
            return convert
        else:
            return "錯誤的網址"