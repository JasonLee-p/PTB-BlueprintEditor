import base64

if __name__ == '__main__':
    with open('dist/main.exe', 'rb') as f:
        # 用base64把exe编码成字符串
        data = base64.b64encode(f.read())
        # 存入PROGRAM.py文件
    with open('PROGRAM.py', 'w') as f:
        # 清除原有内容
        f.truncate()
        # 写入新内容
        f.write(f'PGM = {data}')

