"""
把工艺战舰的船体数据转换成NA的船体数据
"""

import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

from design_reader import AdvancedHull


class FreeHull:
    def __init__(self,
                 length, height,  # 长宽
                 frontWidth, backWidth,  # 宽
                 frontSpread, backSpread,  # 增宽
                 upCurve, downCurve,  # 下下弧度
                 heightScale,  # 前高度缩放
                 heightOffset,  # 前高度偏移
                 position, rotation, scale=(1, 1, 1),
                 color='#6F6F6F',  # 颜色
                 armor=5,  # 装甲
                 ):
        if heightScale > 1 or heightScale < 0:
            raise ValueError('heightScale必须在0到1之间')
        if heightOffset > 1 or heightOffset < -1:
            raise ValueError('heightOffset必须在-1到1之间')
        self.length = length
        self.height = height
        self.frontWidth = frontWidth
        self.backWidth = backWidth
        self.frontSpread = frontSpread
        self.backSpread = backSpread
        self.upCurve = upCurve
        self.downCurve = downCurve
        self.heightScale = heightScale
        self.heightOffset = heightOffset
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.color = color
        self.armor = armor

    def to_xml(self):
        # 生成ET对象
        root = ET.Element('part')
        root.set('id', '0')
        root.append(ET.Element('data'))
        root.append(ET.Element('position'))
        root.append(ET.Element('rotation'))
        root.append(ET.Element('scale'))
        root.append(ET.Element('color'))
        root.append(ET.Element('armor'))
        # 写入数据
        root[0].set('length', str(self.length))
        root[0].set('height', str(self.height))
        root[0].set('frontWidth', str(self.frontWidth))
        root[0].set('backWidth', str(self.backWidth))
        root[0].set('frontSpread', str(self.frontSpread))
        root[0].set('backSpread', str(self.backSpread))
        root[0].set('upCurve', str(self.upCurve))
        root[0].set('downCurve', str(self.downCurve))
        root[0].set('heightScale', str(self.heightScale))
        root[0].set('heightOffset', str(self.heightOffset))
        root[1].set('x', str(self.position[0]))
        root[1].set('y', str(self.position[1]))
        root[1].set('z', str(self.position[2]))
        root[2].set('x', str(self.rotation[0]))
        root[2].set('y', str(self.rotation[1]))
        root[2].set('z', str(self.rotation[2]))
        root[3].set('x', str(self.scale[0]))
        root[3].set('y', str(self.scale[1]))
        root[3].set('z', str(self.scale[2]))
        root[4].set('hex', str(self.color[1:]))
        root[5].set('value', str(self.armor))
        return root


class Ship:
    def __init__(self,
                 name,  # 名称
                 author='2593292614',  # 作者
                 description='',  # 描述
                 hornType="1",
                 hornPitch="1",
                 tracerCol="E53D4FFF"
                 ):
        self.name = name
        self.author = author
        self.description = description
        self.hornType = hornType
        self.hornPitch = hornPitch
        self.tracerCol = tracerCol
        # 生成ET对象
        self.root = ET.Element('root')
        self.ship = ET.SubElement(self.root, 'ship')
        self.ship.set('author', author)
        self.ship.set('description', description)
        self.ship.set('hornType', hornType)
        self.ship.set('hornPitch', hornPitch)
        self.ship.set('tracerCol', tracerCol)

    def add_part(self, part):
        self.ship.append(part)

    def output_to_xml(self):
        text = ET.tostring(self.root, encoding='utf-8')
        text = minidom.parseString(text).toprettyxml(indent='  ')
        text = '\n'.join(text.split('\n')[1:])
        path = os.path.join(os.getcwd(), 'ShipSaves', self.name + '.xml')
        with open(path, 'w') as f:
            f.write(text)

    def output_to_na(self):
        text = ET.tostring(self.root, encoding='utf-8')
        text = minidom.parseString(text).toprettyxml(indent='  ')
        text = '\n'.join(text.split('\n')[1:])
        path = os.path.join(os.getcwd(), 'ShipSaves', self.name + '.na')
        with open(path, 'w') as f:
            f.write(text)


if __name__ == '__main__':
    # --------------------------------------------------------------------------读取PTB进阶船壳
    path = os.path.join(os.getcwd(), 'Designs', 'IJN-Atago.xml')
    root = ET.parse(path).getroot()
    adHull_attr = root.find('adHull').attrib
    adHull_all = root.find('adHull').findall('slice')
    slice_dict = {}
    ii = 0
    for slice_ in adHull_all:
        slice_dict[f"{slice_.attrib['name']}{ii}"] = {
            "pos": float(slice_.attrib['pos']),
            "dock": slice_.attrib['dock'],
            "rail": slice_.attrib['rail'],
            "points": [(float(d.attrib["x"]), float(d.attrib["y"])) for d in slice_.findall('point')]
        }
        ii += 1
    add_hull = SplitAdHull(
        root.find('ShipInfo').attrib['ShipName'],
        (float(adHull_attr['posX']), float(adHull_attr['posY']), float(adHull_attr['posZ'])),
        int(adHull_attr['dock']),
        adHull_attr['rail'],
        adHull_attr['waterLineHeight'],
        (float(adHull_attr['hullColorR']), float(adHull_attr['hullColorG']), float(adHull_attr['hullColorB'])),
        (
            float(adHull_attr['waterLineColorR']),
            float(adHull_attr['waterLineColorG']),
            float(adHull_attr['waterLineColorB'])
        ),
        slice_dict
    )
    # --------------------------------------------------------------------------读取PTB进阶船壳完毕
    # print(add_hull.get_xz_from_y(2))
    for k, v in add_hull.get_plane_dots().items():
        print(k, v)

