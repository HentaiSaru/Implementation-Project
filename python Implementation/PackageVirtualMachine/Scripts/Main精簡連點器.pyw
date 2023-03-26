from tkinter import messagebox , ttk
from PIL import Image, ImageTk
from pynput import keyboard
import tkinter as tk
import pyautogui
import threading
import warnings
import time
import json
import sys
import os
def Validateinseconds(new_value):
    return True
def Authentication(key):
    if  key == '123':
        messagebox.showinfo("高級版解鎖", "功能待開發")
    else:
        messagebox.showerror("高級版解鎖", "功能待開發")
def speed(h,m,s,t,H):
    if h != 0:
        h *= 3600
    if m != 0:
        m *= 60
    if t != 0:
        t /= 10
    if H != 0:
        H /= 100
    Intervals = h+m+s+t+H
    if Intervals == 'none':
        Intervals = 0
    return Intervals
def Timeformatconversion(Time):
    if Time >= 3600:
        Time=(Time/60)/60
        return "h" , int(Time)
    elif Time >= 60:
        Time /= 60
        return "m" , int(Time)
    elif Time >= 1:
        return "s" , int(Time)
    elif Time >= 0.1:
        Time *= 10
        return "t"  , int(Time)
    elif Time >= 0.01:
        Time *= 100
        return "H"  , int(Time)
    else:return "s" , int(Time+1)
def ButtonNameConversion(name):
    match name:
        case "none":return "無"
        case "right":return "右鍵"
        case "left":return "左鍵"
def numberofclicks(Var):
    if Var < 1:
        if Var >= 0.1:
            return 20
        else:return 15
    return Var
Ctrl = keyboard.Key.ctrl_l
Alt = keyboard.Key.alt_l
Shift = keyboard.Key.shift_l
F1 = keyboard.Key.f1
F2 = keyboard.Key.f2
F3 = keyboard.Key.f3
F4 = keyboard.Key.f4
F5 = keyboard.Key.f5
F6 = keyboard.Key.f6
F7 = keyboard.Key.f7
F8 = keyboard.Key.f8
F9 = keyboard.Key.f9
F10 = keyboard.Key.f10
F11 = keyboard.Key.f11
F12 = keyboard.Key.f12
key_combination = [Ctrl,Alt,Shift,F1,F2,F3,F4,F5,F6,F7,F8,F9,F10,F11,F12]
def Judgmentshortcut(keyA,KeyB):
    match keyA:
        case 'Ctrl':keyA = Ctrl
        case 'Alt':keyA = Alt
        case 'Shift':keyA = Shift
    match KeyB:
        case "F1":KeyB = F1
        case "F2":KeyB = F2
        case "F3":KeyB = F3
        case "F4":KeyB = F4
        case "F5":KeyB = F5
        case "F6":KeyB = F6
        case "F7":KeyB = F7
        case "F8":KeyB = F8
        case "F9":KeyB = F9
        case "F10":KeyB = F10
        case "F11":KeyB = F11
        case "F12":KeyB = F12
    return keyA,KeyB
def OutputConversion(key):
    match key:
        case "Key.ctrl_l":key = 'Ctrl'
        case "Key.alt_l":key = 'Alt'
        case "Key.shift":key = 'Shift'
        case "Key.f1":key = 'F1'
        case "Key.f2":key = 'F2'
        case "Key.f3":key = 'F3'
        case "Key.f4":key = 'F4'
        case "Key.f5":key = 'F5'
        case "Key.f6":key = 'F6'
        case "Key.f7":key = 'F7'
        case "Key.f8":key = 'F8'
        case "Key.f9":key = 'F9'
        case "Key.f1":key = 'F10'
        case "Key.f1":key = 'F11'
        case "Key.f1":key = 'F12'
    return key
IntervalsT = ['0'] * 5             
shortcutk = ['Alt','F1','Alt','F2']
MouseB = ['none']                  
MouseBcache = ['none']             
keyboardK = ['none'] * 5           
keyboardKcache = ['none'] * 5      
global MS,KS
global SKeycache , A_startcombo , B_startcombo
global EKeycache , A_endcombo , B_endcombo    
MS = KS = False
SKeycache = [Alt,F1]
EKeycache = [Alt,F2]
A_startcombo = Alt  
B_startcombo = F1   
A_endcombo = Alt    
B_endcombo = F2     
def BackendArchiveRead(save):
    global combospeed
    Timeformat , Timefigures = Timeformatconversion(save['UserSettings']['IntervalSpeed']) #獲取轉換後的時間格式
    match Timeformat:
        case "h":
            IntervalsT[0] = Timefigures
        case "m":
            IntervalsT[1] = Timefigures
        case "s":
            IntervalsT[2] = Timefigures
        case "t":
            IntervalsT[3] = Timefigures
        case "H":
            IntervalsT[4] = Timefigures
