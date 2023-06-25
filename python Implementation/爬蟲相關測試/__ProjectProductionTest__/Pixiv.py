from bs4 import BeautifulSoup
import requests

class request:
    
    def __init__(self,url,header,data):

        self.url = url
        self.header = header
        self.data = data

class landing_page(request):

    def __init__(self):

        url = "https://accounts.pixiv.net/login"

        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "sec-fetch-mode": "no-cors",
            "referer": "https://accounts.pixiv.net/",
        }

        super().__init__(url, header, None)

class login(request):

    def __init__(self):

        url = "https://accounts.pixiv.net/login?lang=zh_tw"

        header = {
            "authority": "accounts.pixiv.net",
            "method": "POST",
            "path": "/ajax/login?lang=zh_tw",
            "scheme": "https",
            "accept": "application/json",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://accounts.pixiv.net",
            "pragma": "no-cache",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        }

        data = {
            "login_id": "#",
            "password": "#",
        }

        super().__init__(url, header, data)


landing_page = landing_page()
print(landing_page.url,landing_page.header)

def crawl():
    session = requests.Session()
    url , Header = landing_page()
    
    session.get(url,headers=Header)

    url , Header , data = login()

    OpenPage = session.post(url,headers=Header,data=data)

    bs4 = BeautifulSoup(OpenPage.content,"lxml")


    print(bs4)
    