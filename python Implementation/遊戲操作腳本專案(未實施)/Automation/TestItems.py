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
        self.Action = ActionScript()
        self.template_data = {}
        self.threshold = threshold
        self.lock = threading.Lock()
        self.stream = cv2.cuda_Stream()
        cv2.cuda_TargetArchs('compute_30')

        if use_window:
            self.Scan = ScreenScan("DeBug")
            self.ScreenshotUse = self.Scan.window
        else:
            self.Scan = ScreenScan()
            self.ScreenshotUse = self.Scan.NoWindow

        for process in template:
            absolute = process.replace('\\', '/')
            name = absolute.split("/")[1]
            self.template_data[name] = cv2.imread(absolute, 0)

        if self.refresh != None:
            if self.refresh == 144:self.refresh = 0.007
            elif self.refresh == 60:self.refresh = 0.0167
        else:self.refresh = 1

    def Find_A_Template(self):

        while True:
            time.sleep(self.refresh)

            # 獲取畫面截圖
            Screen = self.ScreenshotUse(self.Capture)
            # 灰度轉換
            GrayScreen = cv2.cvtColor(Screen, cv2.COLOR_BGR2GRAY)

            with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.template_data)) as executor:
                futures = []
                
                for TemplateName , Template in self.template_data.items():
                    futures.append(executor.submit(self.Match_Template , GrayScreen , Template , TemplateName , Screen))

                for _ in concurrent.futures.as_completed(futures):
                    pass

            if cv2.waitKey(1) == 27:
                break

        cv2.destroyAllWindows()

    def Match_Template(self, GrayScreen , Template , TemplateName , Screen):
        """預設可用匹配模板
        cv2.TM_CCOEFF
        cv2.TM_CCOEFF_NORMED
        cv2.TM_CCORR
        cv2.TM_CCORR_NORMED
        cv2.TM_SQDIFF
        cv2.TM_SQDIFF_NORMED
        """
        # !等待修復 , 想嘗試使用gpu加速匹配 , 但找不到處理該類型數據的方法
        # 進行匹配
        result = cv2.cuda_TemplateMatching(self.Screen_Transition(GrayScreen) , self.Template_Conversion(Template) , cv2.TM_CCOEFF_NORMED , stream=self.stream)
        print(result)
        # 取得匹配成功位置
        _, _, _, max_loc = cv2.cuda.minMaxLoc(result)
        
        
        # if cv2.cuda.max(result)[0] > self.threshold:
        #     self.lock.acquire()
        #     print(TemplateName)
        #     self.Action.DrawBox(max_loc,Screen,self.Template_Conversion(Template))
        #     self.lock.release()

    def Template_Conversion(self,template):
        return cv2.cuda_GpuMat(template)
    
    def Screen_Transition(self,template):
        return cv2.cuda_GpuMat(template)
class ActionScript:
    def __init__(self):
        pass

    # 多線程匹配目前無法正確繪製
    def DrawBox(self,loc,Screen,Template):
        h, w = Template.shape
        top_left = (int(loc.x), int(loc.y))
        bottom_right = (int(loc.x + w), int(loc.y + h))
        cv2.cuda.drawRect(Screen, top_left, bottom_right, (0, 255, 0), 2)

if __name__ == "__main__":
    # 獲取模板(暫時先不進行預處理)
    template = glob.glob('Image/*.[jp][pn]g')
    # 傳入模板,置信度,刷新率,是否使用窗口(刷新預設1,窗口使用預設無)
    Match = Matching(template,0.7,use_window=True)
    Match.Find_A_Template()