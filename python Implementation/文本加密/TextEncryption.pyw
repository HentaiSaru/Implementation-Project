from tkinter import filedialog , messagebox
from Crypto.Util.Padding import unpad , pad
from Crypto.Cipher import AES
import tkinter as tk
import threading
import binascii
import hashlib
import base64
import zlib
import os

"""
Versions 1.1

[+] 多重加密
[+] 批量加解密
[+] 批量加密輸出

待修正

1. 功能使用待測試
2. 加上程式註解
3. 有很多不必要的變數 , 未來很閒再進行重構

"""

root = tk.Tk()
root.title("文本加密程式 v1.0")

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

class FRAW:
    def __init__(self):
        self.filename = None
        self.directory = None
        self.use_file = False
        self.use_folder = False
        self.ContentBox = []
        self.encrypted_dictionary = {}
        self.decryption_dictionary = {}

    def Reset(self):
        gui.Content.delete('1.0', tk.END)
        enc.Cipherbox.clear()
        enc.ContentBox.clear()
        enc.BatchDictionary.clear()
        dec.ContentBox.clear()
        dec.RestoreResult.clear()
        self.ContentBox.clear()
        self.encrypted_dictionary.clear()
        self.decryption_dictionary.clear()

    def open_file(self):
        self.Reset()
        try:
            data = filedialog.askopenfilename()

            if not data:raise FileNotFoundError

            self.use_file = True
            self.use_folder = False

            self.filename = os.path.basename(data)
            self.directory = os.path.dirname(data)

            with open(data,'r',encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    self.ContentBox.append(line)
            
            threading.Thread(target=gui.Content.insert,args=(tk.END, f"{self.filename}\n")).start()

        except FileNotFoundError:pass    

    def open_folder(self):
        self.Reset()
        try:
            data = filedialog.askdirectory()

            if not data:raise FileNotFoundError

            self.use_folder = True
            self.use_file = False

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
            threading.Thread(target=gui.Content.insert,args=(tk.END, f"{illustrate}\n")).start()

            for file in os.listdir(self.directory):

                if file.endswith(".txt"):

                    self.filename = file
                    path = os.path.join(self.directory,file)
                    threading.Thread(target=gui.Content.insert,args=(tk.END, f"{self.filename}\n")).start()

                    with open(path,'r',encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            self.ContentBox.append(line)

                    self.encrypted_dictionary[self.filename] = self.ContentBox.copy()
                    self.ContentBox.clear()

                elif file.endswith(".encr"):

                    self.filename = file
                    path = os.path.join(self.directory,file)
                    threading.Thread(target=gui.Content.insert,args=(tk.END, f"{self.filename}\n")).start()

                    with open(path,'r',encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            self.ContentBox.append(line)

                    self.decryption_dictionary[self.filename] = self.ContentBox.copy()
                    self.ContentBox.clear()

        except FileNotFoundError:pass

    def get_data(self,type):

        if type == "enc":
            if self.use_file:
                yield self.directory , self.filename , self.ContentBox
            elif self.use_folder:
                for filename , ContentBox in self.encrypted_dictionary.items():
                    yield self.directory , filename , ContentBox

        elif type == "dec":
            if self.use_file:
                yield self.directory , self.filename , self.ContentBox
            elif self.use_folder:
                for filename , ContentBox in self.decryption_dictionary.items():
                    yield self.directory , filename , ContentBox

def MD5_Key(string):

    md5 = hashlib.md5()
    merge = ""

    md5.update(string.encode('utf-8'))
    results = md5.hexdigest()

    for i in range(16):
        char_sum = ord(results[i]) + ord(results[i+1])
        char_sum %= 94
        char_sum += 33
        merge += chr(char_sum)

    return (merge + merge[::-1]).encode('utf-8')

def MD5_IV(string):

    md5 = hashlib.md5()
    merge = ""

    md5.update(string.encode('utf-8'))
    results = md5.hexdigest()
    a_str = results[:16]
    b_str = results[16:]

    for i in range(16):
        char_sum = ord(a_str[i]) + ord(b_str[i])
        char_sum %= 94
        char_sum += 33
        merge += chr(char_sum)

    return merge.encode("utf-8")
class EncryptionCalculus:
    def __init__(self):
        self.key = None
        self.filename = None
        self.directory = None
        self.OffsetCount = None
        self.BatchDictionary = {}
        self.ContentBox = []
        self.Cipherbox = []
    
    def encryption(self):
        self.key = gui.passwoed
        for self.directory, self.filename, self.ContentBox in op.get_data("enc"):
            self.Cipherbox.clear()
            self.Calculus()
        dec.DecryptSignal = False
        
    def Calculus(self):
        try:
            if self.key != None:
                gui.Content.delete('1.0', tk.END)
            else:raise Exception()

            for encryp in self.ContentBox:

                self.OffsetCount = 2
                classical = self.Classical_Encryption(encryp).encode('utf-8')

                self.OffsetCount += (len(self.key) + self.OffsetCount)
                Aes = self.Classical_Encryption(self.AES_Encryption(classical))

                self.OffsetCount += len(self.key)
                final_ciphertext = self.Binary_Conversion(self.Classical_Encryption(Aes)).encode('utf-8').hex()

                self.Cipherbox.append(self.Compression(final_ciphertext))

            threading.Thread(target=gui.Content.insert,args=(tk.END, f"{self.filename} - 加密完畢\n")).start()
            self.BatchDictionary[self.filename] = self.Cipherbox.copy()
            
        except Exception as e:
            messagebox.showerror("輸入錯誤","請設置密碼",parent=None)

    def AES_Encryption(self,code):

        cipher = AES.new(MD5_Key(self.key), AES.MODE_CBC, MD5_IV(self.key))
        plaintext = pad(code, AES.block_size)
        ciphertext = cipher.encrypt(plaintext)

        return ciphertext.hex()
    
    def Compression(self,code):

        com = zlib.compress(code.encode('utf-8'))
        return base64.b64encode(com).decode('utf-8')
    
    def Binary_Conversion(self,code):
        hex_text = binascii.hexlify(code.encode()).decode()
        binary_text = bin(int(hex_text, 16))[2:]
        displacement = bin(int(binary_text, 2) << (len(self.key) + self.OffsetCount))[2:]
        return displacement

    def Classical_Encryption(self,code):
        save = ""
        for char in code:
            save += chr(ord(char) + (len(self.key) + self.OffsetCount))
        return save
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

            for decrypt in self.ContentBox:

                byte_str = bytes.fromhex(self.Decompressed(decrypt).decode('utf-8'))
                unicode_str = byte_str.decode('utf-8')

                self.OffsetCount = 2
                self.OffsetCount += (len(self.key) + self.OffsetCount)
                self.OffsetCount += len(self.key) 
                InitialOffset = self.OffsetCount
                Aes_Recovery = self.Classical_Decryption(self.Binary_Conversion(unicode_str))

                self.OffsetCount -= len(self.key)
                string_restore = self.AES_Decryption(self.Classical_Decryption(Aes_Recovery)).decode('utf-8')

                self.OffsetCount -= int(InitialOffset / 2)
                final_restoration = self.Classical_Decryption(string_restore)
 
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
        return zlib.decompress(com)
    
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
class GUI:
    def __init__(self):
        self.passwoed = None

        self.top_frame = tk.Frame(root , width=interface_width-20 , height=110, bd=0, highlightthickness=0 , bg=root['background'])
        self.top_frame.place(x=10, y=10)

        self.text_frame = tk.Frame(root , width=interface_width-41 , height=710, bd=0, highlightthickness=0 , bg=root['background'])
        self.text_frame.place(x=10, y=130)

        self.scroll_bar_frame = tk.Frame(root , width=20 , height=710, bd=0, highlightthickness=0 , bg=root['background'])
        self.scroll_bar_frame.place(x=1170, y=130)

        self.file_button = tk.Button(self.top_frame , text="文件檔選擇")
        self.folder_button = tk.Button(self.top_frame , text="文件夾選擇")
        self.encryption = tk.Button(self.top_frame , text="文本加密")
        self.decrypt = tk.Button(self.top_frame , text="文本解密")
        self.overwrite = tk.Button(self.top_frame , text="覆蓋輸出")
        self.new = tk.Button(self.top_frame , text="新建輸出")
        self.password = tk.Entry(self.top_frame, font=("Microsoft Positive Bold", 50), width=17 , justify='center' , borderwidth=1, highlightthickness=2 , bg=PasswordBox , fg=DisplayText)
        self.Scrollbar = tk.Scrollbar(self.scroll_bar_frame,cursor='hand2',relief="raised",width=23)
        self.Content = tk.Text(self.text_frame , bg=ChooseBackground , fg=root['background'] , yscrollcommand=self.Scrollbar.set)

    def file_selection(self):

        self.file_button.config(font=("Arial Bold", 16), width=12, height=1, border=2 , relief='groove', fg=SelectText , bg=ChooseBackground , command=op.open_file)
        self.file_button.place(x=10,y=10)

    def folder_selection(self):
        
        self.folder_button.config(font=("Arial Bold", 16), width=12, height=1, border=2 , relief='groove', fg=SelectText , bg=ChooseBackground , command=op.open_folder)
        self.folder_button.place(x=10,y=60)

    def password_input_box(self):
  
        self.password.place(x=200,y=20)
        self.password.insert(0,"密碼設置")

        def FocusInput(event):
            if self.password.get() == "密碼設置":
                self.password.delete(0, tk.END)

        def FocusOut(event):
            if self.password.get() == "":
                self.password.insert(0, "密碼設置")

        def Enter(event):
            self.passwoed = self.password.get()

        self.password.bind("<Button-1>",FocusInput)
        self.password.bind("<FocusOut>",FocusOut)
        self.password.bind("<KeyRelease>", lambda event:Enter(event))

    def encryption_display_box(self):

        self.Content.config(font=("Arial", 24),bd=0)
        self.Scrollbar.config(command=self.Content.yview)

        self.Content.place(x=0,y=0)
        self.Scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.Scrollbar.place(relheight=1.0, relwidth=1.0)

    def encryption_button(self):
        
        self.encryption.config(font=("Arial Bold", 16), width=12, height=1, border=2 , relief='groove', fg=SelectText , bg=ChooseBackground , command=enc.encryption)
        self.encryption.place(x=820,y=10)

    def decrypt_button(self):
        
        self.decrypt.config(font=("Arial Bold", 16), width=12, height=1, border=2 , relief='groove', fg=SelectText , bg=ChooseBackground , command=dec.decryption)
        self.decrypt.place(x=820,y=60)

    def overwrite_output(self):
        
        self.overwrite.config(font=("Arial Bold", 16), width=12, height=1, border=2 , relief='groove', fg=SelectText , bg=ChooseBackground , command=SaveOutput.Overwrite)
        self.overwrite.place(x=1000,y=10)

    def new_output(self):

        self.new.config(font=("Arial Bold", 16), width=12, height=1, border=2 , relief='groove', fg=SelectText , bg=ChooseBackground , command=SaveOutput.Create)
        self.new.place(x=1000,y=60)
class SaveOutput:

    def RetrieveData():
        if dec.DecryptSignal:
            directory = dec.directory
        else:
            directory = enc.directory

        return directory , enc.BatchDictionary.items()

    def EncryptedOutput(ChangeName,content):
        with open(ChangeName, "w", encoding="utf-8") as f:
            for index , data in enumerate(content):
                if index == len(content) - 1:
                    f.write(data.rstrip('\n'))
                else:
                    f.write(f"{data}\n")

    def DecryptedOutput(ChangeName):
        with open(ChangeName, "w", encoding="utf-8") as f:
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
    enc = EncryptionCalculus()
    dec = DecryptionCalculus()
    gui = GUI() 
    op = FRAW()

    gui.file_selection()
    gui.folder_selection()
    gui.password_input_box()
    gui.encryption_button()
    gui.decrypt_button()
    gui.overwrite_output()
    gui.new_output()
    gui.encryption_display_box()

    root.mainloop()