import pyperclip
import threading
import keyboard
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

        self.download_trigger = False
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

    def __Read_clipboard(self):
        pyperclip.copy('')

        while self.detection:
            clipboard = pyperclip.paste()
            
            if self.download_trigger:
                pass
            elif clipboard != self.clipboard_cache and re.match(self.initial_url_format , clipboard):
                self.count += 1
                print(f"擷取網址 [{self.count}] : {clipboard}")
                self.download_list.add(clipboard)
                self.clipboard_cache = clipboard

            time.sleep(self.intercept_delay)

    def __Download_command(self):
        while self.detection:
            if keyboard.is_pressed("alt+s"):
                self.download_trigger = True
                self.detection = False
                while keyboard.is_pressed("alt+s"):
                    pass
            time.sleep(0.05)

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

AutoCapture = AutomaticCapture()