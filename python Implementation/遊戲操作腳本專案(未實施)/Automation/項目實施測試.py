import numpy as np
import pyautogui
import torch
import time
import cv2
import mss
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class ScreenCapture:
    def __init__(self,refresh=None):
        self.refresh = refresh
        self.RefreshRate()

    def RefreshRate(self):
        if self.refresh != None:
            if self.refresh == 144:self.refresh = 0.007
            elif self.refresh == 60:self.refresh = 0.0167
        else:self.refresh = 0

    def debug(self,capture):
        win_size_w = 640
        win_size_h = 480

        # 創建窗口名稱
        cv2.namedWindow("Screen", cv2.WINDOW_NORMAL)
        # 窗口顯示位置
        cv2.moveWindow("Screen", 50, 50)
        # 窗口大小
        cv2.resizeWindow("Screen",win_size_w,win_size_h)
        cv2.setWindowProperty("Screen", cv2.WND_PROP_TOPMOST, 1)

        with mss.mss() as sct:
            
            while True:
                time.sleep(self.refresh)
                screen = sct.grab(capture)
                img = np.array(screen)
                # 找到匹配圖
                Seek.Find(img)

                # 重新縮放窗口圖片大小
                img = cv2.resize(img, (win_size_h, win_size_w))
                # 顯示窗口
                cv2.imshow("Screen", img)

                # 按下Esc終止
                if cv2.waitKey(1) == 27:
                    break

            cv2.destroyAllWindows()

    def NoWindow(self,capture):

        with mss.mss() as sct:
            while True:
                time.sleep(self.refresh)
                screen = sct.grab(capture)

class Match:
    def __init__(self,img,threshold):
        self.template = []
        self.template_names = []
        self.match = threshold
        for templates in img:
            self.template.append(cv2.imread(templates,cv2.IMREAD_GRAYSCALE))
            self.template_names.append(templates)

    def Find(self,photo):

        # 將掃描的螢幕轉成灰階
        img_gray = cv2.cvtColor(photo,cv2.COLOR_BGR2GRAY)

        for index , template in enumerate(self.template):

            # 將畫面與模板進行匹配
            res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
            # 匹配狀態
            loc = np.where(res >= self.match)

            # 匹配成功
            if len(loc[0]) > 0:
                self.template_names[index]
                #Action.draw(loc,template,photo)
                #Action.action(loc,self.template)

class Operate:
    def __init__(self):
        self.no = None

    # 為找到的項目繪製方框
    def draw(self,loc,template,photo):
        w,h = template.shape[::-1]
        for pt in zip(*loc[::-1]):
            cv2.rectangle(photo, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)

    # 對找到的目標操作
    def action(self,loc,template):

        # 獲取目標左上座標
        top_left = (loc[1][0], loc[0][0])
        # 獲取目標右下座標
        bottom_right = (loc[1][0] + template.shape[1], loc[0][0] + template.shape[0])
         # 計算中間座標
        x, y = (top_left[0] + bottom_right[0]) // 2, (top_left[1] + bottom_right[1]) // 2
        # 點擊
        pyautogui.click(x,y)


def get_screen_size():
    screen_size = pyautogui.size()
    return screen_size[0] , screen_size[1]

Screen = ScreenCapture(144)
Script = ["Image/test.png","Image/test2.png","Image/test3.png"]
Seek = Match(Script,0.9)
Action = Operate()

w , h = get_screen_size()
capture = {"top": 0, "left": 0, "width": w, "height": h}

Screen.debug(capture)
#Screen.NoWindow(capture)