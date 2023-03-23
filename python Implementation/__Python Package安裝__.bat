@echo off
chcp 65001
%1 %2
ver|find "5.">nul&&goto :Admin
mshta vbscript:createobject("shell.application").shellexecute("%~s0","goto :Admin","","runas",1)(window.close)&goto :eof
:Admin
cls

@echo pip principal update==========
py -m pip install -U pip
cls


@echo pip installation package======
@echo ~
@echo ~

pip install pyinstaller
pip install uncompyle6

pip install discord_webhook
pip install pystray
pip install feedparser
pip install numpy
pip install pywin32
pip install scipy
pip install pandas
pip install matplotlib
pip install scikit-learn
pip install opencv-python
pip install PyQt5
pip install PyAutoGUI
pip install pymem
pip install mss
pip install requests
pip install keyboard
pip install pynput
pip install beautifulsoup4
pip install Scrapy
pip install torch

python -m pip install --upgrade pip setuptools

pause