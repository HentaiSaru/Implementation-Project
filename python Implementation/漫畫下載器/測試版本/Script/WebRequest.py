from bs4 import BeautifulSoup
from lxml import etree
import requests

"""
Todo    適用於 Python 3.10+

?   只寫個人常用的幾種 API 調用
"""

class CarryHead:
    Head = {
        "Google": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"},
        "Edge": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47"}
    }

class Reques(CarryHead):
    def __init__(self, headers: str="Google", cookies: dict=None):
        """
        * headers: "Google" or "Edge", 兩字串擇一, 不處理例外
        * cookies: 傳入字典 cookie
        """
        self.session = requests.Session()
        self.headers = self.Head[headers]
        self.cookies = cookies
    
    # 解析要回傳的類型
    def __Parse(self, respon, type):
        match type:
            case "text":
                return respon.text
            case "content":
                return respon.content
            case "status":
                return respon.status_code
            case "tree":
                return etree.HTML(respon.text)
            case "bf":
                return BeautifulSoup(respon.text, "html.parser")

    def get(self, url: str, result: str="text"):
        """
        *   基本 Get 請求
        >>> [ url ]
        要請求的連結
        
        >>> [ result ]
        要獲取的結果類型
        ("text" / "content" / "status" / "tree" / "bf")
        """
        return self.__Parse(
            self.session.get(url, headers=self.headers, cookies=self.cookies),
            result
        )

    async def async_get(self, url: str, session):
        """
        *   異步 Get 請求

        >>> [ url ]
        要請求的連結

        >>> [ session ]
        請求的 session 值

        -> 目前只回傳 tree 的 Dom 文本
        """
        async with session.get(url, headers=self.headers, cookies=self.cookies) as response:
            content = await response.text()
            return etree.HTML(content)