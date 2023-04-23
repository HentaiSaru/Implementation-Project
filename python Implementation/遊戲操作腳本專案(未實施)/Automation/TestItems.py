import concurrent.futures
import numpy as np
import pyautogui
import threading
import torch
import glob
import time
import cv2
import mss
import os
# 設置預設路徑位置
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 獲取螢幕大小
def get_screen_size():
    screen_size = pyautogui.size()
    return screen_size[0] , screen_size[1]

class ScreenScan:
    def __init__(self,window_name=None):
        self.name = window_name
        self.window_width = 640
        self.window_height = 480
        # 創建窗口名稱
        cv2.namedWindow(self.name, cv2.WINDOW_NORMAL)
        # 窗口顯示位置
        cv2.moveWindow(self.name, 50, 50)
        # 窗口大小設置
        cv2.resizeWindow(self.name,self.window_width,self.window_height)
        # 窗口置頂
        cv2.setWindowProperty(self.name, cv2.WND_PROP_TOPMOST, 1)
        # 使用Mss掃描
        self.sct = mss.mss()

    def window(self,capture):

        # 處理圖片為 numpy 數組
        img = np.array(self.sct.grab(capture))
        # 重新縮放窗口圖片大小
        scaling = cv2.resize(img,(self.window_width,self.window_height))
        # 顯示畫面
        cv2.imshow(self.name, scaling)
        return img

    def NoWindow(self,capture):

        img = np.array(self.sct.grab(capture))
        return img

width , height = get_screen_size()
class Matching:
    def __init__(self,template,threshold,refresh=None,use_window=False):
        self.Capture = {"top": 0, "left": 0, "width": width, "height": height}
        self.refresh = refresh
        self.template = []
        self.template_names = []
        self.threshold = threshold

        if use_window:
            self.Scan = ScreenScan("DeBug")
            self.ScreenshotUse = self.Scan.window
        else:
            self.Scan = ScreenScan()
            self.ScreenshotUse = self.Scan.NoWindow

        for process in template:
            absolute = process.replace('\\', '/')
            self.template.append(cv2.imread(absolute,0))
            self.template_names.append(absolute.split("/")[1])

        if self.refresh != None:
            if self.refresh == 144:self.refresh = 0.007
            elif self.refresh == 60:self.refresh = 0.0167
        else:self.refresh = 1

    def Find_A_Template(self):

        while True:
            time.sleep(self.refresh)

            picture = self.ScreenshotUse(self.Capture)
            # 灰度轉換
            gray = cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)

            with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.template)) as executor:
                futures = []

                for index, template in enumerate(self.template):
                    futures.append(executor.submit(self.Match_Template , gray , template , index , picture))

                for _ in concurrent.futures.as_completed(futures):
                    pass

            if cv2.waitKey(1) == 27:
                break

        cv2.destroyAllWindows()

    def Match_Template(self,gray, template, index, picture):

        # 進行匹配
        res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)

        # 匹配狀態
        loc = np.where(res >= self.threshold)

        # 成功匹配操作
        if len(loc[0]) > 0:
            # 畫框
            # DrawBox = Action.DrawBox(loc, template, picture)
            # if self.use_window:
            #     cv2.imshow(self.scan.name, DrawBox)

            print(self.template_names[index])

class ActionScript:
    def __init__(self):
        pass

    # 多線程匹配目前無法正確繪製
    def DrawBox(self,loc,template,image):
        w,h = template.shape[::-1]
        for img in zip(*loc[::-1]):
            cv2.rectangle(image , img , (img[0] + w, img[1] + h), (0, 255, 0), 2)
        return image
    
Action = ActionScript()

if __name__ == "__main__":
    # 獲取模板(暫時先不進行預處理)
    template = glob.glob('Image/*.[jp][pn]g')
    # 傳入模板,置信度,刷新率,是否使用窗口(刷新預設1,窗口使用預設無)
    Match = Matching(template,0.7,144,True)
    Match.Find_A_Template()