def stopLoop():
    global stop
    stop = False
def Clos():
    global stop
    stop = False
    os._exit(0)

def shortcut_key_start(keyA,KeyB):
    global SKeycache , A_startcombo , B_startcombo
    keyC = SKeycache[0]
    keyD = SKeycache[1]
    if keyA != keyC or KeyB != keyD:
        SKeycache[0] = keyA
        SKeycache[1] = KeyB
        A_startcombo = keyA
        B_startcombo = KeyB
def shortcut_key_stop(keyA,KeyB):
    global EKeycache , A_endcombo , B_endcombo
    keyC = EKeycache[0]
    keyD = EKeycache[1]
    if keyA != keyC or KeyB != keyD:
        EKeycache[0] = keyA
        EKeycache[1] = KeyB
        A_endcombo = keyA
        B_endcombo = KeyB
def setup():
    while True:
        global button , combospeed
        time.sleep(0.5)
        hour = int(IntervalsT[0])
        Minute = int(IntervalsT[1])
        Seconds = int(IntervalsT[2])
        Tenthofasecond = int(IntervalsT[3])
        Hundredthsofasecond = int(IntervalsT[4])
        button = MouseB[0]
        combospeed = speed(hour,Minute,Seconds,Tenthofasecond,Hundredthsofasecond)
        startshortcut = Judgmentshortcut(shortcutk[0],shortcutk[1]) 
        endshortcut = Judgmentshortcut(shortcutk[2],shortcutk[3])
        if startshortcut[0] != endshortcut[0] or startshortcut[1] != endshortcut[1]: 
            shortcut_key_start(*startshortcut)
            shortcut_key_stop(*endshortcut)
        elif startshortcut[1] == endshortcut[1]:
            messagebox.showerror("設置錯誤", "禁止相同的快捷鍵\n請重新設置")
            while True:
                time.sleep(1)
                startshortcut = Judgmentshortcut(shortcutk[0],shortcutk[1]) 
                endshortcut = Judgmentshortcut(shortcutk[2],shortcutk[3])
                if startshortcut[0] != endshortcut[0] or startshortcut[1] != endshortcut[1]: 
                    shortcut_key_start(*startshortcut)
                    shortcut_key_stop(*endshortcut)
                    break
setup = threading.Thread(target=setup)
setup.start()
def start_listener():
    record_key = []
    def on_press(key):
        global A_startcombo , B_startcombo , A_endcombo , B_endcombo
        try: 
            record_key.append(str(key))
            if len(record_key) == 2:
                if str(A_startcombo) == record_key[0] and str(B_startcombo) == record_key[1]:SetupComplete()
                elif str(A_endcombo) == record_key[0] and str(B_endcombo) == record_key[1]:stopLoop()    
        except AttributeError:
            pass
    def on_release(key):
        try:
            if len(record_key) > 1:
                record_key.clear()
        except AttributeError:
            pass
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        time.sleep(0.01)
        listener.join()
listener_thread = threading.Thread(target=start_listener)
listener_thread.start()
def SetupComplete():
    global stop , MS , KS
    stop = True
    
    try:
        if combospeed != 0 and button != 'none' and MS:
            Mcombo = threading.Thread(target=MouseRunning,args=(combospeed,button))
            Mcombo.start()
        elif combospeed != 0 and keyboardK.count('none') != 5 and KS:
            Kcombo = threading.Thread(target=keyboardRunning,args=(combospeed,*keyboardK))
            Kcombo.start()
    except NameError:
        messagebox.showerror("設置錯誤", "請設置間隔\n或啟用點擊")
global clickstatu
clickstatu = True
def clickstart(combospeed,button):
    global stop , clickstatu 
    clickstatu = False        
    while stop:               
        time.sleep(combospeed)
        pyautogui.click(x=None, y=None, interval=0 , clicks=numberofclicks(combospeed) , button=button)
    clickstatu = True
def MouseRunning(combospeed,button):
    global stop , clickstatu
    while stop:         
        time.sleep(0.01)
        if clickstatu:  
            click = threading.Thread(target=clickstart,args=(combospeed,button)) 
            click.start()
        while not stop:
            sys.exit(1)  
def Keyboarclickstart(combospeed,*button):
    global stop , clickstatu

    clickstatu = False
    if button.count('none') == 4:
        while stop:
            time.sleep(combospeed)
            pyautogui.press([button[0]])
    elif button.count("none") == 3:
        while stop:
            time.sleep(combospeed)
            pyautogui.press([button[0],button[1]])
    elif button.count("none") == 2:
        while stop:
            time.sleep(combospeed)
            pyautogui.press([button[0],button[1],button[2]])
    elif button.count("none") == 1:
        while stop:
            time.sleep(combospeed)
            pyautogui.press([button[0],button[1],button[2],button[3]])
    elif button.count("none") == 0:
        while stop:
            time.sleep(combospeed)
            pyautogui.press([button[0],button[1],button[2],button[3],button[4]])
    clickstatu = True
