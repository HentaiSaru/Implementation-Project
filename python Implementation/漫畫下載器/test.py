import multiprocessing
import pyperclip
import threading
import requests
import keyboard
import time
import re
import os
dir = os.path.abspath("R:/") # 可更改預設路徑
os.chdir(dir)

header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
}
# chrome_options = ""
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-popup-blocking")
# chrome_options.add_argument("--profile-directory=Default")
# chrome_options.add_argument("--ignore-certificate-errors")
# chrome_options.add_argument("--disable-plugins-discovery")
# chrome_options.add_argument("--incognito")
# chrome_options.add_argument('--no-first-run')
# chrome_options.add_argument('--no-service-autorun')
# chrome_options.add_argument('--no-default-browser-check')
# chrome_options.add_argument('--password-store=basic')
# chrome_options.add_argument('--no-sandbox')

def Download(Path,SaveName,Image_URL,headers):

        ImageData = requests.get(Image_URL, headers=headers)
        if ImageData.status_code == 200:
            with open(SaveName,"wb") as f:
                f.write(ImageData.content)


class AutomaticCopy:
    def __init__(self):
        self.initial = r"https://nhentai.*"
        self.download_trigger = False
        self.clipboard_cache = None

    def Read_clipboard(self):
        while True:
            clipboard = pyperclip.paste()
            time.sleep(0.3)

            if self.download_trigger:
                print("開始下載")
                break

            elif clipboard != self.clipboard_cache and re.match(self.initial,clipboard): 
                print(clipboard)
                self.clipboard_cache = clipboard

    def Download_command(self):
         
        while True:
            if keyboard.is_pressed("alt+s"):
                self.download_trigger = True
                while keyboard.is_pressed("alt+s"):
                    pass

# copy = AutomaticCopy()
# threading.Thread(target=copy.Read_clipboard).start()
# 
# command = threading.Thread(target=copy.Download_command)
# command.daemon = True
# command.start()