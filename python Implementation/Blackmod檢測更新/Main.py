import ModCheck

""" Versions 1.3

[+] 單線程處理
[+] 批量輸入比對
[+] 首次自動添加
[+] 模板自動更新

[-] 刪除直接顯示下載連結(功能失效)
[+] 顯示網頁網址

自用 基本無優化
"""

test = [
    "https://blackmod.net/threads/12167/",
    "https://blackmod.net/threads/28267/",
    "https://blackmod.net/threads/28095/",
    "https://blackmod.net/threads/28547/",
]

ModCheck.run(test)
print("\n==============================\n")
for out in ModCheck.processing.Result():
    print(out)
    print("\n==============================\n")