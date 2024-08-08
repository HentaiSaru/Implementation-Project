from bs4 import BeautifulSoup
from lxml import etree
import requests
import httpx
import time

"""
Todo    適用於 Python 3.10+

?   只寫個人常用的幾種 API 調用
"""

class CarryHead:
    # 使用 navigator.userAgent 直接獲取
    Head = {
        "Google": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"},
        "Edge": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/126.0.0.0"}
    }

class Reques(CarryHead):
    def __init__(self, headers: str="Google", cookies: dict=None):
        """
        * headers: "Google" or "Edge", 兩字串擇一, 不處理例外
        * cookies: 傳入字典 cookie
        """
        self.client = httpx.Client(http2=True)
        self.session = requests.Session()
        self.headers = self.Head[headers]
        self.cookies = cookies

    # 解析要回傳的類型
    def __Parse(self, respon, type):
        Parse = {
            "none" : lambda : respon,
            "text" : lambda : respon.text,
            "content" : lambda : respon.content,
            "status" : lambda : respon.status_code,
            "tree" : lambda : etree.HTML(respon.text),
            "bf" : lambda : BeautifulSoup(respon.text, "html.parser")
        }

        try:
            return Parse.get(type)()
        except:
            return Parse.get("none")()

    def Elapsed_Time(func):
        """
        加上裝飾器 @Elapsed_Time 測試請求運行耗時
        """
        def wrapper(self, url):
            start_time = time.time()
            result = func(self, url)
            end_time = time.time()
            print(f"調用: {func.__name__}, 耗時: {end_time - start_time} 秒")
            return result
        return wrapper

    def get(self, url: str, type: str="text") -> any:
        """
        *   基本 Get 請求
        >>> [ url ]
        要請求的連結

        >>> [ type ]
        要獲取的結果類型
        ("none" / "text" / "content" / "status" / "tree" / "bf")

        "none" => 無處理
        "tree" => lxml 進行解析
        "bf" => bs4 進行解析
        """
        return self.__Parse(
            self.session.get(url, headers=self.headers, cookies=self.cookies),
            type
        )

    def http2_get(self, url: str, type: str="text") -> any:
        """
        *   支援 http2 的 Get 請求
        >>> [ url ]
        要請求的連結

        >>> [ type ]
        要獲取的結果類型
        ("none" / "text" / "content" / "status" / "tree" / "bf")

        "none" => 無處理
        "tree" => lxml 進行解析
        "bf" => bs4 進行解析
        """
        return self.__Parse(
            self.client.get(url, headers=self.headers, cookies=self.cookies),
            type
        )

    async def async_http_get(self, url: str) -> object:
        """
        *   異步 Get 請求

        >>> [ url ]
        要請求的連結

        >>> [ 使用方式 ]
        import asyncio
        async def main():
            work = [async_http_get(url) for url in date]
            results = await asyncio.gather(*work)
        asyncio.run(main())
        """
        async with httpx.AsyncClient(http2=True) as client:
            response = await client.get(url, headers=self.headers, cookies=self.cookies)
            return etree.HTML(response.text)

    async def async_get(self, url: str, session) -> object:
        """
        *   異步 Get 請求

        >>> [ url ]
        要請求的連結

        >>> [ session ]
        請求的 session 值

        >>> [ 使用方式 ]
        import aiohttp
        async def main():
            async with aiohttp.ClientSession() as session:
                work = [async_get(url, session) for url in date]
                results = await asyncio.gather(*work)
        asyncio.run(main())
        """
        async with session.get(url, headers=self.headers, cookies=self.cookies) as response:
            content = await response.text()
            return etree.HTML(content)