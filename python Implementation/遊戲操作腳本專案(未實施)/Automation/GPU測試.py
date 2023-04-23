import cv2

if cv2.cuda.getCudaEnabledDeviceCount() > 0:
    print("可以使用GPU加速")
else:
    print("無法使用GPU加速")