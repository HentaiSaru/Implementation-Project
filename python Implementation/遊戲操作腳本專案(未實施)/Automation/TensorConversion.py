import torch
import cv2
import os

path = rf"{os.path.dirname(os.path.abspath(__file__))}\Image"
file_names = os.listdir(path)


# 檢測 torch 版本 , 如果安裝到 cpu 版本會顯示 None  , 重載(https://pytorch.org/get-started/locally/)
#print(torch.version.cuda)

# 檢測是否能使用 cuda , 開發包(https://developer.nvidia.com/cuda-downloads?target_os=Windows&target_arch=x86_64)
#print(torch.cuda.is_available())

tensor_list = []

# for file_name in file_names:
#     img_path = os.path.join(path,file_name).split("\\")[-1]
#     img = cv2.imread(img_path,cv2.IMREAD_GRAYSCALE)
#     tensor_img = torch.from_numpy(img).permute(2, 0, 1).float() / 255.0
#     tensor_list.append(tensor_img)

# torch.save(tensor_list, r'\Image\Data.pt')