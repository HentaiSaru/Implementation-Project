from tkinter import filedialog , messagebox , colorchooser
from Crypto.Util.Padding import unpad , pad
from Crypto.Cipher import AES
import tkinter as tk
import threading
import binascii
import hashlib
import base64
import random
import string
import zlib
import os

"""
Versions 1.2

[+] 顯示換色
[+] 多重加密
[+] 批量加解密
[+] 批量加密輸出
[+] 註解添加

待修正

1. 功能使用待測試
2. 有很多不必要的變數 , 未來很閒再進行重構

"""

root = tk.Tk()
root.title("文本加密程式 v1.2")

Icon = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'encrypted.ico')
root.iconbitmap(Icon)
root.resizable(False, False)

interface_width = 1200
interface_height = 850
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()
windowCenterWidth = (window_width - interface_width)/2
windowCenterHeight = (window_height - interface_height)/2

root.geometry(f"{interface_width}x{interface_height}+{int(windowCenterWidth)}+{int(windowCenterHeight)}")

root.configure(background='#150050')
ChooseBackground = "#3F0071"
PasswordBox = "#000000"
DisplayText = "#FFFFFF"
SelectText = "#FB2576"

# 開啟文件讀取
class FRAW:
    def __init__(self):
        self.filename = None
        self.directory = None
        self.use_file = False
        self.use_folder = False
        self.indent = " " * 50
        self.ContentBox = [] # 讀取內容數據保存
        self.encrypted_dictionary = {} # 存放加密數據的字典
        self.decryption_dictionary = {} # 存放解密數據的字典

    # 重新選擇文件時會調用該方法重置
    def Reset(self):
        gui.Content.delete('1.0', tk.END) # 清除內容框文字
        enc.ContentBox.clear()  # 清除準備加密的內容
        enc.Cipherbox.clear()   # 清除加密後結果
        enc.BatchDictionary.clear() # 清除加密結果字典
        dec.ContentBox.clear()  # 清除準備解密內容
        dec.RestoreResult.clear() # 解密後結果
        self.ContentBox.clear() # 清除獲取的保存數據
        self.encrypted_dictionary.clear() # 清除需加密內容字典
        self.decryption_dictionary.clear() # 清除需解密內容字典

    # 開啟單獨文件
    def open_file(self):
        self.Reset()
        try:
            # 開啟文件獲取內容
            data = filedialog.askopenfilename()

            # 內容為空 pass 基本上就是沒有選擇
            if not data:raise FileNotFoundError

            # 文件選取為True , 文件夾選取為False
            self.use_file = True
            self.use_folder = False

            # 取得文件名 , 路徑
            self.filename = os.path.basename(data)
            self.directory = os.path.dirname(data)

            # 開啟該文件
            with open(data,'r',encoding='utf-8') as f:
                for line in f:
                    line = line.strip() # 一行一行讀取並去除不必要內容
                    self.ContentBox.append(line) # 將內容保存至待處理box

            # 這邊原本是輸出所有的文件內容 , 但太多會卡 , 改成只輸出開啟文件名
            threading.Thread(target=gui.Content.insert,args=(tk.END, f"{self.filename}\n")).start()

        except FileNotFoundError:pass

    # 開啟文件夾
    def open_folder(self):
        self.Reset()
        try:
            data = filedialog.askdirectory()

            if not data:raise FileNotFoundError

            self.use_folder = True
            self.use_file = False

            # 這邊先取得文件路徑而已
            self.directory = os.path.abspath(data)

            illustrate = """
            選擇【文件夾】批量導入說明:

            解密時只能解密由此程式新建輸出的.encr檔案
            要解密其他類型檔案 , 使用文件檔選取單檔案

            解密會同時開啟所有的.encr進行解密 , 如再將解密後檔案輸出
            會出現所有輸出檔案內容 , 都合併變成一樣的狀況

            (因為輸出是讀取你看到的文字框內容 , 因此不要批量解密輸出)

            以下為你開啟的檔案...
            """
            # 顯示出說明文字
            threading.Thread(target=gui.Content.insert,args=(tk.END, f"{illustrate}\n")).start()

            # 獲取該路徑所有檔案
            for file in os.listdir(self.directory):
            
                # 選出文字文件
                if file.endswith(".txt"):
                
                    self.filename = file # 取得檔名
                    path = os.path.join(self.directory,file) # 將檔名與路徑合併
                    threading.Thread(target=gui.Content.insert,args=(tk.END, f"{self.indent}{self.filename}\n")).start()

                    # 開啟該檔案內容
                    with open(path,'r',encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            self.ContentBox.append(line)

                    # 將檔名作為字典的 key , 並將保存的數據複製為 value
                    self.encrypted_dictionary[self.filename] = self.ContentBox.copy()
                    # 清除保存數據盒 , 方便讀取下一個文件
                    self.ContentBox.clear()

                # 選出加密文件
                elif file.endswith(".encr"):
                
                    self.filename = file
                    path = os.path.join(self.directory,file)
                    threading.Thread(target=gui.Content.insert,args=(tk.END, f"{self.indent}{self.filename}\n")).start()

                    with open(path,'r',encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            self.ContentBox.append(line)

                    self.decryption_dictionary[self.filename] = self.ContentBox.copy()
                    self.ContentBox.clear()
            
        except FileNotFoundError:pass

    # 獲取處理的數據
    def get_data(self,type):

        # 獲取加密數據
        if type == "enc":
            if self.use_file: # 開啟文件檔(回傳:路徑,檔名,內容)
                yield self.directory , self.filename , self.ContentBox
            elif self.use_folder: # 開啟文件夾(先從字典獲取所需數據再回傳)
                for filename , ContentBox in self.encrypted_dictionary.items():
                    yield self.directory , filename , ContentBox

        # 獲取解密數據
        elif type == "dec":
            if self.use_file:
                yield self.directory , self.filename , self.ContentBox
            elif self.use_folder:
                for filename , ContentBox in self.decryption_dictionary.items():
                    yield self.directory , filename , ContentBox

# 對輸入的Key進行轉換
def MD5_Key(string):
    md5 = hashlib.md5()
    merge = ""

    # 對key進行md5雜湊
    md5.update(string.encode('utf-8'))
    results = md5.hexdigest()

    # md5雜湊後,會有32碼,將2碼2碼的進行轉換
    for i in range(16):
        # 將字元編碼相加
        char_sum = ord(results[i]) + ord(results[i+1])
        # 進行轉換 , 避免超出範圍
        char_sum %= 94
        char_sum += 33
        # 最後將編碼轉回字元 , 並合併成新的字串
        merge += chr(char_sum)

    # 將合併的字串(16碼) + 上反轉的合併字串 , 變成32碼的key
    return (merge + merge[::-1]).encode('utf-8')

# IV的產生算法
def MD5_IV(string):
    md5 = hashlib.md5()
    merge = ""

    # 進行雜湊
    md5.update(string.encode('utf-8'))
    results = md5.hexdigest()
    # 將雜湊的前16和後16字串,分為兩個不同字串
    a_str = results[:16]
    b_str = results[16:]

    for i in range(16):
        # 進行字元碼相加
        char_sum = ord(a_str[i]) + ord(b_str[i])
        char_sum %= 94
        char_sum += 33
        # 合併變成32碼IV
        merge += chr(char_sum)

    return merge.encode("utf-8")

# 加密演算法
class EncryptionCalculus:
    def __init__(self):
        self.key = None
        self.filename = None
        self.directory = None
        self.OffsetCount = None # 偏移計數
        self.BatchDictionary = {} # 批量字典
        self.ContentBox = [] # 獲取需加密數據保存盒
        self.Cipherbox = [] # 加密結果保存盒
        # 加密用的混淆字串 (大小英文+數字+符號)
        self.EncChars = string.ascii_letters + string.digits + string.punctuation

    def encryption(self):
        self.key = gui.passwoed # 取得輸入的key
        for self.directory, self.filename, self.ContentBox in op.get_data("enc"):
            # 獲取所需數據後,清除加密結果盒(假設數據不只一條,所以每次運行都要清除)
            self.Cipherbox.clear()
            # 呼叫開始加密
            self.Calculus()
        dec.DecryptSignal = False

    def Calculus(self):
        try:
            # 如果有輸入key , 也就是不為空
            if self.key != None:
                # 清除展示框
                gui.Content.delete('1.0', tk.END)
            else:raise Exception() # 為空輸出例外

            # 一行一行的獲取需加密數據
            for encryp in self.ContentBox:
                # 偏移初始為2
                self.OffsetCount = 2
                # 首先就對明文進行古典偏移 , 將明文的字元變成其他字
                #! 混淆後一起偏移
                classical = self.Classical_Encryption(self.Confuse(encryp, 1)).encode('utf-8')

                # 偏移量變化 , 初始偏移 + (key的長度 + 初始偏移)
                self.OffsetCount += (len(self.key) + self.OffsetCount)
                # 進行AES加密 , 將回傳結果進行偏移
                #! 偏移後再次混淆
                Aes = self.Confuse(self.Classical_Encryption(self.AES_Encryption(classical)), 2)

                # 偏移量變化 , (變化偏移量 + key的長度)
                self.OffsetCount += len(self.key)
                # 將aes結果轉成二進制 , 再次偏移結果 , 然後轉成16進制
                final_ciphertext = self.Classical_Encryption(self.Binary_Conversion(Aes)).encode('utf-8').hex()

                # 最後將最終密文 , 進行壓縮轉換 , 進行保存
                self.Cipherbox.append(self.Compression(final_ciphertext))

            # 展示框顯示完成
            threading.Thread(target=gui.Content.insert,args=(tk.END, f"{self.filename} - 加密完畢\n")).start()
            # 將結果連同檔名 , 存入字典保存
            self.BatchDictionary[self.filename] = self.Cipherbox.copy()

        except Exception as e:
            messagebox.showerror("輸入錯誤","請設置密碼",parent=None)

    # AES加密
    def AES_Encryption(self,code):
        # 使用被轉換過的 Key 和 Iv 進行加密
        cipher = AES.new(MD5_Key(self.key), AES.MODE_CBC, MD5_IV(self.key))
        plaintext = pad(code, AES.block_size)
        ciphertext = cipher.encrypt(plaintext)
        # 回傳16進制結果
        return ciphertext.hex()

    # 壓縮
    def Compression(self,code):
        com = zlib.compress(code.encode('utf-8'))
        # 將壓縮後的2進制表示結果 , 轉成字串類型 , 因為輸出保存不是寫出2進制 , 所以要轉成字串
        return base64.b64encode(com).decode('utf-8')

    # 二進制轉換
    def Binary_Conversion(self,code):
        hex_text = binascii.hexlify(code.encode()).decode()
        binary_text = bin(int(hex_text, 16))[2:]
        # 這邊也會進行偏移 , 而進制的 <<
        displacement = bin(int(binary_text, 2) << (len(self.key) + self.OffsetCount))[2:]
        return displacement

    # 古典加密偏移
    def Classical_Encryption(self,code):
        save = ""
        for char in code:
            save += chr(ord(char) + (len(self.key) + self.OffsetCount))
        return save
    
    # 混淆字串添加
    def Confuse(self, code, parity: int):
        # parity (1是奇數 , 2是偶數)
        obfuscation = ""
        for data in code:
            if parity == 1:
                obfuscation += f"{random.choice(self.EncChars)}{data}"
            elif parity == 2:
                obfuscation += f"{data}{random.choice(self.EncChars)}"
        return obfuscation

# 解密演算法
class DecryptionCalculus:
    def __init__(self):
        self.key = None
        self.filename = None
        self.directory = None
        self.OffsetCount = None
        self.DecryptSignal = False
        self.ContentBox = []
        self.RestoreResult = []

    def decryption(self):
        self.key = gui.passwoed

        for self.directory, self.filename, self.ContentBox in op.get_data("dec"):
            self.Calculus()
        self.DecryptSignal = True

    def Calculus(self):

        try:
            if self.key != None:
                gui.Content.delete('1.0', tk.END)
            else:raise Exception()

            # 基本上就是把加密算法 , 最終的密文 , 一步一步的推回去 , 獲取明文
            for decrypt in self.ContentBox:
            
                byte_str = bytes.fromhex(self.Decompressed(decrypt))
                unicode_str = byte_str.decode('utf-8')

                self.OffsetCount = 2
                self.OffsetCount += (len(self.key) + self.OffsetCount)
                self.OffsetCount += len(self.key)
                InitialOffset = self.OffsetCount
                # 還原AES密文
                Aes_Recovery = self.Binary_Conversion(self.Classical_Decryption(unicode_str))

                self.OffsetCount -= len(self.key)
                # 進行AES解密
                string_restore = self.AES_Decryption(self.Classical_Decryption(self.Clarify(Aes_Recovery, 2))).decode('utf-8')

                self.OffsetCount -= int(InitialOffset / 2)
                # 最終字串
                final_restoration = self.Classical_Decryption(self.Clarify(string_restore, 1))

                threading.Thread(target=gui.Content.insert,args=(tk.END, f"{final_restoration}\n")).start()

                self.RestoreResult.append(final_restoration)

                enc.BatchDictionary[self.filename] = self.RestoreResult.copy()

        except ValueError:
            messagebox.showerror(
            "操作錯誤",
            "可能的錯誤:\n1. 無開啟被加密文件\n2. 輸入了錯誤的密碼\n",
            parent=None
            )
        except Exception as e:
            messagebox.showerror("輸入錯誤","請輸入解密密碼",parent=None)

    def AES_Decryption(self,code):
        cipher = AES.new(MD5_Key(self.key), AES.MODE_CBC, MD5_IV(self.key))
        ciphertext_bytes = bytes.fromhex(code)
        plaintext_bytes = cipher.decrypt(ciphertext_bytes)
        plaintext = unpad(plaintext_bytes, AES.block_size)
        return plaintext

    def Decompressed(self,code):
        com = base64.b64decode(code)
        return zlib.decompress(com).decode('utf-8')

    def Binary_Conversion(self,code):
        binary_text = bin(int(code, 2) >> (len(self.key) + self.OffsetCount))[2:].zfill(len(code))
        hex_text = hex(int(binary_text, 2))[2:]
        restore = binascii.unhexlify(hex_text.encode()).decode()
        return restore

    def Classical_Decryption(self,code):
        save = ""
        for char in code:
            save += chr(ord(char) - (len(self.key) + self.OffsetCount))
        return save
    
    def Clarify(self, code, parity: int):
        if parity == 1:
            return code[1::2]
        elif parity == 2:
            return code[::2]

# 此程式的GUI顯示
class GUI:
    def __init__(self):
        self.passwoed = None

        # 頂層框架
        self.top_frame = tk.Frame(root , width=interface_width-20 , height=110, bd=0, highlightthickness=0 , bg=root['background'])
        self.top_frame.place(x=10, y=10)

        # 文本顯示框架
        self.text_frame = tk.Frame(root , width=interface_width-41 , height=710, bd=0, highlightthickness=0 , bg=root['background'])
        self.text_frame.place(x=10, y=130)

        # 滾動條框架
        self.scroll_bar_frame = tk.Frame(root , width=20 , height=710, bd=0, highlightthickness=0 , bg=root['background'])
        self.scroll_bar_frame.place(x=1170, y=130)

        self.file_button = tk.Button(self.top_frame , text="文件檔選擇") # 文件檔選擇按鈕
        self.folder_button = tk.Button(self.top_frame , text="文件夾選擇") # 文件夾選擇按鈕
        self.text_box_color = tk.Button(self.top_frame , text="文本框文字色選擇") # 文本顏色選擇按鈕
        self.background_frame_color = tk.Button(self.top_frame , text="文本框背景色選擇") # 文本背景選擇色按鈕
        self.encryption = tk.Button(self.top_frame , text="文本加密") # 加密按鈕
        self.decrypt = tk.Button(self.top_frame , text="文本解密") # 解密按鈕
        self.overwrite = tk.Button(self.top_frame , text="覆蓋輸出") # 覆蓋輸出按鈕
        self.new = tk.Button(self.top_frame , text="新建輸出")  # 新建輸出按鈕
        # 密碼輸入框
        self.password = tk.Entry(self.top_frame, font=("Microsoft Positive Bold", 35), width=15 , justify='center' , borderwidth=1, highlightthickness=2 , bg=PasswordBox , fg=DisplayText)
        # 滾動條
        self.Scrollbar = tk.Scrollbar(self.scroll_bar_frame, cursor="hand2", relief="raised", width=23)
        # 顯示內容框
        self.Content = tk.Text(self.text_frame, bg=ChooseBackground, fg=root['background'], yscrollcommand=self.Scrollbar.set)

    def file_selection(self):

        self.file_button.config(font=("Arial Bold", 16), width=12, height=1, border=2 , relief='groove', fg=SelectText , bg=ChooseBackground , command=op.open_file)
        self.file_button.place(x=10,y=10)

    def folder_selection(self):

        self.folder_button.config(font=("Arial Bold", 16), width=12, height=1, border=2 , relief='groove', fg=SelectText , bg=ChooseBackground , command=op.open_folder)
        self.folder_button.place(x=10,y=60)

    def text_choose_color(self):

        color = colorchooser.askcolor(title="文字顏色選擇")
        if color[1]:
            self.Content.config(fg=color[1])

    def background_choose_color(self):

        color = colorchooser.askcolor(title="文字框背景顏色選擇")
        if color[1]:
            self.Content.config(bg=color[1])

    def text_color(self):

        self.text_box_color.config(font=("Arial Bold", 16), width=14, height=1, border=2 , relief='groove', fg=SelectText , bg=ChooseBackground , command=self.text_choose_color)
        self.text_box_color.place(x=634, y=60)

    def background_color(self):

        self.background_frame_color.config(font=("Arial Bold", 16), width=14, height=1, border=2 , relief='groove', fg=SelectText , bg=ChooseBackground , command=self.background_choose_color)
        self.background_frame_color.place(x=634,y=10)

    def password_input_box(self):

        self.password.place(x=205, y=47)
        self.password.insert(0, "密碼設置")

        def FocusInput(event):
            if self.password.get() == "密碼設置":
                self.password.delete(0, tk.END)

        def FocusOut(event):
            if self.password.get() == "":
                self.password.insert(0, "密碼設置")

        def Enter(event):
            self.passwoed = self.password.get()

        # 選取時狀態
        self.password.bind("<Button-1>",FocusInput)
        # 非選取時狀態
        self.password.bind("<FocusOut>",FocusOut)
        # 讀取輸入的文字
        self.password.bind("<KeyRelease>", lambda event:Enter(event))

    # 內容展示框
    def encryption_display_box(self):

        self.Content.config(font=("Arial", 24), bd=0)
        self.Scrollbar.config(command=self.Content.yview)

        self.Content.place(x=0, y=0)
        self.Scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.Scrollbar.place(relheight=1.0, relwidth=1.0)

    def encryption_button(self):

        self.encryption.config(font=("Arial Bold", 16), width=12, height=1, border=2 , relief='groove', fg=SelectText , bg=ChooseBackground , command=enc.encryption)
        self.encryption.place(x=835,y=10)

    def decrypt_button(self):

        self.decrypt.config(font=("Arial Bold", 16), width=12, height=1, border=2 , relief='groove', fg=SelectText , bg=ChooseBackground , command=dec.decryption)
        self.decrypt.place(x=835,y=60)

    def overwrite_output(self):

        self.overwrite.config(font=("Arial Bold", 16), width=12, height=1, border=2 , relief='groove', fg=SelectText , bg=ChooseBackground , command=SaveOutput.Overwrite)
        self.overwrite.place(x=1010,y=10)

    def new_output(self):

        self.new.config(font=("Arial Bold", 16), width=12, height=1, border=2 , relief='groove', fg=SelectText , bg=ChooseBackground , command=SaveOutput.Create)
        self.new.place(x=1010,y=60)

# 輸出方法
class SaveOutput:

    # 檢索當前是加密還是解密
    def RetrieveData():
        if dec.DecryptSignal:
            directory = dec.directory
        else:
            directory = enc.directory

        return directory , enc.BatchDictionary.items()

    # 加密輸出
    def EncryptedOutput(ChangeName,content):
        with open(ChangeName, "w", encoding="utf-8") as f:
            # 加密輸出是讀取檔案內容
            for index , data in enumerate(content):
                if index == len(content) - 1:
                    f.write(data.rstrip('\n'))
                else:
                    f.write(f"{data}\n")

    # 解密輸出
    def DecryptedOutput(ChangeName):
        with open(ChangeName, "w", encoding="utf-8") as f:
            # 解密輸出讀取的是 , 顯示內容框
            for data in gui.Content.get("1.0", "end-2c"):
                f.write(data)

    def Create():

        directory , data = SaveOutput.RetrieveData()

        for filename , content in data:

            if directory == None:
                messagebox.showerror("操作錯誤","沒有進行加解密操作",parent=None)
            else:
                ChangeName = os.path.join(directory,f'{filename.split(".")[0]}.encr')

            if dec.DecryptSignal:
                SaveOutput.DecryptedOutput(ChangeName)
            else:
                SaveOutput.EncryptedOutput(ChangeName,content)

        choose = messagebox.askquestion("輸出成功", "以輸出完畢,是否要開啟輸出位置")
        if choose == "yes":
            folder_path = os.path.dirname(ChangeName)
            os.startfile(folder_path)

    def Overwrite():

        directory , data = SaveOutput.RetrieveData()

        for filename , content in data:

            if directory == None:
                messagebox.showerror("操作錯誤","沒有進行加解密操作",parent=None)
            else:
                ChangeName = os.path.join(directory,filename)

            if dec.DecryptSignal:
                SaveOutput.DecryptedOutput(ChangeName)
            else:
                SaveOutput.EncryptedOutput(ChangeName,content)

        choose = messagebox.askquestion("輸出成功", "以輸出完畢,是否要開啟輸出位置")
        if choose == "yes":
            folder_path = os.path.dirname(ChangeName)
            os.startfile(folder_path)

if __name__ == "__main__":
    enc = EncryptionCalculus() # 加密算法
    dec = DecryptionCalculus() # 解密算法
    gui = GUI() # GUI顯示
    op = FRAW() # 開啟檔案

    gui.file_selection() # 文件選擇
    gui.folder_selection() # 文件夾選擇

    gui.text_color() # 文字顏色選擇
    gui.background_color() # 背景顏色選擇

    gui.password_input_box() # 密碼輸入框

    gui.encryption_button() # 加密按鈕
    gui.decrypt_button() # 解密按鈕

    gui.overwrite_output() # 覆蓋輸出按鈕
    gui.new_output() # 新建輸出按鈕

    gui.encryption_display_box() # 顯示內容框

    root.mainloop()