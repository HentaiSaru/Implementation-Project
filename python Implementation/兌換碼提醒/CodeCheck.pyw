from RedemptionCode import auto
import multiprocessing
import threading
import time

def run():
    while True:
        # 檢測時沒網路程式會直接中止
        auto.Detection("https://www.gbyhn.com.tw/blog/post/hsr")
        auto.Detection("https://www.gbyhn.com.tw/blog/post/genshin60")

        # 輸出新的時間戳
        auto.Output_timestamp()

        # 每兩小時檢測一次
        time.sleep(7200)

if __name__ == '__main__':
    # 進程調用
    multiprocessing.Process(target=run).start()
    
    # 線程調用
    # threading.Thread(target=run).start()