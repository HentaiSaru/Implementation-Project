from tkinter import filedialog , messagebox
from Crypto.Util.Padding import unpad , pad
from Crypto.Cipher import AES
import tkinter as tk
import threading
import binascii
import os

root = tk.Tk()
root.title("文本加密程式")

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
        self.ContentBox = []
        self.ContentDictionary = {}
        self.use_file = False
        self.use_folder = False

    def Reset(self):
        gui.Content.delete('1.0', tk.END)
        enc.Cipherbox.clear()
        enc.ContentBox.clear()
        dec.ContentBox.clear()
        dec.RestoreResult.clear()
        self.ContentBox.clear()
        self.ContentDictionary.clear()

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
                    threading.Thread(target=gui.Content.insert,args=(tk.END, f"{line}\n")).start()
                    self.ContentBox.append(line)

        except FileNotFoundError:pass    

    def open_folder(self):
        self.Reset()
        try:
            data = filedialog.askdirectory()

            if not data:raise FileNotFoundError

            self.use_folder = True
            self.use_file = False     

            self.directory = os.path.abspath(data)

            for file in os.listdir(self.directory):

                if file.endswith(".txt") or file.endswith(".encr"):

                    self.filename = file
                    path = os.path.join(self.directory,file)
                    threading.Thread(target=gui.Content.insert,args=(tk.END, f"{self.filename}\n")).start()

                    with open(path,'r',encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            self.ContentBox.append(line)

                    self.ContentDictionary[self.filename] = self.ContentBox.copy()
                    self.ContentBox.clear()

        except FileNotFoundError:pass

    def get_data(self):

        if self.use_file:
            yield self.directory , self.filename , self.ContentBox

        elif self.use_folder:
            for filename , ContentBox in self.ContentDictionary.items():
                yield self.directory , filename , ContentBox
class EncryptionCalculus:
    def __init__(self):
        self.key = None
        self.filename = None
        self.directory = None
        self.ContentBox = []
        self.Cipherbox = []
    
    def encryption(self):
        self.key = gui.passwoed
        for self.directory, self.filename, self.ContentBox in op.get_data():
            self.Calculus()

    def Calculus(self):
        try:
            if self.key != None:
                gui.Content.delete('1.0', tk.END)
            else:raise Exception()

            for encryp in self.ContentBox:
                 
                classical = self.Classical_Encryption(encryp).encode('utf-8')
                Aes = self.Classical_Encryption(self.AES_Encryption(classical))
                final_ciphertext = self.Binary_Conversion(self.Classical_Encryption(Aes)).encode('utf-8').hex()

                threading.Thread(target=gui.Content.insert,args=(tk.END, f"{final_ciphertext}\n")).start()
                self.Cipherbox.append(final_ciphertext)

        except Exception as e:
            messagebox.showerror("輸入錯誤","請設置密碼",parent=None)

    def AES_Encryption(self,code):
        key_bytes = pad(self.key.encode('utf-8'),32)
        iv = b"WeiChanghong8787"

        cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
        plaintext = pad(code, AES.block_size)
        ciphertext = cipher.encrypt(plaintext)

        return ciphertext.hex()
    
    def Binary_Conversion(self,code):
        hex_text = binascii.hexlify(code.encode()).decode()
        binary_text = bin(int(hex_text, 16))[2:]
        displacement = bin(int(binary_text, 2) << len(self.key))[2:]
        return displacement

    def Classical_Encryption(self,code):
        save = ""
        for char in code:
            save += chr(ord(char) + len(self.key))
        return save
class DecryptionCalculus:
    def __init__(self):
        self.key = None
        self.filename = None
        self.directory = None
        self.ContentBox = []
        self.RestoreResult = []

    def decryption(self):
        self.key = gui.passwoed
        for self.directory, self.filename, self.ContentBox in op.get_data():
            self.Calculus()

    def Calculus(self):
        try:
            if self.key != None:
                gui.Content.delete('1.0', tk.END)
            else:raise Exception()

            for decrypt in self.ContentBox:

                byte_str = bytes.fromhex(decrypt)
                unicode_str = byte_str.decode('utf-8')

                Aes_Recovery = self.Classical_Decryption(self.Binary_Conversion(unicode_str))
                string_restore = self.AES_Decryption(self.Classical_Decryption(Aes_Recovery)).decode('utf-8')
                final_restoration = self.Classical_Decryption(string_restore)
            
                threading.Thread(target=gui.Content.insert,args=(tk.END, f"{final_restoration}\n")).start()

                self.RestoreResult.append(final_restoration)

        except ValueError:
            messagebox.showerror(
                "操作錯誤",
                "可能的錯誤:\n1. 無開啟被加密文件\n2. 輸入了錯誤的密碼\n",
                parent=None
            )
        except Exception as e:
            messagebox.showerror("輸入錯誤","請輸入解密密碼",parent=None)

    def AES_Decryption(self,code):
        key_bytes = pad(self.key.encode('utf-8'), 32)
        iv = b"WeiChanghong8787"

        cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
        ciphertext_bytes = bytes.fromhex(code)
        plaintext_bytes = cipher.decrypt(ciphertext_bytes)
        plaintext = unpad(plaintext_bytes, AES.block_size)

        return plaintext
    
    def Binary_Conversion(self,code):
        binary_text = bin(int(code, 2) >> len(self.key))[2:].zfill(len(code))
        hex_text = hex(int(binary_text, 2))[2:]
        restore = binascii.unhexlify(hex_text.encode()).decode()
        return restore
    
    def Classical_Decryption(self,code):
        save = ""
        for char in code:
            save += chr(ord(char) - len(self.key))
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

    def Create():
        directory = enc.directory
        filename = enc.filename
        if directory == None:
            messagebox.showerror("操作錯誤","沒有進行加解密操作",parent=None)
        else:
            ChangeName = os.path.join(directory,f'{filename.split(".")[0]}.encr')
            
            with open(ChangeName, "w", encoding="utf-8") as f:
                for data in gui.Content.get("1.0", "end-1c"):
                    f.write(data)

            choose = messagebox.askquestion("輸出成功", "以輸出完畢,是否要開啟輸出位置")
            if choose == "yes":
                folder_path = os.path.dirname(directory)
                os.startfile(folder_path)

    def Overwrite():
        directory = enc.directory
        filename = enc.filename
        if directory == None:
            messagebox.showerror("操作錯誤","沒有進行加解密操作",parent=None)
        else:
            ChangeName = os.path.join(directory,filename)

            with open(ChangeName, "w", encoding="utf-8") as f:
                for data in gui.Content.get("1.0", "end-1c"):
                    f.write(data)

            choose = messagebox.askquestion("輸出成功", "以輸出完畢,是否要開啟輸出位置")
            if choose == "yes":
                folder_path = os.path.dirname(directory)
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