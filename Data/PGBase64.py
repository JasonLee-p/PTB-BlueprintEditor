import base64
import os

if __name__ == '__main__':
    with open('E:/JasonLee//python_projects/PTB-BlueprintEditor/dist/main.exe', 'rb') as f:
        # 用base64把exe编码成字符串
        data = base64.b64encode(f.read())
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

