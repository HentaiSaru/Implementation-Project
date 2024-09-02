import ctypes
import opencc
from ctypes import wintypes
from sortedcontainers import SortedDict

"""
? dll 字串表提取器

* 1. 輸入 dll 路徑
* 2. 輸入字串表起始 id (由其他軟體查看)
* 3. 輸入字串表結束 id (由其他軟體查看)
* 4. 將字串字典, 輸出為 StringTable.rc

* 最後使用 Visual Studio Code 來編輯要修改的 dll, 以及 StringTable.rc

"""

LoadString = ctypes.windll.user32.LoadStringW
LoadString.argtypes = [wintypes.HINSTANCE, wintypes.UINT, wintypes.LPWSTR, ctypes.c_int]
LoadString.restype = ctypes.c_int

# 提取 dll 中的字符串, 將其文字轉成繁中
def extract_strings(path, start_id=1, max_id=100000):
    Record_dict = {}
    Save_dict = SortedDict()
    Converter = opencc.OpenCC("s2twp.json")

    DLL = ctypes.windll.LoadLibrary(path)
    Buffer = ctypes.create_unicode_buffer(1024)

    for id in range(start_id, max_id + 1):
        length = LoadString(DLL._handle, id, Buffer, 1024)

        if length > 0:
            string = Converter.convert(Buffer.value).translate(str.maketrans({'\n': '\\n', '\r': '\\r'}))

            if Record_dict.get(string) is None:
                Save_dict[id] = string
                Record_dict[string] = None

    return Save_dict

# 將字串字典, 輸出為 StringTable.rc
def save_strings_to_rc(path, strings):
    with open(path, "w", encoding="utf-8") as file:
        file.write('STRINGTABLE\nBEGIN\n')

        for id, string in strings.items():
            file.write(f'\t{id},"{string}"\n')

        file.write('END\n')

    print(f"已輸出: {path}")

save_strings_to_rc(
    "R:\\StringTable.rc",
    extract_strings("Lang.dll", 100, 10049)
)