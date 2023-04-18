from tkinter import filedialog, messagebox
import tkinter as tk
import opencc
import os

root = tk.Tk()
root.title("簡轉繁 文字轉換器")
# 使用當前檔案的絕對路徑的,目錄名稱做為指定位置,導入Icon圖片
Icon = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ChineseConversion.ico')
root.iconbitmap(Icon)
root.resizable(False, False)
# Gui窗口大小
interface_width = 280
interface_height = 180
# 取得使用者的螢幕寬度高度
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()
# 計算窗口正中間的位置
windowCenterWidth = (window_width - interface_width)/2
windowCenterHeight = (window_height - interface_height)/2
# 設置開啟位置於螢幕中心
root.geometry(f"{interface_width}x{interface_height}+{int(windowCenterWidth)}+{int(windowCenterHeight)}")
root.configure(background='#BA90C6')
buttonbackground = "#E8A0BF"
buttontrigger = "#C0DBEA"
buttontext = "#FDF4F5"

class basic:
    def __init__ (self):
        self.Content = None
        self.filename = None
        self.directory = None
        self.Scrollbar = None
        self.openbutton = None
        self.CreateOutput = None
        self.OverwriteOutput = None
        self.ConversionBox = []
        self.SaveBox = []
        self.converter = opencc.OpenCC('s2twp.json')

    # 初始按鈕    
    def initial_button(self):
        self.openbutton = tk.Button(root, text="選擇檔案")
        self.openbutton.config(font=("Arial Bold", 22), width=12, height=1, fg=buttontext , border=2, relief='groove', bg=buttonbackground , command=self.open_file)
        self.openbutton.place(x=27,y=15)

        # 創建滾動條
        self.Scrollbar = tk.Scrollbar(root,cursor='hand2',width=20,relief="raised")
        self.Content = tk.Text(root , bg=buttonbackground , fg=buttontext , width=85 , height=31 , yscrollcommand=self.Scrollbar.set)
        self.Content.config(font=("Arial", 13),bd=0)
        self.Scrollbar.config(command=self.Content.yview)

    # 將處理結果插入至GUI文字框
    def displaybox(self, line):
        self.Content.insert(tk.END, f"{line}\n")

    # 選擇檔案後的處理
    def open_file(self):

        try:
            self.openbutton.config(fg=buttontrigger,bg=buttonbackground)

            # 開啟文件
            data = filedialog.askopenfilename()

            # 取消選取
            if not data:raise FileNotFoundError

            # 獲取文件名稱
            self.filename = os.path.basename(data)
            # 獲取文件路徑
            self.directory = os.path.dirname(data)

            with open(data, 'r' , encoding='utf-8') as f:
                for line in f:
                    line = line.strip() # 刪除特殊轉譯符
                    self.SaveBox.append(line)
                    self.Content.after(0, self.displaybox, line)

            # 變更窗口大小與位置
            root.geometry(f"{interface_width*3}x{interface_height*4}+{int(windowCenterWidth/2+150)}+{int(windowCenterHeight/2-50)}")
            # 刪除原本的按鈕
            self.openbutton.destroy()
            # 再次創建新的按鈕
            self.openbutton = tk.Button(root, text="開始轉換")
            self.openbutton.config(font=("Arial Bold", 22), width=12, height=1, fg=buttontext , border=2, relief='groove', bg=buttonbackground , command=self.Conversion)
            self.openbutton.place(x=570,y=630)

            # 顯示文字框 和 滾動條
            self.Content.place(x=30,y=20)
            self.Scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        except FileNotFoundError:
            self.openbutton.config(fg=buttontext,bg=buttonbackground)
            pass
        except UnicodeDecodeError:
            self.openbutton.config(fg=buttontext,bg=buttonbackground)
            messagebox.showerror("格式錯誤","此選項並非文本格式")
            self.open_file()
        except Exception as e:
            self.openbutton.config(fg=buttontext,bg=buttonbackground)
            messagebox.showerror("例外錯誤",f"錯誤代碼:{e}")
            self.open_file()

    # 簡體轉繁體觸發
    def Conversion(self):
        self.Content.delete("1.0", "end")
        self.openbutton.config(fg=buttontrigger,bg=buttonbackground)

        # 將保存的簡體一行一行轉成繁體,並且將結果顯示再文字框
        for Simplified in self.SaveBox:
            Traditional = self.converter.convert(Simplified)
            self.ConversionBox.append(Traditional)
            self.Content.after(0, self.displaybox, Traditional)

        # 刪除原先按鈕
        self.openbutton.destroy()

        self.openbutton = tk.Button(root, text="重新選擇檔案")
        self.openbutton.config(font=("Arial Bold", 22), width=12, height=1, fg=buttontext , border=2, relief='groove', bg=buttonbackground , command=self.Reselect)
        self.openbutton.place(x=30,y=630)

        # 創建兩個輸出按鈕
        self.CreateOutput = tk.Button(root, text="建立新檔輸出")
        self.OverwriteOutput = tk.Button(root, text="覆蓋原始輸出")

        self.CreateOutput.config(font=("Arial Bold", 22), width=12, height=1, fg=buttontext , border=2, relief='groove', bg=buttonbackground , command=self.Create)
        self.OverwriteOutput.config(font=("Arial Bold", 22), width=12, height=1, fg=buttontext , border=2, relief='groove', bg=buttonbackground , command=self.Overwrite)
        
        self.CreateOutput.place(x=270,y=630)
        self.OverwriteOutput.place(x=510,y=630)

    def Create(self):

        self.CreateOutput.config(fg=buttontext,bg=buttonbackground)
        filepath = os.path.join(self.directory, f"轉換繁體_{self.converter.convert(self.filename)}")

        with open(filepath, "w", encoding="utf-8") as f:
            for data in self.ConversionBox:
                f.write(data + "\n")

        choose = messagebox.askquestion("輸出成功", "以輸出完畢,是否要開啟輸出位置")
        if choose == "yes":
            folder_path = os.path.dirname(filepath)
            os.startfile(folder_path)

    def Overwrite(self):
        self.OverwriteOutput.config(fg=buttontext,bg=buttonbackground)
        filepath = os.path.join(self.directory, self.filename)
        ChangeName = os.path.join(self.directory, self.converter.convert(self.filename))

        with open(filepath, "w", encoding="utf-8") as f:
            for data in self.ConversionBox:
                f.write(data + "\n")

        # 將檔案名稱也變成繁體
        os.rename(filepath, ChangeName)

        choose = messagebox.askquestion("輸出成功", "以輸出完畢,是否要開啟輸出位置")
        if choose == "yes":
            folder_path = os.path.dirname(filepath)
            os.startfile(folder_path)

    def Reselect(self):
        self.open_file()
        self.CreateOutput.destroy()
        self.OverwriteOutput.destroy()

if __name__ == "__main__":
    Gui = basic()
    Gui.initial_button()
    root.mainloop()