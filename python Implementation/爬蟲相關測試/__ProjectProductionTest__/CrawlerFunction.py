from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from urllib.parse import unquote
from selenium import webdriver
from bs4 import BeautifulSoup
import threading
import requests
import datetime
import random
import opencc
import time
import json
import csv
import sys
import re
import os

""" ---------- 功能API ---------- """
# 清除非正常關閉時遺留的垃圾
def TrashRemoval():
    os.system('for /d %d in ("C:\Program Files\chrome_BITS*") do rd /s /q "%d" >nul 2>&1')
    os.system('for /d %d in ("C:\Program Files (x86)\scoped_dir*") do rd /s /q "%d" >nul 2>&1')

# 網址含有中文時的轉換
def UrlPattern(URL):
        # 很重要!! 當網址含有中文,在複製時會被轉譯,這邊是將他轉回去
        NewURL = unquote(URL)

        # 用於判斷 BiliBil 影片網址的後綴,並將其去除
        if NewURL.find("/?") != -1:
            NewURL = NewURL.split("/?")[0]
        return NewURL

# 簡繁轉換
def Converter(language):
    converter = opencc.OpenCC('s2twp.json')
    return converter.convert(language)

# 輸出保存
def SaveBox(search):
    global ListBox , state
    os.system("cls")

    def SaveJson(search):
        name = input("輸入保存的文件名稱: ")
        Adjustment_dict = {search:[]}
        DividerStyle = ["»","≈","…"]
        Style = random.choice(DividerStyle)

        for data in ListBox:
            for key , value in data.items():
                if value == list(data.values())[-1]:
                    value = " " + value
                NewData = f"【 {key} 】 {value}"
                Adjustment_dict[search].append(NewData)
            Adjustment_dict[search].append(f" {Style*70} ")

        SaveBox = json.dumps(Adjustment_dict,indent=4,separators=(',',':'),ensure_ascii=False)
        directory = os.path.dirname(os.path.abspath(sys.argv[0]))
        filename = f"{name}.json"
        fileoutput = os.path.join(directory, filename)

        with open(fileoutput,"w",encoding="utf-8") as f:
            f.write(SaveBox)

        print("輸出完畢...")

    def SaveCsv(search):
        name = input("輸入保存的文件名稱: ")
        rows = [f"【{search}】"]

        for data in ListBox:
            merge = ""
            for value in data.values():
                merge += f"{value},"

            merge = "{}, https{}".format(merge.split(",https")[0],merge.split(",https")[1]).rstrip(",")
            rows.append(merge)

        directory = os.path.dirname(os.path.abspath(sys.argv[0]))
        filename = f"{name}.csv"
        fileoutput = os.path.join(directory, filename)

        with open(fileoutput, 'w', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile,quoting=csv.QUOTE_NONE, escapechar=' ')
            for row in rows:
                writer.writerow([row])
        print("輸出完畢...")


    if state:
        save_options = ["【1】保存為JSON","【2】保存為CSV","【0】不保存"]

        for save in save_options:
            print(save)

        while True:
            try:
                options =int(input("\n輸入數字選擇: "))
                if options == 1:
                    os.system("cls")
                    print(save_options[0])
                    SaveJson(search)
                    break
                elif options == 2:
                    os.system("cls")
                    print(save_options[1])
                    SaveCsv(search)
                    break
                elif options == 0:
                    os.system("cls")
                    print(save_options[2])
                    break
                else:print("沒有此選項")
            except:
                print("錯誤的輸入")

# 功能選項
def add():
    options = Options()
    options.add_argument('--headless') # 此行關閉操作窗口
    options.add_argument("user-data-dir=R:/ChromTest")
    options.add_argument('--disk-cache-dir=R:/caching')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36")
    options.add_argument(f'--remote-debugging-port={random.randint(1024,65535)}') # 隨機遠程端口
    options.add_argument('--incognito')
    options.add_argument("--log-level=3") # 關閉日誌訊息(設置層級)
    options.add_argument('--disable-logging')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-translate')
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # 關閉日誌訊息
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    return options

""" ---------- 主要程式運行 ---------- """
# 針對巴哈非普通遊戲版 的搜尋設置
class Gamerconversion:

    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    }
    
    def GNN(page):
        global ListBox , state
        ListBox = []
        state = True

        # 取得當前的年月
        now = datetime.datetime.now()
        year = now.year
        month = now.month

        try:
            current_page = 1
            while current_page <= int(page):
                Information = requests.get(f"https://gnn.gamer.com.tw/?yy={year}&mm={month}",headers=Gamerconversion.header)
                Html = BeautifulSoup(Information.text, "html.parser")
                articletitle = Html.find_all('h1', class_="GN-lbox2D")

                for i in range(len(articletitle)):
                    title = articletitle[i].find("a").text
                    url = "https:{}".format(articletitle[i].find("a")['href'])

                    print(title)
                    print(url+"\n")

                    Box = {
                        "新聞標題": title,
                        "新聞連結": url,
                    }
                    time.sleep(0.05)
                    ListBox.append(Box)

                print("========== {}年 {}月 結尾 ==========\n".format(year,month))
                current_page += 1
                month -= 1

                if month < 1:
                    month = 12
                    year -= 1

                time.sleep(2)
        except:pass

    def Outside():
        # 場外選擇也是由Js動態生成
        driver = webdriver.Chrome(options=add())
        driver.get("https://forum.gamer.com.tw/index.php?c=95")
        driver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')

        # 經過計算翻三次剛好可以加載全部
        for i in range(3):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(1)

        Html = BeautifulSoup(driver.page_source, "html.parser")
        Title = Html.find_all("div", class_="forum_list_title")
        os.system("cls")

        linkbox = []
        for i in range(len(Title)):
            print(f'【 {i+1} 】{Title[i].find("a").text}')
            linkbox.append("https://forum.gamer.com.tw/{}".format(Title[i].find("a").get("href")))
        driver.quit() 
        select = eval(input("\n請選擇您要進入的版面(編號): "))
        print("\n開始搜尋...")
        return linkbox[select-1]

