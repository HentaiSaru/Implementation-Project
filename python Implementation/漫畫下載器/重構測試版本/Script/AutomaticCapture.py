import pyperclip
import threading
import keyboard
import queue
import time
import os
import re

class AutomaticCapture:
    def __init__(self):
        self.UrlFormat = r'^(?:http|ftp)s?://'

        self.initial_url_format = None
        self.intercept_delay = None

        self.clipboard_cache = None
        self.download_list = set()
        self.queue = queue.Queue()

        self.generate_type = False
        self.detection = True
        self.count = 0

    def __trigger(self):
        print("複製網址後自動擷取(Alt+S 開始下載):")
        clipboard = threading.Thread(target=self.__Read_clipboard)
        command = threading.Thread(target=self.__Download_command)

        clipboard.start()
        command.start()

        command.join()
        clipboard.join()
        
    def __generate_trigger(self):
        print("自動監聽剪貼簿觸發下載(只能手動停止程式):")
        self.generate_type = True
        threading.Thread(target=self.__Read_clipboard).start()

    def __Read_clipboard(self):
        pyperclip.copy('')

        while self.detection:
            clipboard = pyperclip.paste()
            
            if clipboard != self.clipboard_cache and re.match(self.initial_url_format , clipboard):
                self.count += 1
                print(f"擷取網址 [{self.count}] : {clipboard}")
                self.download_list.add(clipboard)
                self.clipboard_cache = clipboard
                
                if self.generate_type:
                    self.queue.put(clipboard)

            time.sleep(self.intercept_delay)

    def __Download_command(self):
        keyboard.wait("alt+s")
        self.detection = False

    def settings(self, domainName:str, delay=0.05):
        try:
            if re.match(self.UrlFormat , domainName):
                self.initial_url_format = r"{}.*".format(domainName)
                self.intercept_delay = delay
            else:
                raise Exception()
        except:
            print("錯誤的網址格式")

    # 以list回傳所有擷取的網址
    def GetList(self):
        if self.initial_url_format != None:
            self.__trigger()

            if len(self.download_list) > 0:
                os.system("cls")
                return list(self.download_list)
            else:
                return None
        else:
            print("請先使用 settings(domainName) 設置域名")

    # 只會回傳一條網址 , 擷取多條就只回傳第一條
    def GetLink(self):
        if self.initial_url_format != None:
            self.__trigger()

            if len(self.download_list) > 0:
                os.system("cls")
                return list(self.download_list)[0]
            else:
                return None
        else:
            print("請先使用 settings(domainName) 設置域名")

    # 以生成器的方式回傳
    def GetBuilder(self):
        if self.initial_url_format != None:
            self.__trigger()

            if len(self.download_list) > 0:
                os.system("cls")
                for link in list(self.download_list):
                    yield link
            else:
                return None
        else:
            print("請先使用 settings(domainName) 設置域名")
            
    # 特別的擷取方法
    def Unlimited(self):
        """
        這是一個無限擷取的函數 , 沒有快捷停止 , 只能手動中止程式
        * 使用方法 :
        * 使用一個迴圈接受此方法的回傳參數 , 並進行後續的處理
        """
        self.__generate_trigger()
        while True:
            if not self.queue.empty():
                url = self.queue.get()
                yield url

AutoCapture = AutomaticCapture()