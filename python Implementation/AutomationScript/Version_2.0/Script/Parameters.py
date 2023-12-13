from selenium.webdriver.chrome.options import Options
import datetime
import random
import pytz
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Dataio import DI

class Parameters:
    def __init__(self):
        self.Settings = Options()
        self.generate_port = []
        self.port = 1024
    
    """
    * 隨機端口生成
    * 二種版本再低於 2 萬以下的生成量 , 差異並不大
    """
    # 複雜版-隨機端口 (複雜版當生成量大時 , 所需時間更長) [懷舊用]
    def RandomPort(self):
        increment_port = int(self.port * random.uniform(1.0, 64.0))
        
        if increment_port <= 65535:
            port = random.randint(self.port, increment_port)
        else:
            port = random.randint(self.port, (increment_port-1))

        if port != None:
            try:
                if port not in self.generate_port:
                    self.generate_port.append(port)
                    return port
                else:
                    raise Exception()
            except:
                return self.RandomPort()

    # 簡易版-隨機端口 (簡易版生成量大時 , 時間只需複雜版的一半)
    def Simple_RandomPort(self):
        port = random.randint(self.port, 65535)
        if port not in self.generate_port:
            self.generate_port.append(port)
            return port
        else:
            return self.Simple_RandomPort()

    # 計算等待秒數
    def WaitingTime(self):
        # 取得時區 (亞洲/台北)
        TaipeiTimezone = pytz.timezone('Asia/Taipei')
        # 當前時區時間
        current_time = datetime.datetime.now(TaipeiTimezone).time()

        # 設置目標時間 , 00:00 分
        TargetTime = datetime.time(hour=0, minute=0, second=0)

        if current_time < TargetTime:
            seconds_to_wait = (datetime.datetime.combine(datetime.date.today(), TargetTime) - datetime.datetime.combine(datetime.date.today(), current_time)).seconds
        else:
            seconds_to_wait = (datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1), TargetTime) - datetime.datetime.combine(datetime.date.today(), current_time)).seconds

        # 當等待時間 > 1 分鐘 , 回傳 3 秒
        if seconds_to_wait > 60:
            return 3
        else:
            return seconds_to_wait

    # 參數設置
    def AddSet(self, value: str, headless: bool = False):
        if headless:self.Settings.add_argument("--headless")
        self.Settings.add_argument("--no-sandbox")
        self.Settings.add_argument('--log-level=3')
        self.Settings.add_argument('--start-maximized')
        self.Settings.add_argument('--disable-notifications')
        self.Settings.add_argument('--disable-popup-blocking')
        self.Settings.add_argument('--ignore-certificate-errors')
        self.Settings.add_argument('--remote-debugging-address=0.0.0.0')
        self.Settings.add_argument(f"--remote-debugging-port={self.RandomPort()}")
        self.Settings.add_argument(f"--user-data-dir={DI.get_website_data(value)}")
        self.Settings.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        self.Settings.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.Settings.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.Settings.add_experimental_option('useAutomationExtension', False)
        return self.Settings

paramet = Parameters()