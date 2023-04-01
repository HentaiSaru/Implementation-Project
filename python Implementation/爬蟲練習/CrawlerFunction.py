from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from urllib.parse import unquote
from bs4 import BeautifulSoup
import requests
import random
import opencc
import time
import json
import sys
import os

# 簡繁轉換
def Converter(language):
    converter = opencc.OpenCC('s2twp.json')
    return converter.convert(language)

# 輸出保存
def SaveBox(name):
    global ListBox
    SaveBox = json.dumps(ListBox,indent=4,separators=(',', ': '),sort_keys=True,ensure_ascii=False)
    with open(f"{name}.json","w",encoding="utf-8") as f:
        f.write(SaveBox)

# 巴哈哈拉區爬文爬蟲
def RequestsGamer(URL):
    global ListBox , state
    ListBox = []
    state = False

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
            time.sleep(0.2)
            state = True

            try:
                # 取得文章的類型
                ArticleType = i.select(".b-list__summary__sort")[0].text.strip()
                # 取得文章標題
                ArticleTitle = i.select(".b-list__main__title")[0].text.strip()
                # 取得文章連結
                ArticleTitleLink = f'https://forum.gamer.com.tw/{i.select(".b-list__main__title")[0]["href"]}'

                Box = {
                    "文章版面": ArticleType,
                    "文章標題": ArticleTitle,
                    "文章連結": ArticleTitleLink,
                }
                ListBox.append(Box)

            except Exception as e:
                print("debug:{}".format(e))
                continue

            print("【{}】{}\n {}\n".format(ArticleType,ArticleTitle,ArticleTitleLink))

        print("========== Page:{}結尾 ==========\n".format(page))

# BiliBil 搜尋爬蟲
def RequestsBiliBili(Input):
    global ListBox , state
    state = False
    ListBox = []

    print("\n開始搜尋...")

    options = Options()
    options.add_argument('--headless') # 此行關閉操作窗口
    # 以下為繞過驗證爬蟲的機製
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36")
    # 隨機端口
    port = random.randint(1024, 65535)
    options.add_argument(f'--remote-debugging-port={port}')
    options.add_argument("--log-level=3") # 關閉日誌訊息(設置層級)
    options.add_argument('--start-maximized')
    options.add_argument('--disable-infobars')
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # 關閉日誌訊息
    # 開啟網頁
    driver = webdriver.Chrome(options=options)
    # 繞過檢測Js
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    # 到達首頁
    driver.get("https://www.bilibili.com/")
    # 找到輸入框
    search = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, "//input[@class='nav-search-input']")))
    # 點選
    search.click()
    # 輸入
    search.send_keys(Input)
    # 送出
    search.send_keys(Keys.RETURN)

    # 切換分頁(B站的搜尋會開新的分頁)
    driver.switch_to.window(driver.window_handles[-1])
    # 獲取新分頁的網址
    Newurl = driver.current_url

    """ selenium 的解析的爬取方式
        # 開始爬取資料
        Content = driver.page_source.encode('utf-8').strip()
        html = BeautifulSoup(Content,'html.parser')
        # 取得資料
        finalPage = html.select('button.vui_button.vui_button--no-transition.vui_pagenation--btn.vui_pagenation--btn-num')[-1]
        VideoTitle = html.find_all('h3')
        VideoTime = html.select("span.bili-video-card__info--date")
        VideoURL = html.select("div.bili-video-card__info--right")
        time.sleep(3)
        os.system("cls")
        for i in range(len(VideoTitle)):
            Tag = VideoURL[i].find("a")
            href = Tag['href']
            Vtime = VideoTime[i].text
            Vtitle = VideoTitle[i].text
            print("{}\n{}\n{}\n".format(Vtime,Vtitle,"https:"+href))
    """
    os.system("cls")
    def UrlPattern(URL):
        # 大坑 很重要!! 當網址含有中文,在複製時會被轉譯,這邊是將他轉回去
        NewURL = unquote(URL)
        # 用於判斷 BiliBil 影片網址的後綴,並將其去除
        if NewURL.find("/?") != -1:
            NewURL = NewURL.split("/?")[0]
        return NewURL

    # === 換回 requests 爬取方式 ===
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
    }

    # 取得新頁面的URL並轉換格式
    URL = UrlPattern(Newurl)
    Information = requests.get(URL, headers=header)
    html = BeautifulSoup(Information.text, "html.parser")

    # 取得最後一頁
    finalPage = html.select('button.vui_button.vui_button--no-transition.vui_pagenation--btn.vui_pagenation--btn-num')[-1]
    # 從第一頁開始 ~ finalPage
    current_page = 1
    while current_page <= int(finalPage.text):
        if current_page == 1: # 如果是第一頁,用預設的
            Information = requests.get(Newurl, headers=header)
            html = BeautifulSoup(Information.text, "html.parser")
            List = html.select("div.bili-video-card")
        else: # 之後的頁數
            # 滾動頁面
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            # 找到下一頁按鈕
            Next = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "//button[@class='vui_button vui_pagenation--btn vui_pagenation--btn-side' and text()='下一页']")))
            time.sleep(0.5)
            # 按下按鈕
            Next.click()
            # 獲取新的網址格式
            Newurl = UrlPattern(driver.current_url)
            Information = requests.get(Newurl, headers=header)
            htmlNew = BeautifulSoup(driver.page_source, "html.parser") 
            #driver.execute_script("return document.documentElement.outerHTML")JavaScript代碼在瀏覽器中執行並返回當前頁面的完整HTML源代碼
            #driver.page_source 也是另一種返回當前頁面的完整HTML源代碼的方法
            List = htmlNew.select("div.bili-video-card")

        # 就耐心等一下網頁載入
        time.sleep(2.5)

        # 開始爬取頁面
        for i in List:
            try:
                state = True
                VideoTitle = i.select("h3")[0].text.strip()
                VideoTime = i.select("span.bili-video-card__info--date")[0].text.strip()
                VideoURL = i.select("div.bili-video-card__info--right")[0].find("a")["href"]

                if VideoTitle not in ListBox or VideoURL not in ListBox:
                    Box ={
                        "影片日期":Converter(VideoTime).split("· ")[1],
                        "影片標題":Converter(VideoTitle),
                        "影片連結":'https:'+VideoURL
                    }
                    ListBox.append(Box)
                print("{}\n{}\n{}\n".format(VideoTime,VideoTitle,"https:"+VideoURL))
            except Exception as e:
                print("debug:{}".format(e))
                continue
        print("========== Page:{}結尾 ==========\n".format(current_page))
        current_page += 1 # 每爬完一頁就+1

    driver.quit() # 關閉端口避免出錯 


RequestsGamer("https://forum.gamer.com.tw/B.php?page=235&bsn=60608")

#RequestsBiliBili(input("輸入你的查詢: "))

global state
if state:
    # 輸出成Json
    SaveBox(input("輸入輸出的文件名稱: "))

input("\n運行完畢...")