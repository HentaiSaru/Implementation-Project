import tkinter as tk
import os

def run_command():
    command = entry.get()  # 获取输入的命令
    output = os.popen(command).read()  # 运行命令并获取输出
    text.insert(tk.END, output)  # 在Text小部件中插入输出文本

root = tk.Tk()

entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text="Run", command=run_command)
button.pack()

text = tk.Text(root)
text.pack()

root.mainloop()