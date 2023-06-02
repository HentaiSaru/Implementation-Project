import threading
import pyperclip
import time
import os

class Scrapbook:
    def __init__(self):
        self.fetch_cache = None
        self.delay = None
        self.clear = None
        self.result = []

    def __call__(self,delay:float=0.1 , clear:bool=False):

        self.delay = delay
        self.clear = clear

        threading.Thread(target=self.capture).start()

    def capture(self):
        pyperclip.copy('')
        
        while True:
            time.sleep(self.delay)
            clipboard = pyperclip.paste()

            if clipboard != self.fetch_cache:
                self.fetch_cache = clipboard
                self.result.append(clipboard)

                if self.clear:
                    os.system("cls")

                print(clipboard)

    def get_result(self):
        if len(self.result) != 0:
            return self.result