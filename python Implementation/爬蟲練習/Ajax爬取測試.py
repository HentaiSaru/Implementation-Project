from concurrent.futures import *
from datetime import datetime
from lxml import etree
from tqdm import tqdm
import subprocess
import requests
import aiohttp
import asyncio
import random
import shutil
import json
import time
import re
import os

def DomainName():
    return "https://ani.gamer.com.tw/"

def CookiesRead():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    ReadCookie = {}

    with open("Cookies.json" , "r") as file:
        cookies = json.loads(file.read())

    for cookie in cookies:
        name = cookie['name']
        value = cookie["value"]
        ReadCookie[name] = value

    return ReadCookie

class Animation:
    def __init__(self):
        self.session = requests.Session()
        self.cookies = CookiesRead()
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'Referer': f'{DomainName()}',
            'origin': f'{DomainName()}',
        }

        self.ID = ""
        self.Quality = ""

        self.RandomBox = [[97,122],[48,57]]
        self.merge = ""

        self.support = r'^' + re.escape(DomainName()) + r'animeVideo\.php\?sn=\d+$'
        self.episodes = r'"\?sn=(\d{5})"'
        self.Ad_time = re.compile(r"php\?id=([0-9]{6})")

        self.title_list = []
        self.data_list = []

        self.download_list = {}

    # 隨機字串
    def Random_string(self,scope):
        for _ in range(scope):
            string = self.RandomBox[random.randint(0,1)]
            self.merge += chr(random.randint(string[0],string[1]))
        return self.merge
    
    # 下載選擇
    def download_select(self):
        print("全集下載 [0]")
        choose = int(input("\n選擇下載集數 (代號) : "))
        print("")
        for index in range(len(self.data_list)):

            if choose == 0:
                self.download_list[self.title_list[index]] = self.data_list[index]
            elif choose <= len(self.data_list) and choose >= 0:
                self.download_list[self.title_list[choose-1]] = self.data_list[choose-1]
                break
            else:
                print("錯誤的代號")
                os._exit(1)

    # 異步獲取數據
    async def Asyn_get_data(self,session,url):
        async with session.get(url, headers=self.headers, cookies=self.cookies) as response:
            text = await response.text()
            return etree.fromstring(text,etree.HTMLParser()) , text
    
    # 普通獲取
    def Get_data(self,url):
        response = self.session.get(url, headers=self.headers, cookies=self.cookies)
        return response

    # 獲取章節數
    async def Get_episodes(self,session,url):
        tree , text = await self.Asyn_get_data(session,url)
        return re.findall(self.episodes, text)
    
    # 獲取下載數據
    async def Get_download_data(self,session,url):
        tree , text = await self.Asyn_get_data(session,f"{DomainName()}/animeVideo.php?sn={url}")
        return tree.xpath("//div[@class='anime_name']/h1/text()")[0] , url
    
    # 獲取授權
    async def get_authorization(self,session,url):
        tree , text = await self.Asyn_get_data(session,url)
        return text

    def animation_data_request(self,url: str, quality: str="720"):
        self.Quality = quality

        async def Trigger():
            work = []
            async with aiohttp.ClientSession() as session:
                data = await self.Get_episodes(session,url)
                tree , text = await self.Asyn_get_data(session,"https://ani.gamer.com.tw/ajax/getdeviceid.php?id=")
                self.ID = json.loads(text)["deviceid"]

                for link in data: 
                    work.append(asyncio.create_task(self.Get_download_data(session,link)))

                results = await asyncio.gather(*work)

                for data in results:
                    print(data[0])
                    self.title_list.append(data[0])
                    self.data_list.append(data[1])

                self.download_select()

                for name , link in self.download_list.items():
                    authoriz = await self.get_authorization(session,f"https://ani.gamer.com.tw/ajax/token.php?adID=undefined&sn={link}&device={self.ID}&hash={self.Random_string(12)}")

                    if(authoriz.find("error")!=-1):
                        print("授權失敗")
                        return
                    
                    self.Ad_processing(name,link)

        asyncio.run(Trigger())
    
    def Ad_processing(self,name,link):
        # 取得廣告數據
        response = self.Get_data(f"https://i2.bahamut.com.tw/JS/ad/animeVideo2.js?v={datetime.now().strftime('%Y%m%d%H')}")
        Match = self.Ad_time.findall(response.text)
        Ad = Match[0].replace("php?id=","")

        self.Get_data(f"https://ani.gamer.com.tw/ajax/videoCastcishu.php?sn={link}&s={Ad}")
        for i in range(30):
            print(f"\r將於{30-i}秒後跳過廣告... ", end='', flush=True)
            time.sleep(1)
        print("\n")
        self.Get_data(f"https://ani.gamer.com.tw/ajax/videoCastcishu.php?sn={link}&s={Ad}&ad=end")

        # 呼叫 m3u8 處理
        self.M3u8_processing(name,link)

    def M3u8_processing(self,name,link):
        response = self.Get_data(f"https://ani.gamer.com.tw/ajax/videoStart.php?sn={link}")
        response = self.Get_data(f"https://ani.gamer.com.tw/ajax/m3u8.php?sn={link}&device={self.ID}")
        m3u8 = json.loads(response.text)["src"]
        
        Res = " "
        response = self.Get_data(m3u8)
        streaming = response.text.split('\n')
        print(f"streaming:{streaming}")
        input()
        for stream in streaming:
            if stream.startswith("#EXT-X-STREAM-INF"):
                if self.Quality == stream.split('x')[1].strip():
                    Next = streaming[streaming.index(stream) + 1]
                    Res = Next.split("?")[0].strip()
                    break
        
        if Res == " ":
            print("M3u8解析失敗")
            return
        
        m3u8 = m3u8[:m3u8.find("playlist_basic.m3u8")] + Res
        TempName = Res[Res.rindex('/') + 1:]
        TempFile = f"%temp%\\{TempName}"

        response = self.Get_data(m3u8)
        with open(TempFile, "wb") as f:
            f.write(response.content)

        # 處理獲取數據
        stream_chunking = re.findall(r'.+\.ts',response.text)
        decrypt_key = re.search(r'URI="([^"]+)"', response.text).group(1)
        m3u8 = m3u8[:m3u8.rfind('/')+1]

        # 保存Key
        self.Download(m3u8+decrypt_key, TempFile.replace('chunklist','key')+'key')

        # 保存塊
        with ThreadPoolExecutor(max_workers=500) as executor:
            for chunking in tqdm(stream_chunking , desc=name, colour="#9575DE"):
                executor.submit(self.Download , m3u8+chunking , f"%temp%\\{chunking}")

        ffmpeg_path = "R:/test/ffmpeg.exe"
        input_file = (TempFile).replace('\\','/')
        output_file = "R:/測試下載" +'/'+ name + ".mp4"
        self.Merge_save(ffmpeg_path, input_file, output_file, TempFile)

    def Download(self, request, path):
        response = self.Get_data(request)
        with open(path , "wb") as f:
            f.write(response)

    def Merge_save(self, ffmpeg_path, input_file, output_file, TempFile):
        command = [
            ffmpeg_path,
            "-allowed_extensions",
            "ALL",
            "-y",
            "-i",
            input_file,
            "-c",
            "copy",
            output_file
        ]
        
        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=input_file[:input_file.rfind("/")])
        process.wait()
        if process.poll() is not None:
            process.terminate()

        shutil.rmtree(TempFile)
        

if __name__ == "__main__":
    baha = Animation()
    baha.animation_data_request("")