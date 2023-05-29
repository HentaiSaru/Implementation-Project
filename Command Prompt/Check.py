import requests

class Check_for_updates:
    def __init__(self):
        self.url = "https://raw.githubusercontent.com/TenshinoOtoKafu/Implementation-Project/Main/Command%20Prompt/System-Cleaning.bat"
        self.text = []

    def Get_web(self):
        reques = requests.get(self.url)
        text = reques.text.split('\n')

        for line in text:
            self.text.append(line)

        print(self.text)

if __name__ == "__main__":
    check = Check_for_updates()
    check.Get_web()