from tkinter import filedialog , messagebox
import threading
import tkinter as tk
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

    def open_file(self):

        try:

            data = filedialog.askopenfilename()

            if not data:raise FileNotFoundError

            self.filename = os.path.basename(data)
            self.directory = os.path.dirname(data)

            with open(data,'r',encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    self.ContentBox.append(line)
                    threading.Thread(target=gui.Content.insert,args=(tk.END, f"{line}\n")).start()

        except FileNotFoundError:pass
            

    def open_folder(self):
        pass

    def get_data(self):
        return self.directory , self.filename , self.ContentBox

class EncryptionCalculus:
    def __init__(self):
        self.key = None
        self.filename = None
        self.directory = None
        self.ContentBox = []
    
    def encryption(self):
        self.directory , self.filename , self.ContentBox = op.get_data()
        self.key = gui.passwoed
        print(self.filename)
        print(self.key)

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
        
        self.folder_button.config(font=("Arial Bold", 16), width=12, height=1, border=2 , relief='groove', fg=SelectText , bg=ChooseBackground)
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
        
        self.decrypt.config(font=("Arial Bold", 16), width=12, height=1, border=2 , relief='groove', fg=SelectText , bg=ChooseBackground)
        self.decrypt.place(x=820,y=60)

    def overwrite_output(self):
        
        self.overwrite.config(font=("Arial Bold", 16), width=12, height=1, border=2 , relief='groove', fg=SelectText , bg=ChooseBackground)
        self.overwrite.place(x=1000,y=10)

    def new_output(self):

        self.new.config(font=("Arial Bold", 16), width=12, height=1, border=2 , relief='groove', fg=SelectText , bg=ChooseBackground)
        self.new.place(x=1000,y=60)

if __name__ == "__main__":
    enc = EncryptionCalculus()
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