# 巴哈哈拉區爬文爬蟲
def RequestsGamer(search,pages):
    global ListBox , state
    ListBox = []
    state = False
    
    print("\n開始搜尋... (搜尋速度取決於你的網速)")

    try:
        if search.find("場外") != -1:
            URL = Gamerconversion.Outside()
            os.system("cls")
        else:
            search_convert = f"https://search.gamer.com.tw/?q={UrlPattern(search)}#gsc.tab=0&gsc.q={UrlPattern(search)}&gsc.page=1"
            # 因為是由Js動態生成的,只能用自動化操作取得
            driver = webdriver.Chrome(options=add())
            driver.get(search_convert)
            driver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')
            Page = BeautifulSoup(driver.page_source, 'html.parser')
            URL = Page.find('a', class_='gs-title').get('data-ctorig')
            os.system("cls")
            driver.quit()
        
        # 只供哈拉區版面的轉換
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
        session = requests.Session()
        Information = session.get(URL,headers=header,params=params)
        if Information.status_code == 400:print('錯誤的要求')
        elif Information.status_code == 404:print('找不到網頁')
        elif Information.status_code == 500:print('伺服器錯誤')
        elif Information.status_code == 504:print('伺服器沒有回應')

        """取得所有 該標籤的內容 Content = doc.find_all("div")"""

        # html.parser解析 其他解析器(html5lib)
        Html = BeautifulSoup(Information.text, "html.parser")

        # 取得完整的頁數
        finalList = int(Html.select(".BH-pagebtnA")[0].find_all('a')[-1].text)

        # 可由輸入的頁數作為爬取數量,但要確保小於最大的頁數量
        if pages != 0:
            if pages < finalList:finalList = pages

        # 從1+到finalList的頁數
        for page in range(1,int(finalList)+1):

            # 將URL轉換為新格式
            UrlNew = "{}page={}&{}".format(URL.split("page=")[0],f"{page}",URL.split("&")[1])
            InformationNew = session.get(UrlNew,headers=header)
            HtmlNew = BeautifulSoup(InformationNew.text, "html.parser")
            List = HtmlNew.select(".b-list__row.b-list-item.b-imglist-item")

            for i in List:
                time.sleep(0.05)
                state = True

                try:
                    # 取得文章的類型
                    ArticleType = i.select(".b-list__summary__sort")[0].text.strip()
                    # 取得文章標題
                    ArticleTitle = i.select(".b-list__main__title")[0].text.strip()
                    # 取得文章連結
                    ArticleTitleLink = f'https://forum.gamer.com.tw/{i.select(".b-list__main__title")[0]["href"]}'

                    Box = {
                        "文章版面": f"【{ArticleType}】",
                        "文章標題": ArticleTitle,
                        "文章連結": ArticleTitleLink,
                    }
                    ListBox.append(Box)

                except Exception as e:
                    #print("debug:{}".format(e))
                    continue

                print("【{}】{}\n {}\n".format(ArticleType,ArticleTitle,ArticleTitleLink))

            print("========== Page:{}結尾 ==========\n".format(page))
            time.sleep(0.5)
        InformationNew.close()
    except Exception as e:
        print(e)
        if search.upper()  == "GNN":
            Gamerconversion.GNN(pages)
    SaveBox(search)

# BiliBil 搜尋爬蟲
def RequestsBiliBili(Input,pages):
    global ListBox , state
    state = False
    ListBox = []

    print("\n開始搜尋... (搜尋速度取決於你的網速)")

    driver = webdriver.Chrome(options=add()) # 開啟網頁
    driver.get("https://www.bilibili.com/") # 到達首頁
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") # 繞過檢測Js
    search = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, "//input[@class='nav-search-input']"))) # 找到輸入框
    search.click() # 點選
    search.send_keys(Input) # 輸入
    search.send_keys(Keys.RETURN) # 送出

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
    finalPage = int(html.select('button.vui_button.vui_button--no-transition.vui_pagenation--btn.vui_pagenation--btn-num')[-1].text)
    
    if pages != 0:
        if pages < finalPage:finalPage = pages

    # 從第一頁開始 ~ finalPage
    current_page = 1
    while current_page <= finalPage:
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
                VideoTitle = i.select("h3.bili-video-card__info--tit")[0].text.strip()
                VideoTime = i.select("span.bili-video-card__info--date")[0].text.strip()
                VideoURL = i.select("div.bili-video-card__info--right")[0].find("a")["href"]

                if VideoTitle not in ListBox or VideoURL not in ListBox:
                    Box ={
                        "影片日期":f'【{Converter(VideoTime).split("· ")[1]}】',
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
    SaveBox(Input)
    driver.quit() # 關閉端口避免出錯 

search = input("(盡量打完整名稱不然搜不到)\n請輸入查詢: ")
pages = eval(input("輸入要搜尋的頁數: "))
threading.Thread(target=RequestsGamer,args=(search,pages)).start()
# threading.Thread(target=RequestsBiliBili,args=(search,pages)).start()

TrashRemoval()
"""
作業中..

創建關於動畫瘋的搜索

"""