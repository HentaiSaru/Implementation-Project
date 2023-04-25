import cv2
#cv2.cuda.printCudaDeviceInfo(0)
methods = [method_name for method_name in dir(cv2) if callable(getattr(cv2, method_name))]
class Classification:
    def __init__(self):
        pass
    # 所有模塊
    def _all(self,input):print(input)
    # 特徵匹配模塊
    def features(self,input):
        if input.find("features2d") != -1:print(input)
    # 文本辨識模塊
    def text(self,input):
        if input.find("text") != -1:print(input)
    # 深度學習模塊
    def dnn(self,input):
        if input.find("dnn") != -1 or input.find("ml") != -1:print(input)
    # GPU加速處理模塊
    def cuda(self,input):
        if input.find("cuda") != -1:print(input)
    # 高階圖像處理模塊(超分辨率處理)
    def advanced(self,input):
        if input.find("ximgproc") != -1 or input.find("xphoto") != -1:print(input)

find = Classification()

for data in methods:
    find._all(data)

"""
cv2.VideoCapture：用於捕獲視頻或視頻流，可以從遊戲畫面中捕獲畫面，也可以從外部攝像頭中捕獲畫面。

cv2.matchTemplate：用於模板匹配，可以在遊戲畫面中搜索指定的目標物體。

cv2.imshow：用於顯示圖像或視頻畫面，可以在處理遊戲畫面時將結果顯示在熒幕上。

cv2.waitKey：用於等待按鍵事件，可以在等待用戶輸入時暫停程式執行。

cv2.cvtColor：用於顏色空間轉換，可以將遊戲畫面轉換成指定的顏色空間進行後續處理。

cv2.threshold：用於圖像二值化，可以將遊戲畫面轉換成黑白圖像，方便進行後續處理。

cv2.findContours：用於圖像輪廓檢測，可以在遊戲畫面中檢測出物體的輪廓。

cv2.drawContours：用於在圖像上繪製輪廓，可以在遊戲畫面中繪製物體的輪廓。

cv2.rectangle：用於繪製矩形，可以在遊戲畫面中繪製矩形框，標記出物體的位置。

cv2.circle：用於繪製圓形，可以在遊戲畫面中繪製圓形，標記出物體的位置或進行其他操作。
"""