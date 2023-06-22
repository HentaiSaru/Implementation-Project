# https://steam.oxxostudio.tw/category/python/example/matplotlib-pie.html
from numpy import random
import matplotlib.pyplot as plt
x = random.randint(100,1000,5)
def func(s,d):
  t = int(round(s/100.*sum(d)))     # 透過百分比反推原本的數值
  return f'{s:.1f}%\n( {t}ml )'     # 使用文字格式化的方式，顯示內容
plt.pie(x,
        radius=1.5,
        textprops={'color':'w', 'weight':'bold', 'size':12},  # 設定文字樣式
        pctdistance=0.7,
        autopct=lambda i: func(i,x),
        wedgeprops={'linewidth':3,'edgecolor':'w'})   # 繪製每個扇形的外框
plt.show()