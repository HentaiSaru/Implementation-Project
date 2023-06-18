import json
import os

tsgs = None
result_spl = {}
result_all = {}


name = "範圍201-300.json"

with open(name , "r") as file:
    tsgs = json.loads(file.read())

stopjudging = True
stopline = 20
calculate = 0

for tag , count in tsgs.items():

    if stopjudging:
        calculate += 1
        os.system(f"start {tag}")

        if calculate >= stopline:
            n = input("繼續測試...")
            calculate = 0
            if n == "0":
                stopjudging = False
    else:
        result_all[tag] = count

if len(result_all) > 0:
    with open(name , "w") as file:
        file.write(json.dumps(result_all, indent=4, separators=(',',':')))
else:
    os.system(f"del /f /s /q {name}")