def keyboardRunning(combospeed,*button):
    global stop , clickstatu
    while stop:
        time.sleep(0.01)
        if clickstatu:
            Keyboarclick = threading.Thread(target=Keyboarclickstart,args=(combospeed,*button)) 
            Keyboarclick.start()
        while not stop:
            sys.exit(1)
def SaveSettings():
    global A_startcombo , B_startcombo , A_endcombo , B_endcombo , MS , KS
    combospeed
    button
    keyboardK
    save = {    
            "UserSettings":{
                    "IntervalSpeed":    combospeed,
                    "StartShortcutKeyA":OutputConversion(str(A_startcombo)),
                    "StartShortcutKeyB":OutputConversion(str(B_startcombo)),
                    "EndShortcutKeyA":  OutputConversion(str(A_endcombo)),
                    "EndShortcutKeyB":  OutputConversion(str(B_endcombo)),
                    "MouseEnabled":     MS,
                    "keyboardEnabled":  KS,
                    "MouseButton":      button,
                    "KeyboardKeys": {
                        "keyboardA" :   str(keyboardK[0]),
                        "keyboardB" :   str(keyboardK[1]),
                        "keyboardC" :   str(keyboardK[2]),
                        "keyboardD" :   str(keyboardK[3]),
                        "keyboardE" :   str(keyboardK[4])
                    }
                }
            }
    output = json.dumps(save, indent=4 , separators=(',',': '))
    with open('./settings.json', 'w') as f: f.write(output)
    messagebox.showinfo("保存設置", "\b\b保存成功\n\n預設為程式目錄下")
def Intervals(unit,time):
    value = time.get()
    if value != "" and value.isdigit():
        match unit:
            case "Hour":
                if int(value) <= 24:
                    IntervalsT[0] = value
                else:messagebox.showerror("無效的間隔設置", "小時最大值為24")
            case "Minute":
                if int(value) <= 60:
                    IntervalsT[1] = value
                else:messagebox.showerror("無效的間隔設置", "分鐘最大值為60")
            case "Seconds":
                if int(value) <= 60:
                    IntervalsT[2] = value
                else:messagebox.showerror("無效的間隔設置", "秒鐘最大值為60")
            case "Tenthofasecond":
                if int(value) <= 9:
                    IntervalsT[3] = value
                else:messagebox.showerror("無效的間隔設置", "1/10最大值為9")
            case "Hundredthsofasecond":
                if int(value) <= 9:
                    IntervalsT[4] = value
                else:messagebox.showerror("無效的間隔設置", "1/100最大值為9")
    elif value == "":pass
    else:messagebox.showerror("無效的間隔設置", "你要確定你輸入的是數字ㄟ")
def shortcutkey(state,key):
    match state:
        case "S1":
            shortcutk[0] = key
        case "S2":
            shortcutk[1] = key
        case "E1":
            shortcutk[2] = key
        case "E2":
            shortcutk[3] = key
def MouseSwitch(state):
        global MS , KS
        MS = state
        KS = False
        MouseB[0] = MouseBcache[0]
        for i in range(len(keyboardK)):
            keyboardK[i] = 'none'
def keyboardSwitch(state):
        global KS , MS
        KS = state
        MS = False
        MouseB[0] = 'none'
        for i in range(len(keyboardKcache)):
            keyboardK[i] = keyboardKcache[i]
def MouseButton(key):
    if MS:
        match key:
            case "無":
                key = "none"
                MouseB[0] = key
            case "右鍵":
                key = "right"
                MouseB[0] = key
            case "左鍵":
                key = "left"
                MouseB[0] = key
    MouseBcache[0] = MouseB[0]
def keyboardkey(unit,key):
    value = key.get()
    if KS:
        match unit:
            case "keybA":
                keyboardK[0] = value
            case "keybB":
                keyboardK[1] = value
            case "keybC":
                keyboardK[2] = value
            case "keybD":
                keyboardK[3] = value
            case "keybE":
                keyboardK[4] = value
    for i in range(len(keyboardK)):
        keyboardKcache[i] = keyboardK[i]
global State
State = False
def ArchiveRead(save,state):
    global Save , State
    Save = save
    State = state
