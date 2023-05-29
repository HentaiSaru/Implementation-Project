import ModCheck

""" Versions 1.1

[+] 單線程處理
[+] 批量輸入比對
[+] 首次自動添加
[+] 更新連結顯示
[+] 模板自動更新

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