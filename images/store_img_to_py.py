"""
    This file is used to store images in the PTB-BlueprintReader app.
"""

import base64
import os

if __name__ == '__main__':
    # 删除旧的
    if os.path.exists('Img_main.py'):
        os.remove('Img_main.py')
    if os.path.exists('Img_special.py'):
        os.remove('Img_special.py')
    if os.path.exists('Img_shipType.py'):
        os.remove('Img_shipType.py')
    if os.path.exists('Img_mainWeapon.py'):
        os.remove('Img_mainWeapon.py')
    # 检索images文件夹下第一层的所有图片
    with open('Img_main.py', 'a') as f:
        f.write('"""This file is used to store images in the PTB-BlueprintReader app."""\n\n')
        # 只找images内的文件
        for file in os.listdir('./'):
            if file.endswith('.png'):
                with open(file, 'rb') as img:
                    img_base64 = base64.b64encode(img.read())
                    f.write(f'{file[:-4]} = {img_base64}\n\n')
    # Special（特化类型）的图片
    with open('Img_special.py', 'a') as f:
        f.write('"""This file is used to store ships specials images in the PTB-BlueprintReader app."""\n\n')
        # 只找images内的文件
        root = './Special'
        for file in os.listdir('./Special'):
            if file.endswith('.png'):
                with open(os.path.join(root, file), 'rb') as img:
                    img_base64 = base64.b64encode(img.read())
                    f.write(f'{file[:-4]} = {img_base64}\n\n')
    # ShipType（船型）的图片
    with open('Img_shipType.py', 'a') as f:
        f.write('"""This file is used to store ships types images in the PTB-BlueprintReader app."""\n\n')
        # 只找images内的文件
        root = './ShipType'
        for file in os.listdir('./ShipType'):
            if file.endswith('.png'):
                with open(os.path.join(root, file), 'rb') as img:
                    img_base64 = base64.b64encode(img.read())
                    f.write(f'{file[:-4]} = {img_base64}\n\n')
    # MainWeapon（主武器）的图片
    with open('Img_mainWeapon.py', 'a') as f:
        f.write('"""This file is used to store ships main weapons images in the PTB-BlueprintReader app."""\n\n')
        # 只找images内的文件
        root = './MainWeapon'
        for file in os.listdir('./MainWeapon'):
            if file.endswith('.png'):
                with open(os.path.join(root, file), 'rb') as img:
                    img_base64 = base64.b64encode(img.read())
                    f.write(f'{file[:-4]} = {img_base64}\n\n')
    # OtherPart（其他部件）的图片
    with open('Img_otherPart.py', 'a') as f:
        f.write('"""This file is used to store ships other parts images in the PTB-BlueprintReader app."""\n\n')
        # 只找images内的文件
        root = './OtherPart'
        for file in os.listdir('./OtherPart'):
            if file.endswith('.png'):
                with open(os.path.join(root, file), 'rb') as img:
                    img_base64 = base64.b64encode(img.read())
                    f.write(f'{file[:-4]} = {img_base64}\n\n')
    print('Done!')
