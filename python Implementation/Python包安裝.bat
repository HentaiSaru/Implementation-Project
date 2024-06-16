@echo off
chcp 65001
%1 %2
ver|find "5.">nul&&goto :Admin
mshta vbscript:createobject("shell.application").shellexecute("%~s0","goto :Admin","","runas",1)(window.close)&goto :eof
:Admin
cls

@echo ------------------------------
@echo pip update
python.exe -m pip install --upgrade pip
@echo ------------------------------

@echo ------------------------------
@echo installation package
@echo ------------------------------

:: 打包EXE
pip install pyinstaller
pip install cx_Freeze
::------------------------::
:: 加密
pip install tinyaes
pip install pycryptodome
:: 解密反編譯
pip install uncompyle6
::------------------------::
:: 爬蟲
pip install httpx[http2]
pip install requests
pip install grequests
pip install Scrapy
pip install urllib3
pip install beautifulsoup4
::------------------------::
:: 反爬處理
pip install scrapy-crawlera
:: 繞過 cloud 反爬檢測 (免費版)
pip install cloudscraper
:: 反爬自動化
pip install undetected-chromedriver2
:: 簡單的處理反爬, 與動態生成網站
pip install requests-html
::------------------------::
:: 異步請求
pip install aiohttp
:: 異步讀寫檔案
pip install aiofiles
::------------------------::
:: 自動化操作
pip install selenium
:: 驅動安裝
pip install chromedriver_autoinstaller
::------------------------::
:: RSS解析
pip install feedparser
:: 字符編碼檢測
pip install chardet
:: 語言文字轉換
pip install opencc
:: 字串比對
pip install fuzzywuzzy
pip install python-Levenshtein
::------------------------::
:: 事件檢測與進程相關資訊
pip install psutil
:: 獲取GPU資訊
pip install GPUtil
::------------------------::
:: 日期時間取得
pip install schedule
:: 版本比對
pip install packaging
:: 檔案下載
pip install wget
:: 讀取剪貼簿
pip install pyperclip
:: 播放音訊
pip install playsound
:: 可視化進度條
pip install tqdm
pip install progress
pip install progressbar
pip install progressbar2
pip install alive-progress
::------------------------::
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
:: html 代碼生成 模板
pip install Jinja2
:: AI庫 深度學習與神經網路
:: pip install torch (Cpu版本)
:: (GPU版) https://pytorch.org/get-started/locally/
::------------------------::
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
::------------------------::
:: 創建GUI
pip install PyQt5
pip install PyQt6
pip install PySide6
:: 創建系托盤圖標和菜單
pip install pystray
:: 自動化GUI交互
pip install PyAutoGUI
:: 圖像處理和操作
pip install Pillow
::------------------------::
:: discord Bot交互相關
pip install discord_webhook
::------------------------::
:: 視覺與圖像處理 - Cpu版本
:: pip install opencv-python

::編譯 opencv - gpu版本
::顯卡算力-> https://developer.nvidia.com/cuda-gpus#compute
:: GPU版本載點 https://pytorch.org/get-started/locally/
:: GPU開發工具下載 https://developer.nvidia.com/cuda-downloads
:: Cudnn https://developer.nvidia.com/rdp/cudnn-download
:: 編譯器 https://cmake.org/files/
:: https://github.com/opencv/opencv/tree/4.7.0
:: https://github.com/opencv/opencv_contrib/tree/4.7.0

:: 編譯設置
:: WITH_CUDA -> 開
:: OPENCV_DNN_CUDA -> 開
:: ENABLE_FAST_MATH -> 開
:: BUILD_CUDA_STUBS -> 開
:: PYTHON -> 看到能開的都開(除了有test的)
:: OPENCV_EXTRA_MODULES_PATH -> 指定opencv_contrib的modules
:: BUILD_opencv_world -> 開
:: OPENCV_ENABLE_NONFREE -> 開
:: conf 把debug和release改為只有release
:: CUDA_ARCH_BIN -> 根據顯卡算力設置
:: CUDA_FAST_MATH -> 開
:: test -> 可以都關掉
:: java -> 可以都關掉
:: OPENCV_GENERATE_SETUPVARS -> 關
:: 最後開啟 OpenCV.sln -> 用 vs 並且編譯 INSTALL

pip install --upgrade setuptools
pip install --upgrade wheel

@echo ------------------------------
@echo installation is complete
@echo ------------------------------
pause