def InitialGUI():
    global Save , State
    root = tk.Tk()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(current_dir,'click.ico')
    warnings.filterwarnings("ignore", message="Image was not the expected size", category=UserWarning)
    image = Image.open(icon_path)
    image = image.resize((64, 64))
    titleImage = ImageTk.PhotoImage(image)
    root.iconphoto(True, titleImage)
    root.title("遊俠牌自動連點器 v1.0 GUI")
    root.geometry("400x280")
    root.geometry("+640+320")
    root.protocol("WM_DELETE_WINDOW",Clos)
    root.wm_attributes('-topmost', True)
    root.resizable(False, False)
    root.configure(background='#C6DCE4')
    root.tk_setPalette(background='#F2D1D1')
    TextColor = "#00235B"
    TextBackgroundColor = "#FFE6E6"
    MarqueeHighlight = "#DAEAF1"
    MarqueeHighlight2 = "#C6DCE4"
    AreaBoxColor = "#FFE6E6"
    BorderColor = "#BE6DB7"
    frame_width = 390
    frame_height = 230
    frame_x = 5
    frame_y = 15
    frame = tk.Canvas(root, width=frame_width , height=frame_height, bd=0, highlightthickness=0 , bg=AreaBoxColor)
    frame.place(x=frame_x, y=frame_y)
    frame.create_rectangle(0,0,frame_width, frame_height, width=1.5 ,outline=BorderColor)
    SpeedBox_width = frame_width-10
    SpeedBox_height = frame_height-160
    SpeedBox = tk.Canvas(frame, width=SpeedBox_width, height=SpeedBox_height, bd=0 , highlightthickness=0 , bg=AreaBoxColor)
    SpeedBox.place(x=frame_x, y=frame_y-10)
    SpeedBox.create_rectangle(0,0,SpeedBox_width,SpeedBox_height,width=1.5,outline=BorderColor,dash=(5,5))
    ShortcutBox_width = frame_width-202.5
    ShortcutBox_height = frame_height-155
    ShortcutBox = tk.Canvas(frame, width=ShortcutBox_width , height=ShortcutBox_height, bd=0, highlightthickness=0 , bg=AreaBoxColor)
    ShortcutBox.place(x=frame_x, y=frame_y+65)
    ShortcutBox.create_rectangle(0,0,ShortcutBox_width,ShortcutBox_height,width=1.5 ,outline=BorderColor)
    MouseBox_width = frame_width-202.5
    MouseBox_height = frame_height-155
    MouseBox = tk.Canvas(frame, width=MouseBox_width , height=MouseBox_height, bd=0, highlightthickness=0 , bg=AreaBoxColor)
    MouseBox.place(x=frame_x+192, y=frame_y+65)
    MouseBox.create_rectangle(0,0,MouseBox_width,MouseBox_height,width=1.5 ,outline=BorderColor)
    keyboardBox_width = frame_width-10
    keyboardBox_height = frame_height-167
    keyboardBox = tk.Canvas(frame, width=keyboardBox_width , height=keyboardBox_height , bd=0 , highlightthickness=0 , bg = AreaBoxColor)
    keyboardBox.place(x=frame_x, y=frame_y+145)
    keyboardBox.create_rectangle(0,0,keyboardBox_width,keyboardBox_height,width=1.5 ,outline=BorderColor)
    BBH = 249
    startbutton = tk.Button(root, text="開始運行" , command=SetupComplete)
    startbutton.config(font=("Arial Bold", 10), fg=TextColor , bg=TextBackgroundColor)
    startbutton.place(x=91,y=BBH)
    stopbutton = tk.Button(root, text="中止運行" , command=stopLoop)
    stopbutton.config(font=("Arial Bold", 10), fg=TextColor , bg=TextBackgroundColor)
    stopbutton.place(x=166,y=BBH)
    savebutton = tk.Button(root, text="保存設置",command=SaveSettings)
    savebutton.config(font=("Arial Bold", 10), fg=TextColor , bg=TextBackgroundColor)
    savebutton.place(x=241,y=BBH)
    label = tk.Label(root, text="點擊間隔")
    label.config(font=("Arial Bold", 11), fg=TextColor , bg=TextBackgroundColor)
    label.place(in_=frame, x=frame_x+10, y=frame_y-23)
    timeV = (root.register(Validateinseconds), "%P")
    HourT = tk.Label(root, text="小時")
    HourT.config(font=("Arial Bold", 10), fg=TextColor , bg=TextBackgroundColor)
    HourT.place(in_=SpeedBox, x=frame_x+15, y=frame_y-3)
    Hour = tk.Entry(root, font=("Microsoft Positive Bold", 12), width=5 , justify='center',borderwidth=3, highlightthickness=2.5, highlightcolor=MarqueeHighlight, validate="key", validatecommand=timeV)
    Hour.bind("<KeyRelease>", lambda event, unit=Hour: Intervals("Hour", unit))
    Hour.place(in_=SpeedBox, x=frame_x+5, y=frame_y+20)
    MinuteT = tk.Label(root, text="分鐘")
    MinuteT.config(font=("Arial Bold", 10), fg=TextColor , bg=TextBackgroundColor)
    MinuteT.place(in_=SpeedBox, x=frame_x+75, y=frame_y-3)
    Minute = tk.Entry(root, font=("Microsoft Positive Bold", 12), width=5 , justify='center',borderwidth=3, highlightthickness=2.5, highlightcolor=MarqueeHighlight, validate="key", validatecommand=timeV)
    Minute.bind("<KeyRelease>", lambda event, unit=Minute: Intervals("Minute", unit))
    Minute.place(in_=SpeedBox, x=frame_x+65, y=frame_y+20)
    SecondsT = tk.Label(root, text="秒數")
    SecondsT.config(font=("Arial Bold", 10), fg=TextColor , bg=TextBackgroundColor)
    SecondsT.place(in_=SpeedBox, x=frame_x+135, y=frame_y-3)
    Seconds = tk.Entry(root, font=("Microsoft Positive Bold", 12), width=5 , justify='center',borderwidth=3, highlightthickness=2.5, highlightcolor=MarqueeHighlight, validate="key", validatecommand=timeV)
    Seconds.bind("<KeyRelease>", lambda event, unit=Seconds: Intervals("Seconds", unit))
    Seconds.place(in_=SpeedBox, x=frame_x+125, y=frame_y+20)
    TenthofasecondT = tk.Label(root, text="1/10秒")
    TenthofasecondT.config(font=("Arial Bold", 10), fg=TextColor , bg=TextBackgroundColor)
    TenthofasecondT.place(in_=SpeedBox, x=frame_x+190, y=frame_y-3)
    Tenthofasecond = tk.Entry(root, font=("Microsoft Positive Bold", 12), width=5 , justify='center',borderwidth=3, highlightthickness=2.5, highlightcolor=MarqueeHighlight, validate="key", validatecommand=timeV)
    Tenthofasecond.bind("<KeyRelease>", lambda event, unit=Tenthofasecond: Intervals("Tenthofasecond", unit))
    Tenthofasecond.place(in_=SpeedBox, x=frame_x+185, y=frame_y+20)
    HundredthsofasecondT = tk.Label(root, text="1/100秒")
    HundredthsofasecondT.config(font=("Arial Bold", 10), fg=TextColor , bg=TextBackgroundColor)
    HundredthsofasecondT.place(in_=SpeedBox, x=frame_x+247, y=frame_y-3)
    Hundredthsofasecond = tk.Entry(root, font=("Microsoft Positive Bold", 12), width=5 , justify='center',borderwidth=3, highlightthickness=2.5, highlightcolor=MarqueeHighlight, validate="key", validatecommand=timeV)
    Hundredthsofasecond.bind("<KeyRelease>", lambda event, unit=Hundredthsofasecond: Intervals("Hundredthsofasecond", unit))
    Hundredthsofasecond.place(in_=SpeedBox, x=frame_x+245, y=frame_y+20)
    if State:
            Timeformat , Timefigures = Timeformatconversion(Save['UserSettings']['IntervalSpeed']) #獲取轉換後的時間格式
            match Timeformat:
                case "h":
                    Hour.insert(0,Timefigures)
                case "m":
                    Minute.insert(0,Timefigures)
                case "s":
                    Seconds.insert(0,Timefigures)
                case "t":
                    Tenthofasecond.insert(0,Timefigures)
                case "H":
                    Hundredthsofasecond.insert(0,Timefigures)
    def unblock():
        key = tk.Toplevel(root)
        key.geometry("220x150+{}+{}".format(int((root.winfo_screenwidth() / 2) - (220 / 2)), int((root.winfo_screenheight() / 2) - (150 / 2))))
        key.title("功能解鎖")
        def verify():
            send_button['state'] = 'disabled'
            for i in range(101):
                bar['value'] = i
                val.set(f'{i}%')
                root.update()
                time.sleep(0.01)
            send_button['state'] = 'normal'
            Authentication(key_entry.get())
            key.destroy()
        val = tk.StringVar()
        val.set('0%')
        label = tk.Label(key, textvariable=val)
        label.place(x=20,y=3)
        bar = ttk.Progressbar(key, mode='determinate')
        bar.pack(pady=3)
        key_label = tk.Label(key, text="請輸入你的 Key:", font=("Arial Bold", 12), fg=TextColor)
        key_label.pack(pady=10)
        key_entry = tk.Entry(key,font=("Arial", 10), width=20)
        key_entry.pack(pady=5)
        button_frame = tk.Frame(key)
        button_frame.place(in_=key,x=50,y=110)
        send_button = tk.Button(button_frame, text="送出", command=verify , font=("Arial Bold", 10), fg=TextColor, bg=TextBackgroundColor)
        send_button.pack(side="left", padx=10)
        cancel_button = tk.Button(button_frame, text="取消", font=("Arial Bold", 10), fg=TextColor, bg=TextBackgroundColor, command=key.destroy)
        cancel_button.pack(side="left", padx=10)
    ReservedT = tk.Label(root, text="功能解鎖")
    ReservedT.config(font=("Arial Bold", 10), fg=TextColor , bg=TextBackgroundColor)
    ReservedT.place(in_=SpeedBox, x=frame_x+305, y=frame_y-3)
    Reserved = tk.Button(root, text="解鎖",command=unblock)
    Reserved.config(font=("Arial Bold", 10), fg=TextColor , bg=TextBackgroundColor)
    Reserved.place(in_=SpeedBox,x=frame_x+315,y=frame_y+20)
    startshortcut = tk.Label(root, text="開始快捷:")
    startshortcut.config(font=("Arial Bold", 10), fg=TextColor , bg=TextBackgroundColor)
    startshortcut.place(in_=ShortcutBox, x=frame_x, y=frame_y-6)
    endshortcut = tk.Label(root, text="結束快捷:")
    endshortcut.config(font=("Arial Bold", 10), fg=TextColor , bg=TextBackgroundColor)
    endshortcut.place(in_=ShortcutBox, x=frame_x, y=frame_y+28)
    def S1(*Key):
        value = S_shortcutkey1_option.get()
        shortcutkey("S1",value)
    S_shortcutkey1 = ["Ctrl", "Alt", "Shift"]
    S_shortcutkey1_option = tk.StringVar()
    S_shortcutkey1_option.trace('w',S1)
    dropdown = tk.OptionMenu(ShortcutBox, S_shortcutkey1_option,*S_shortcutkey1)
    dropdown.config(width=3, fg=TextColor , bg=TextBackgroundColor)
    dropdown.place(x=70, y=5)
    S_shortcutkey2 = ttk.Combobox(ShortcutBox, values=["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"])
    S_shortcutkey2.configure(width=3, height=6, foreground=TextColor, background=TextBackgroundColor, state="readonly")
    S_shortcutkey2.bind("<<ComboboxSelected>>", lambda event: shortcutkey("S2",S_shortcutkey2.get()))
    S_shortcutkey2.place(x=139, y=11)
    def E1(*Key):
        value = E_shortcutkey1_option.get()
        shortcutkey("E1",value)
    E_shortcutkey1 = ["Ctrl", "Alt", "Shift"]
    E_shortcutkey1_option = tk.StringVar()
    E_shortcutkey1_option.trace('w',E1)
    dropdown = tk.OptionMenu(ShortcutBox, E_shortcutkey1_option,*E_shortcutkey1)
    dropdown.config(width=3, fg=TextColor , bg=TextBackgroundColor)
    dropdown.place(x=70, y=40)
    E_shortcutkey2 = ttk.Combobox(ShortcutBox, values=["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"])
    E_shortcutkey2.configure(width=3, height=6, foreground=TextColor, background=TextBackgroundColor, state="readonly")
    E_shortcutkey2.bind("<<ComboboxSelected>>", lambda event: shortcutkey("E2",E_shortcutkey2.get()))
    E_shortcutkey2.place(x=139, y=45)
    if State:
        S_shortcutkey1_option.set(Save['UserSettings']['StartShortcutKeyA'])
        S_shortcutkey2.set(Save['UserSettings']['StartShortcutKeyB'])
        E_shortcutkey1_option.set(Save['UserSettings']['EndShortcutKeyA'])
        E_shortcutkey2.set(Save['UserSettings']['EndShortcutKeyB'])
    else:
        S_shortcutkey1_option.set(S_shortcutkey1[1])
        S_shortcutkey2.set("F1")
        E_shortcutkey1_option.set(E_shortcutkey1[1])
        E_shortcutkey2.set("F2")
    def mouse(*Key):
        value = mousebutton_option.get()
        MouseButton(value)
    mousebutton = ["無","右鍵","左鍵"]
    mousebutton_option = tk.StringVar()
    mousebutton_option.set(mousebutton[0])
    mousebutton_option.trace('w',mouse)
    mouseoption = tk.OptionMenu(MouseBox, mousebutton_option, *mousebutton)
    mouseoption.config(width=3, fg=TextColor, bg=TextBackgroundColor , state='disabled')
    mouseoption.place(x=110, y=37)
    mousedefault = tk.BooleanVar(value=False)
    keyboarddefault = tk.BooleanVar(value=False)
    def enablemouse():
        MouseSwitch(True)
        mouseoption.config(state='normal')
        keyboard_AT.config(state='disabled')
        keyboard_A.config(state='disabled')
        keyboard_BT.config(state='disabled')
        keyboard_B.config(state='disabled')
        keyboard_CT.config(state='disabled')
        keyboard_C.config(state='disabled')
        keyboard_DT.config(state='disabled')
        keyboard_D.config(state='disabled')
        keyboard_ET.config(state='disabled')
        keyboard_E.config(state='disabled')
        keyboarddefault.set(False)
    def enablekeyboard():
        keyboardSwitch(True)
        mouseoption.config(state='disabled')
        keyboard_AT.config(state='normal')
        keyboard_A.config(state='normal')
        keyboard_BT.config(state='normal')
        keyboard_B.config(state='normal')
        keyboard_CT.config(state='normal')
        keyboard_C.config(state='normal')
        keyboard_DT.config(state='normal')
        keyboard_D.config(state='normal')
        keyboard_ET.config(state='normal')
        keyboard_E.config(state='normal')
        mousedefault.set(False)
    mouserad = tk.Radiobutton(MouseBox, text="啟用滑鼠連點", variable=mousedefault , command=enablemouse)
    mouserad.config(fg=TextColor, bg=TextBackgroundColor)
    mouserad.place(x=5, y=8)
    keyboardrad = tk.Radiobutton(MouseBox, text="啟用鍵盤連點", variable=keyboarddefault , command=enablekeyboard)
    keyboardrad.config(fg=TextColor, bg=TextBackgroundColor)
    keyboardrad.place(x=5, y=40)
    mouseoptionT = tk.Label(root, text="按鍵選擇")
    mouseoptionT.config(font=("Arial Bold", 10), fg=TextColor , bg=TextBackgroundColor)
    mouseoptionT.place(in_=MouseBox, x=110, y=8)
    keyboard_AT = tk.Label(root, text="鍵盤自訂1")
    keyboard_AT.config(font=("Arial Bold", 10), fg=TextColor , bg=TextBackgroundColor, state='disabled')
    keyboard_AT.place(in_=keyboardBox, x=frame_x, y=frame_y-13)
    keyboard_A = tk.Entry(root, font=("Microsoft Positive Bold", 12), width=5 , justify='center',borderwidth=3, highlightthickness=2.5, highlightcolor=MarqueeHighlight2)
    keyboard_A.config(state='disabled')
    keyboard_A.place(in_=keyboardBox, x=frame_x+4, y=frame_y+10)
    keyboard_A.bind("<KeyRelease>", lambda event, unit=keyboard_A: keyboardkey("keybA", unit))
    def keyA(event):
        if event.keycode in []:return
        keyboard_A.config(state='normal')
        keyboard_A.delete(0, 'end')
        keyboard_A.insert(0, event.char)
        keyboard_A.config(state='readonly')
    keyboard_BT = tk.Label(root, text="鍵盤自訂2")
    keyboard_BT.config(font=("Arial Bold", 10), fg=TextColor , bg=TextBackgroundColor, state='disabled')
    keyboard_BT.place(in_=keyboardBox, x=frame_x+70, y=frame_y-13)
    keyboard_B = tk.Entry(root, font=("Microsoft Positive Bold", 12), width=5 , justify='center',borderwidth=3, highlightthickness=2.5, highlightcolor=MarqueeHighlight2)
    keyboard_B.config(state='disabled')
    keyboard_B.place(in_=keyboardBox, x=frame_x+74, y=frame_y+10)
    keyboard_B.bind("<KeyRelease>", lambda event, unit=keyboard_B: keyboardkey("keybB", unit))
    def keyB(event):
        if event.keycode in []:return
        keyboard_B.config(state='normal')
        keyboard_B.delete(0, 'end')
        keyboard_B.insert(0, event.char)
        keyboard_B.config(state='readonly')
    keyboard_CT = tk.Label(root, text="鍵盤自訂3")
    keyboard_CT.config(font=("Arial Bold", 10), fg=TextColor , bg=TextBackgroundColor, state='disabled')
    keyboard_CT.place(in_=keyboardBox, x=frame_x+140, y=frame_y-13)
    keyboard_C = tk.Entry(root, font=("Microsoft Positive Bold", 12), width=5 , justify='center',borderwidth=3, highlightthickness=2.5, highlightcolor=MarqueeHighlight2)
    keyboard_C.config(state='disabled')
    keyboard_C.place(in_=keyboardBox, x=frame_x+144, y=frame_y+10)
    keyboard_C.bind("<KeyRelease>", lambda event, unit=keyboard_C: keyboardkey("keybC", unit))
    def keyC(event):
        if event.keycode in []:return
        keyboard_C.config(state='normal')
        keyboard_C.delete(0, 'end')
        keyboard_C.insert(0, event.char)
        keyboard_C.config(state='readonly')
    keyboard_DT = tk.Label(root, text="鍵盤自訂4")
    keyboard_DT.config(font=("Arial Bold", 10), fg=TextColor , bg=TextBackgroundColor, state='disabled')
    keyboard_DT.place(in_=keyboardBox, x=frame_x+210, y=frame_y-13)
    keyboard_D = tk.Entry(root, font=("Microsoft Positive Bold", 12), width=5 , justify='center',borderwidth=3, highlightthickness=2.5, highlightcolor=MarqueeHighlight2)
    keyboard_D.config(state='disabled')
    keyboard_D.place(in_=keyboardBox, x=frame_x+214, y=frame_y+10)
    keyboard_D.bind("<KeyRelease>", lambda event, unit=keyboard_D: keyboardkey("keybD", unit))
    def keyD(event):
        if event.keycode in []:return
        keyboard_D.config(state='normal')
        keyboard_D.delete(0, 'end')
        keyboard_D.insert(0, event.char)
        keyboard_D.config(state='readonly')
    keyboard_ET = tk.Label(root, text="鍵盤自訂5")
    keyboard_ET.config(font=("Arial Bold", 10), fg=TextColor , bg=TextBackgroundColor, state='disabled')
    keyboard_ET.place(in_=keyboardBox, x=frame_x+280, y=frame_y-13)
    keyboard_E = tk.Entry(root, font=("Microsoft Positive Bold", 12), width=5 , justify='center',borderwidth=3, highlightthickness=2.5, highlightcolor=MarqueeHighlight2)
    keyboard_E.config(state='disabled')
    keyboard_E.place(in_=keyboardBox, x=frame_x+284, y=frame_y+10)
    keyboard_E.bind("<KeyRelease>", lambda event, unit=keyboard_E: keyboardkey("keybE", unit))
    def keyE(event):
        if event.keycode in []:return
        keyboard_E.config(state='normal')
        keyboard_E.delete(0, 'end')
        keyboard_E.insert(0, event.char)
        keyboard_E.config(state='readonly')       
    if State:
        if Save['UserSettings']['MouseEnabled']:
            mouserad.select()
            enablemouse()
            mousebutton_option.set(ButtonNameConversion(Save['UserSettings']['MouseButton']))
        elif Save['UserSettings']['keyboardEnabled']:
            keyboardrad.select()
            enablekeyboard()
            keyboard_A.insert(0,Save['UserSettings']['KeyboardKeys']['keyboardA'])
            keyboard_B.insert(0,Save['UserSettings']['KeyboardKeys']['keyboardB'])
            keyboard_C.insert(0,Save['UserSettings']['KeyboardKeys']['keyboardC'])
            keyboard_D.insert(0,Save['UserSettings']['KeyboardKeys']['keyboardD'])
            keyboard_E.insert(0,Save['UserSettings']['KeyboardKeys']['keyboardE'])
    keyboard_A.bind('<Key>', keyA)
    keyboard_B.bind('<Key>', keyB)
    keyboard_C.bind('<Key>', keyC)
    keyboard_D.bind('<Key>', keyD)
    keyboard_E.bind('<Key>', keyE)
    if State:
        BackendArchiveRead(Save)
    root.mainloop()
