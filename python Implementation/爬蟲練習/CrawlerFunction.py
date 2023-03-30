from tkinter import messagebox
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import chardet
import time
import re
import os

def RequestsUse(URL):
    os.system("color 9f")

    if URL.find("page=") == -1:
        URL = "{}?{}".format(URL.split("?")[0],"page=1&"+URL.split("?")[1]).replace("A","B")

    # 模擬 headers 資訊繞過反爬蟲
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
    }

    # 顯示格式設置
    params = {}

    # 載入 headers 資訊
    Information = requests.get(URL,headers=header,params=params)
    if Information.status_code == 400:print('錯誤的要求')
    elif Information.status_code == 404:print('找不到網頁')
    elif Information.status_code == 500:print('伺服器錯誤')
    elif Information.status_code == 504:print('伺服器沒有回應')

    """取得所有 該標籤的內容 Content = doc.find_all("div")"""

    # html.parser解析 其他解析器(html5lib)
    Html = BeautifulSoup(Information.text, "html.parser")
    # 取得完整的頁數
    finalList = Html.select(".BH-pagebtnA")[0].find_all('a')[-1].text

    # 取得給予的網址頁數
    URLPage = URL.split("page=")[1].split("&")[0]

    # 從1+到finalList的頁數
    for page in range(int(URLPage),int(finalList)+1):

        # 將URL轉換為新格式
        UrlNew = "{}page={}&{}".format(URL.split("page=")[0],f"{URLPage}",URL.split("&")[1])

        InformationNew = requests.get(UrlNew,headers=header)

        HtmlNew = BeautifulSoup(InformationNew.text, "html.parser")

        List = HtmlNew.select(".b-list__row.b-list-item.b-imglist-item")

        for i in List:
            time.sleep(0.3)

            try:
                # 取得文章的類型
                ArticleType = i.select(".b-list__summary__sort")[0].text.strip()
                # 取得文章標題
                ArticleTitle = i.select(".b-list__main__title")[0].text.strip()
                # 取得文章連結
                ArticleTitleLink = f'https://forum.gamer.com.tw/{i.select(".b-list__main__title")[0]["href"]}'
            except:continue

            print("【{}】{}\n {}\n".format(ArticleType,ArticleTitle,ArticleTitleLink))

        print("========== Page:{}結尾 ==========\n".format(page))

def SeleniumUse():

    Url = "https://www.gamer.com.tw/"

    # 模擬 headers
    UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    opt = webdriver.ChromeOptions()

    # 載入 headers 資訊
    opt.add_argument("--user-agent=%s" % UserAgent)
    driver = webdriver.Chrome('./chromedriver', options=opt)
    driver.get(Url)

RequestsUse("https://forum.gamer.com.tw/B.php?page=24&bsn=30861")