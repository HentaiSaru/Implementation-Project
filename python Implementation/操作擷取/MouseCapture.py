from pynput import mouse
import time

class capture():
    def __init__(self):
        self.Button = None
        self.press_time = None
        self.letgo_time = None

    def click(self, x, y, button, pressed):
        left = "左鍵"
        right = "右鍵"
        middle = "中鍵"

        if pressed:
            self.press_time = time.time()
            self.Button = str(button).split("Button.")[1]
            print(f"按下了：{eval(self.Button)}")
        else:
            self.letgo_time = time.time()
            print(f"按放開了：{eval(self.Button)} , 持續時間 : {self.letgo_time-self.press_time}")

    def move(self, x, y):
        print(f"X座標:{x} , Y座標:{y}")

class Mouse:
    def __init__(self):
        self.Delay = 10
        self.listener = None

    def __call__(self):
        cap = capture()
        self.listener = mouse.Listener(on_click=cap.click,on_move=cap.move).start()
        self.run()

    def run(self):
        try:
            while True:
                time.sleep(self.Delay)
        except KeyboardInterrupt:
            self.listener.stop()
            pass