import hashlib


class HashText:
    def __init__(self, text):
        self.text = text

    def hash32bit_base16(self):
        return hashlib.md5(self.text.encode('utf-8')).hexdigest()


if __name__ == '__main__':
    with open('Designs/test.xml', 'r', encoding='utf-8') as f:
        xml1 = f.read()
    # 将xml1中的所有空格和换行符去掉
    xml1 = xml1.replace(' ', '').replace('\n', '')
    # 将xml1中的Cheakcode下的Code的值删除，改为0
    xml1 = xml1.split('<Code>')[0] + '<Code>0</Code>' + xml1.split('</Code>')[-1]
    # 将xml1中的Cheakcode下的Code2的值删除，改为0
    hash1 = HashText(xml1)
    print(hash1.hash32bit_base16())
    hash2 = HashText('''31099 1672402767''')
    print(hash2.hash32bit_base16())