settings = []
SetVerification = {
    "ShortcutKeyA": ['Ctrl','Alt','Shift'],
    "ShortcutKeyB": ["F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12"],
    "MouseButton": ["left", "right","none"],
}
class InvalidIntervalSpeed(Exception):
    pass
class ShortcutKeySettingError(Exception):
    pass
class WrongMouseButtons(Exception):
    pass
try:  
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    if settings["UserSettings"]["IntervalSpeed"] < 0.01:
        raise InvalidIntervalSpeed()
    if settings["UserSettings"]["StartShortcutKeyA"] not in SetVerification["ShortcutKeyA"] or settings["UserSettings"]["EndShortcutKeyA"] not in SetVerification["ShortcutKeyA"]:
        raise ShortcutKeySettingError()
    if settings["UserSettings"]["StartShortcutKeyB"] not in SetVerification["ShortcutKeyB"] or settings["UserSettings"]["EndShortcutKeyB"] not in SetVerification["ShortcutKeyB"]:
        raise ShortcutKeySettingError()
    if settings["UserSettings"]["MouseButton"] not in SetVerification["MouseButton"]:
        raise WrongMouseButtons()
    Archive = True
    ArchiveRead(settings,Archive)
except InvalidIntervalSpeed:
    messagebox.showerror("設置錯誤", "你設置了無效的間隔速度")
except ShortcutKeySettingError:
    messagebox.showerror("設置錯誤", "你設置了無效的快捷鍵")
except WrongMouseButtons:
    messagebox.showerror("設置錯誤", "你設置了無效滑鼠按鍵")
except FileNotFoundError:
    Archive = False
    ArchiveRead(settings,Archive)
except:
    messagebox.showerror("設置錯誤", "請不要亂改設置檔\n即將刪除你的設置檔")
    os.system("del /f /s /q settings.json >nul 2>&1")
finally:
    InitialGUI()