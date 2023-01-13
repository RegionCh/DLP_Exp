import shutil
import os
from PIL import Image
import PIL.ImageOps 
import numpy as np


# base = Image.open(r'inputs\benign\benign (424)_mask.png')
# base = np.array(base)
## region = Image.open(r'inputs\benign\benign (424)_mask_1.png').convert('1')
## region = np.array(region)
# img = np.logical_or(base,region)
# img = Image.fromarray(img)
# img.show()
# img.save(r'inputs\benign\benign (424)_mask.png')

a = os.listdir(r'inputs\benign')
for filename in a:
    if filename == 'images' or filename == 'masks':
        continue
    if filename.find('mask') == -1:
        num = filename[filename.find('(')+1:filename.find(')')].zfill(3)
        Src = 'inputs\\benign\\' + filename
        Dst = 'inputs\\benign\\images\\' + num + '.png'
        shutil.copy(Src,Dst)
        os.unlink(Src)
    
    else:
        num = filename[filename.find('(')+1:filename.find(')')].zfill(3)
        Src = 'inputs\\benign\\' + filename
        Dst = 'inputs\\benign\\masks\\0\\' + num + '.png'
        shutil.copy(Src,Dst)
        os.unlink(Src)

        