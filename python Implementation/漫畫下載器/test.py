import requests
import os
dir = os.path.abspath("R:/") # 可更改預設路徑
os.chdir(dir)

header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
}

def Download(Path,SaveName,Image_URL,headers):

        ImageData = requests.get(Image_URL, headers=headers)
        if ImageData.status_code == 200:
            with open(SaveName,"wb") as f:
                f.write(ImageData.content)

Download(dir,"測試.jpg","",header)