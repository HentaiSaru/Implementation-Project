import torchvision.transforms as transforms
from PIL import Image
import torch
import cv2
import os

# 檢測 torch 版本 , 如果安裝到 cpu 版本會顯示 None  , 重載(https://pytorch.org/get-started/locally/)
#print(torch.version.cuda)

# 檢測是否能使用 cuda , 開發包(https://developer.nvidia.com/cuda-downloads?target_os=Windows&target_arch=x86_64)
#print(torch.cuda.is_available())

#print(torch.cuda.get_device_name())

"""
用於機器學習的,圖像張量轉換
"""

preprocess = transforms.Compose([
    transforms.RandomResizedCrop((224, 224), scale=(0.8, 1.0)),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.ColorJitter(brightness=(0, 1), contrast=(0, 1), saturation=(0, 1), hue=(-0.5, 0.5)),
    transforms.ToTensor(),
    transforms.Lambda(lambda x: x[:3]),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# 資料夾路徑
path = rf"{os.path.dirname(os.path.abspath(__file__))}\Image"
os.chdir(path)

Picturename = ""
for filename in os.listdir(path):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        template = []
        # 讀取圖片
        image_path = os.path.join(path, filename)
        image = Image.open(image_path)
        Picturename = filename.split(".")[0]
        for _ in range(10):
            # 預處理圖片
            preprocessed_image = preprocess(image)

            # 將預處理後的圖片轉換為張量，並加入張量列表中
            template_tensor = torch.unsqueeze(preprocessed_image, 0)
            template.append(template_tensor)

        # 將張量列表轉換為模板張量，即將所有張量進行串接
        template_tensor = torch.cat(template, dim=0)

        # 儲存模板張量到檔案
        torch.save(template_tensor, f'{Picturename}.pt')

merge = []
for filename in os.listdir(path):
    if filename.endswith(".pt"):
        merge.append(torch.load(filename))
        os.remove(filename)

combined_template = torch.cat(merge, dim=0)
torch.save(combined_template, 'final.pt')