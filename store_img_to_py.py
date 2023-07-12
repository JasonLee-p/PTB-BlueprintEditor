"""
    This file is used to store images in the PTB-BlueprintReader app.
"""

import base64
import os

if __name__ == '__main__':
    # 删除旧的store_img_to_py.py
    if os.path.exists('IMGS.py'):
        os.remove('IMGS.py')
    # 检索imgs文件夹下的所有图片
    with open('IMGS.py', 'a') as f:
        f.write('"""This file is used to store images in the PTB-BlueprintReader app."""\n\n')
        for root, dirs, files in os.walk('images'):
            for file in files:
                if file.endswith('.png'):
                    with open(os.path.join(root, file), 'rb') as img:
                        img_base64 = base64.b64encode(img.read())
                        f.write(f'{file[:-4]} = {img_base64}\n\n')
