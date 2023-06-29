from Package.Operation_Logic.ShortcutKey_Trigger import KeyboardMonitor

"""
* 回放結束 , 會直接中止程式
"""

keybo = KeyboardMonitor()
hotkey = {"SR":["Alt","F2"],"ER":["Alt","F3"],"SP":["Ctrl","F1"],"EP":["Ctrl","F2"]}
keybo(hotkey , "Script-2023-06-29-16-00-13")