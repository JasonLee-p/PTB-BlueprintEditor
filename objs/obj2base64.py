"""
    This file is used to store images in the PTB-BlueprintReader app.
"""

import base64
import os
import Data.PartAttrMaps as PAM

if __name__ == '__main__':
    # 删除旧的
    if os.path.exists('OBJS.py'):
        os.remove('OBJS.py')
    # 检索Mesh文件夹下第一层的所有图片
    with open('OBJS.py', 'a') as f:
        f.write('"""This file is used to store 3D obj files in the PTB-BlueprintReader app."""\n\n')
        _all_vars = []
        # 只找Mesh内的文件
        for file in os.listdir('./Mesh'):
            in_weapon = False
            if file.endswith('.obj'):
                for weapon in PAM.PartType11.keys():
                    if weapon in file:
                        in_weapon = True
                        break
                if not in_weapon:
                    continue
                # 获取文件大小：
                size = os.path.getsize(os.path.join(os.getcwd(), "Mesh", file))
                if size > 300000:
                    print(f'文件{file}过大，已跳过')
                    continue
                if size < 50000:
                    print(f'文件{file}过小，已跳过')
                    continue
                with open(os.path.join(os.getcwd(), "Mesh", file), 'rb') as obj:
                    obj_base64 = base64.b64encode(obj.read())
                    file = file.replace(' ', '_')
                    file = file.replace('#', '_')
                    file = file.replace('-', '_')
                    file = file.replace('(', '_')
                    file = file.replace(')', '_')
                    file = file.replace('（', '_')
                    file = file.replace('）', '_')
                    f.write(f'O{file[:-4]} = {obj_base64}\n\n')
                    _all_vars.append(f'O{file[:-4]}')
        f.write("ALL = [\n")
        for var in _all_vars:
            f.write(f"    '{var}',\n")
        f.write("]\n")
    print('Done!')
