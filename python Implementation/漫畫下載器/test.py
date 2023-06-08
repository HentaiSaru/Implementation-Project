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