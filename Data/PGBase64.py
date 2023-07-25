import base64
import os
import zlib

if __name__ == '__main__':
    with open('E:/JasonLee//python_projects/PTB-BlueprintEditor/dist/main.exe', 'rb') as f:
        # 读取exe文件，把编码尽量压缩到最小
        data = zlib.compress(f.read(), 9)
        # 把压缩后的数据编码为base64
        data = base64.b64encode(data)
    # 获取原文件大小
    size = os.path.getsize('PROGRAM.py')
    # 存入PROGRAM.py文件
    with open('PROGRAM.py', 'w') as f:
        # 读取原文件大小
        print(f"原文件大小：{size}字节")
        # 清除原有内容
        f.truncate()
        # 写入新内容
        f.write(f'PGM = {data}')
    print(f"新文件大小：{os.path.getsize('PROGRAM.py')}字节")
