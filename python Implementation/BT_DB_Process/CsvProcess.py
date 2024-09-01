import csv
import time
import queue
import psutil
import opencc
import psutil
import threading
from tqdm import tqdm
from sortedcontainers import SortedDict
from concurrent.futures import ThreadPoolExecutor

def ReadCsv(path):
    with open(path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            yield row

def WriteCsv(path, data):
    with open(path, 'w', encoding='utf-8') as csvfile:
        # writer = csv.writer(csvfile)
        value = data.values()
        size = len(value) - 1
        # 為了避免最後一行, 不使用正常 csv 的方式寫入 (但進度條會壞掉)
        for index, row in tqdm(enumerate(value), total=size, desc="輸出中"):
            if index == size:
                csvfile.write(row)
            else:
                csvfile.write(row + "\n")

def throttle(wait):
    def decorator(fn):
        last_call_time = [0]
        last_result = [None]
        def throttled(*args, **kwargs):
            current_time = time.time()
            if current_time - last_call_time[0] >= wait:
                last_call_time[0] = current_time
                last_result[0] = fn(*args, **kwargs)
            return last_result[0]
        return throttled
    return decorator

@throttle(5.0)  # 5 秒取得一次
def GetMemory():
    return psutil.virtual_memory().percent

class Maim:
    def __init__(self):
        self.queue = queue.Queue()
        self.converter = opencc.OpenCC("s2twp.json")
        self.list_to_string = lambda lst: ','.join([str(item).strip() for item in lst])

    def Run(self, row):
        Data = self.converter.convert(self.list_to_string(row))
        self.queue.put((row, Data))

    def Process(self):
        count = 0
        local_dict = SortedDict()

        while True:
            task = self.queue.get()

            if task is None:  # 檢查結束信號
                break

            name = task[0][1]
            Item = local_dict.get(name)

            if Item is None:
                local_dict[name] = task[1]
            else: # 重複時, 比較大小, 大的覆蓋
                count -= 1 # 當有重複對象時, 重複數據不納入計算
                rowSize = int(task[0][2])
                itemSize = int(Item.split(',')[2]) # 將保存數據轉回列表

                if rowSize > itemSize:
                    local_dict[name] = task[1]

            count += 1
            print(f"\r記憶體佔用: {GetMemory()}% | 已處理: {count} 筆數據", end="", flush=True)

        # 輸出數據
        WriteCsv("R:\\Clean.csv", local_dict)
        local_dict.clear()

if __name__ == "__main__":
    main = Maim()

    threading.Thread(target=main.Process).start() # 最大線程數量為, CPU核心數量 * CPU線程數量
    with ThreadPoolExecutor(max_workers=(psutil.cpu_count() * psutil.cpu_count(False))) as executor:
        for row in ReadCsv("R:\\db.csv"):
            name = row[1]
            if name.isdigit(): # 排除都是數字的
                continue
            executor.submit(main.Run, row)

    main.queue.put(None) # 完成停止