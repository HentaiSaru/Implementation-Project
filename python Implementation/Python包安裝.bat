@echo off
chcp 65001
%1 %2
ver|find "5.">nul&&goto :Admin
mshta vbscript:createobject("shell.application").shellexecute("%~s0","goto :Admin","","runas",1)(window.close)&goto :eof
:Admin
cls

@echo pip principal update==========
pip install --upgrade pip
cls


@echo pip installation package======
@echo ~
@echo ~

:: 打包EXE
pip install pyinstaller


:: 加密
pip install tinyaes


:: 解密反編譯
pip install uncompyle6


:: discord Bot交互相關
pip install discord_webhook


:: 爬蟲
pip install requests
pip install Scrapy
pip install beautifulsoup4
pip install urllib3

:: 異步請求
pip install aiohttp

:: 異步讀寫檔案
pip install aiofiles

:: 自動化操作
pip install selenium


:: 日期時間取得
pip install schedule


:: 字符編碼檢測
pip install chardet
:: 語言文字轉換
pip install opencc


:: 事件檢測與進程相關資訊
pip install psutil


:: RSS解析
pip install feedparser


:: 數值分析
pip install numpy
:: 數據操作
pip install pandas
:: 科學計算和高等數學
pip install scipy
:: 數據可視化
pip install matplotlib
:: 機器學習與數據挖掘
pip install scikit-learn


:: 創建GUI
pip install PyQt5
:: 創建系托盤圖標和菜單
pip install pystray
:: 自動化GUI交互
pip install PyAutoGUI
:: 圖像處理和操作
pip install Pillow
:: 視覺與圖像處理
pip install opencv-python


:: 處理鍵盤操作
pip install keyboard
:: 控制和監控輸入設備
pip install pynput
:: 內存讀寫
pip install pymem
:: 訪問windows API
pip install pywin32
:: 畫面截圖與錄影
pip install mss


:: AI庫 深度學習與神經網路
pip install torch

pip install --upgrade setuptools
pip install --upgrade wheel
pause