import os

class Exit:
    def __init__(self):
        pass

    def ex(self):
        os._exit(1)

    def ex2(self):
        os.system('wmic process where name="python.exe" delete > nul')

# exit = Exit()
# exit.ex2()