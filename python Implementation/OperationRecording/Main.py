from Package.Operation_Logic.ShortcutKey_Trigger import KeyboardMonitor

keybo = KeyboardMonitor()

hotkey = {"SR":["Alt","F2"],"ER":["Alt","F3"],"SP":["Ctrl","F1"],"EP":["Ctrl","F2"]}

keybo(hotkey)