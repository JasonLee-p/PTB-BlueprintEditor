"""
读取xml形式的图纸，提取出图纸的各项参数

该文件引用了https://github.com/ZhangBohan233/PtbStats
"""
import xml.etree.ElementTree as ET
from typing import Tuple
# 项目内部引用
from PartAttrMaps import *

WEIGHT_MULTIPLIER = 0.216  # xml的weight值与真实重量的比例，也就是（3/5）的三次方
HULL_DENSITY = 0.2  # 普通船体的密度

TURBINE_DATA = {  # 这里的吨位单位是t
    "日航烟A": {"block_size": (2, 2, 2), "block_weight": 300},
    "日航烟B": {"block_size": (3, 2, 2), "block_weight": 400},
    "德烟A": {"block_size": (3, 2, 2), "block_weight": 400},
    "德烟B": {"block_size": (3, 3, 2), "block_weight": 425},
    "德烟C": {"block_size": (3, 3, 2), "block_weight": 450},
    "英烟A": {"block_size": (3, 3, 2), "block_weight": 350},
    "驱逐烟": {"block_size": (2, 2, 1), "block_weight": 150},
    "美烟A": {"block_size": (3.5, 3.5, 2), "block_weight": 300},
    "美烟A桅杆": {"block_size": (3.5, 3.5, 2), "block_weight": 300},
    "美烟B": {"block_size": (3, 3.5, 2), "block_weight": 320}
}


class Part:
    def __init__(self, Id, name, weight, buoyancy, rotation, position, scale, color,
                 weapon, turbine):
        # --------------------------------------基础信息-------------------------------------- #
        if self.id2name(Id):
            self.ID = self.id2name(Id)
        else:
            self.ID = Id
            print(f'遇到未知的零件ID: {Id}\n位置:{position} 大小: {scale} 颜色: {color}\n')

        self.Name = name
        self.Weight = weight
        self.Buoyancy = buoyancy
        self.Rotation = rotation  # 旋转角度
        self.RotX = rotation[0]
        self.RotY = rotation[1]
        self.RotZ = rotation[2]
        self.Position = position  # 位置
        self.PosX = position[0]
        self.PosY = position[1]
        self.PosZ = position[2]
        self.Scale = scale  # 碰撞箱
        self.ScaX = scale[0]
        self.ScaY = scale[1]
        self.ScaZ = scale[2]
        self.Color = color  # 颜色
        self.ColR = color[0]
        self.ColG = color[1]
        self.ColB = color[2]
        self.weapon = weapon  # 是否为武器
        self.turbine = turbine  # 是否为轮机
        # --------------------------------------计算信息-------------------------------------- #
        if self.turbine:
            self.countX = int(self.turbine["countX"])
            self.countY = int(self.turbine["countY"])
            self.turbine_num = self.countX * self.countY
            self.turbine_num_show = f'{self.countX} × {self.countY}'
            self.turbine_size = multiply_list(
                TURBINE_DATA[self.ID]["block_size"], [self.countX, 1, self.countY])
            self.turbine_weight = TURBINE_DATA[self.ID]["block_weight"] * self.turbine_num
        else:
            self.turbine_num = 0  # 轮机数量
            self.turbine_size = (0, 0, 0)
            self.turbine_weight = 0
            self.turbine_num_show = '0'

    def __str__(self):
        return f'名称: {self.ID}    类别: {self.Name}\n重量: {self.Weight}      浮力: {self.Buoyancy}\n' \
               f'旋转: {self.Rotation}   坐标: {self.Position}   大小: {self.Scale}   RGB: {self.Color}\n'

    @staticmethod
    def id2name(Id):
        if Id in PartType1:
            return PartType1[Id]
        elif Id in PartTypeSpecial:
            return PartTypeSpecial[Id]
        elif Id in PartType10:
            return PartType10[Id]
        elif Id in PartType12:
            return PartType12[Id]
        elif Id in PartType13:
            return PartType13[Id]
        elif Id in PartType14:
            return PartType14[Id]
        elif Id[0] in ['2', '3', '4', '5']:  # 船体
            result = f'船体{int(Id[2:4])}*{int(Id[4:6])}*{int(Id[6:8])}'
            _rel0 = {'2': '1/2', '3': '1/3', '4': '1/6', '5': '5/6'}
            _rel1 = {'0': '右', '1': '左', '2': '斜右', '3': '斜左'}
            return _rel0[Id[0]] + result + _rel1[Id[1]]
        elif Id[0] == '6':  # 甲板
            result = f'甲板{int(Id[2:4])}*1*{int(Id[6:8])}'
            _rel = {'0': '柚', '1': '蓝', '2': '毡', '3': '空'}
            return result + _rel[Id[1]]
        elif Id[0] == '7':  # 甲板
            result = f'1/2甲板{int(Id[2:4])}*1*{int(Id[6:8])}'
            _rel = {'0': '柚右', '1': '柚左', '2': '蓝右', '3': '蓝左', '4': '毡右', '5': '毡左', '6': '空右', '7': '空左'}
            return result + _rel[Id[1]]
        elif Id[0] == '9':  # 装甲舱
            result = f'{int(Id[-3]) * 50}mm装甲舱'
            _rel = {'1': '1*1*1', '2': '1/2', '3': '1/3', '4': '1/6', '5': '5/6', '6': '3*1*2', '7': '2*2*2'}
            return result + _rel[Id[1]]
        elif Id in PartType11:  #
            return PartType11[Id]
        elif Id in PartType15:
            return PartType15[Id]


class ArmorBoard:
    def __init__(self, name, thickness, size, position, rotation, color, count, cost, time):
        # --------------------------------------基础信息-------------------------------------- #
        self.Name = name
        self.Thickness = thickness
        self.Size = size
        self.Rotation = rotation  # 旋转角度
        self.RotXen = rotation[0]
        self.RotYen = rotation[1]
        self.RotZen = rotation[2]
        self.Position = position  # 位置
        self.PosXen = position[0]
        self.PosYen = position[1]
        self.PosZen = position[2]
        self.Color = color  # 颜色
        self.ColR = color[0]
        self.ColG = color[1]
        self.ColB = color[2]
        self.Count = count
        self.Cost = cost
        self.Time = time
        self.Volume = self.Thickness * self.Size[0] * self.Size[1] / 1000
        self.Weight = round(self.Volume * 7.81, 3)  # 7.81t/m^3
        # --------------------------------------破解信息-------------------------------------- #
        self.crack_rot = {
            ("aItFb4DVGMA=", "EyeSI9BZ8iA=", "EyeSI9BZ8iA="): "上",
            ("EyeSI9BZ8iA=", "vBtdNgUkMhJnDj8rAJ8W1Q==", "EyeSI9BZ8iA="): "前",
            ("EyeSI9BZ8iA=", "wqy+hTD7/OU=", "EyeSI9BZ8iA="): "右",
            ("EyeSI9BZ8iA=", "aItFb4DVGMA=", "EyeSI9BZ8iA="): "后",
            ("EyeSI9BZ8iA=", "DCkAZTY/6PH2Ya3NmrBXVQ==", "EyeSI9BZ8iA="): "左",
            ("cTYnG36Sjc0=", "EyeSI9BZ8iA=", "EyeSI9BZ8iA="): "下",
        }

    def __str__(self):
        return f'名称: {self.Name}    大小: {self.Size}\n' \
               f'旋转: {self.Rotation}   坐标: {self.Position}   RGB: {self.Color}\n'


class Rebar:
    def __init__(self, name, position: Tuple[float], rotation: Tuple[float], child_rotation: Tuple[float], color,
                 diameter: tuple, lineCount, height, variant, group, hallowOut):
        self.Name = name  # 名称
        self.Position = position  # 位置
        self.PosX = position[0]
        self.PosY = position[1]
        self.PosZ = position[2]
        self.Rotation = rotation  # 放置旋转角度
        self.RotX = rotation[0]
        self.RotY = rotation[1]
        self.RotZ = rotation[2]
        self.ChildRotation = child_rotation  # 延伸旋转角度
        self.ChildRotX = child_rotation[0]
        self.ChildRotY = child_rotation[1]
        self.ChildRotZ = child_rotation[2]
        self.Color = color  # 颜色
        self.ColR = color[0]
        self.ColG = color[1]
        self.ColB = color[2]
        self.Diameter = diameter  # 直径
        self.DiaStart = diameter[0]
        self.DiaEnd = diameter[1]
        self.LineCount = lineCount  # 边数
        self.Height = height  # 高度（格）
        self.Variant = variant  # 拉伸
        self.Group = group  # 组
        self.HallowOut = hallowOut  # 空心

    def __str__(self):
        return f'名称: {self.Name}\n' \
               f'坐标: {self.Position}   放置角度: {self.Rotation}   延伸角度: {self.ChildRotation}   RGB: {self.Color}\n' \
               f'直径: {self.Diameter}   边数: {self.LineCount}   高度: {self.Height}   拉伸: {self.Variant}   空心: {self.HallowOut}\n' \
               f'组: {self.Group}\n'


class ReadDesign:
    def __init__(self, path):
        self.path = path
        # 读取xml形式的图纸：
        self._tree = ET.parse(self.path)
        self.root = self._tree.getroot()
        # ShipInfo
        self.ShipInfo = self.root.find('ShipInfo')
        self.ShipName = self.ShipInfo.attrib['ShipName']
        self.AllParts = []
        self.Introduction = self.root.find('CopyWriting').attrib['Text']
        self.HP = int(self.ShipInfo.attrib['HP'])  # 推进功率
        self.weight = str2float(self.ShipInfo.attrib['weight'])
        self.TotalBuoyancy = str2float(self.ShipInfo.attrib['TotalBuoyancy'])
        # 所有部件初始化
        self.Parts = None  # 所有零件
        self.WeightRelation = None  # 零件重量关系
        self.parts_weight = {}  # 零件重量
        self.ArmorBoards = None  # 装甲板
        self.armorboards_weight = 0  # 装甲板重量
        self.Turbines = []  # 涡轮
        self.turbines_weight = 0  # 涡轮重量
        self.Rebars = None  # 钢筋
        self.AirFixs = None  # 空气固定器
        self.Power = None  # 功率
        self.armor2hull_weight = 0  # 装甲舱换算成船体的重量
        self.aircraft_added_weight = 0  # 机库换算成船体的重量
        self.WeaponsMagazines = []  # 所有武器的消耗弹药库信息
        self.WeaponsMagazinesRelation = None  # 武器弹药库关系
        # CP
        try:
            self.CP = int(self.ShipInfo.attrib['CP'])
            self.SecurityCode = self.ShipInfo.attrib['SecurityCode']
        except KeyError:
            self.CP = None
            self.SecurityCode = None
        try:
            # ShipType
            self.ShipType = self.root.find('ShipType')
            self.Type = self.ShipType.attrib['type']
            self.efficiency = str2float(self.ShipType.attrib['efficiency'])
            self.CheckCode1 = self.ShipType.attrib['checkCode']
            # CheakCode
            self.CheakCode = self.root.find('CheakCode')
            self.DesignerID = self.CheakCode.attrib['Designer']
            self.DesignTimeID = self.CheakCode.attrib['DesignTime']
            self.CheckCode2 = self.CheakCode.attrib['Code']
        except AttributeError:
            self.ShipType = None
            self.Type = None
            self.efficiency = None
            self.CheckCode1 = None
            self.CheakCode = None
            self.DesignerID = None
            self.DesignTimeID = None
            self.CheckCode2 = None
        # ________________________________________________________________________________ShipCard
        self.ShipCard = self.root.find('ShipCard')
        self.Designer = self.ShipCard.find('Designer').attrib['Value']
        self.Length = str2float(self.ShipCard.find('Length').attrib['Value'])
        self.Width = str2float(self.ShipCard.find('Width').attrib['Value'])
        self.Height = str2float(self.ShipCard.find('Height').attrib['Value'])
        self.Draft = str2float(self.ShipCard.find('Draft').attrib['Value'])
        self.Volume = str2float(self.ShipCard.find('Volume').attrib['Value'])
        self.Displacement = str2float(self.ShipCard.find('Displacement').attrib['Value'])
        self.Length_in_m = round(3 * self.Length, 3)
        self.Width_in_m = round(3 * self.Width, 3)
        self.Height_in_m = round(3 * self.Height, 3)
        self.Draft_in_m = round(3 * self.Draft, 3)
        self.Len_Wid = round(self.Length / self.Width, 2)
        self.Dra_Wid = round(self.Draft / self.Width, 2)
        self.Len_Wid_Dra = f"{self.Len_Wid}  :1  :{self.Dra_Wid}"
        self.Volume_in_m = round(27 * self.Volume, 3)
        self.Displacement_in_t = round(27 * self.Displacement, 3)
        self.Drag = str2float(self.ShipCard.find('Drag').attrib['Value'])
        self.Range = int(self.ShipCard.find('Range').attrib['Value'])
        self.Power = int(self.ShipCard.find('HP').attrib['Value'])
        self.ViewRange = 0  # TODO:视野
        self.Concealment = 0  # TODO:隐蔽能力
        # 弹药供给
        try:
            self.AmmoSupply = int(self.ShipCard.find('Magazine').attrib['Value'])
        except TypeError:
            self.AmmoSupply = 0
        try:
            self.NeedAmmo = int(self.ShipCard.find('NeedMagazine').attrib['Value'])
        except TypeError:
            self.NeedAmmo = 0
        self.Ammo = f"需求 {self.NeedAmmo} 供给 {self.AmmoSupply}"

        try:  # 主炮
            self.MainWeapon = int(self.ShipCard.find('MainWeapon').attrib['Value'])
        except TypeError:
            self.MainWeapon = 0

        try:  # 主装
            self.MainArmor = int(str2float(self.ShipCard.find('MainArmor').attrib['Value']))
        except TypeError:
            self.MainArmor = 0

        try:  # 防空
            self.AA = self.ShipCard.find('AA').attrib['Value']
        except AttributeError:
            self.AA = "0 / 0 / 0"

        try:  # 水上飞机
            self.Aircraft = self.ShipCard.find('Plane').attrib['Value']
        except AttributeError:
            self.Aircraft = "0"

        try:  # 建造时间
            self.SpendTime = str2float(self.ShipCard.find('SpendTime').attrib['Value'])
        except AttributeError:
            self.SpendTime = 0

        try:  # 建造费用
            self.Price = int(self.ShipCard.find('SpendMoney').attrib['Value'])
        except ValueError:
            _sp = self.ShipCard.find('SpendMoney').attrib['Value'].split('E')
            self.Price = int(str2float(_sp[0]) * 10 ** int(_sp[1]))  # 把科学计数法转换为整数
        # ________________________________________________________________________________钢板
        self._airfixs = self.root.find('airfixs')
        self.AirFixs = {
            "name": [],
            "posX": [],
            "posY": [],
            "posZ": [],
            "rotX": [],
            "rotY": [],
            "rotZ": [],
            "thickness": [],
            "scaleX": [],
            "scaleY": [],
            "scaleZ": [],
            "group": [],
            "colR": [],
            "colG": [],
            "colB": []
        }
        self._airfix_points = []
        if self._airfixs is None:
            self.AirFixs = None
        else:
            for airfix in self._airfixs:
                for key in self.AirFixs.keys():
                    self.AirFixs[key].append(airfix.attrib[key])
                # 钢板的所有point元素全部作为list存到self._airfix_points中
                points = [list(p.attrib.values()) for p in airfix.findall('point')]
                self._airfix_points.append(points)
            self.AirFixs['points'] = self._airfix_points
        # ________________________________________________________________________________MODs
        self._mods = self.root.find('mods')
        self.Mods = {
            "name": [],
            "posX": [],
            "posY": [],
            "posZ": [],
            "rotX": [],
            "rotY": [],
            "rotZ": [],
            "colR": [],
            "colG": [],
            "colB": [],
            "modID": [],
            "modType": [],
            "shaftType": []
        }
        if self._mods is None:
            self.Mods = None
        else:
            for mod in self._mods:
                for key in self.Mods.keys():
                    self.Mods[key].append(mod.attrib[key])
        self.weight_ratio = round(self.Displacement_in_t / self.Volume_in_m, 3)
        # 方形系数
        self.SquareCoefficient = round(
            self.Displacement_in_t / (self.Length_in_m * self.Width_in_m * self.Draft_in_m), 3)

    @staticmethod
    def get_magazines_from_weapon_name(weapon):
        ...

    def get_parts_weight(self):
        """
        计算每个种类零件的总重量
        :return:
        """
        self.parts_weight = {category: 0 for category in self.Parts.keys()}
        for category, parts in self.Parts.items():  # 计算每个category的总重量
            if len(parts) == 0:
                continue
            self.parts_weight[category] = round(sum([part.Weight for part in parts]), 3)

    def get_turbine_weight(self):
        """
        计算轮机的总重量
        :return:
        """
        # 获取战舰的轮机数据：
        if self.Parts["排烟器"]:
            self.turbines_weight = round(sum([part.turbine_weight for part in self.Parts["排烟器"]]), 3)

    def get_weight_relation(self):
        """
        必须在get_parts_weight()和get_turbine_weight()之后调用
        :return:
        """
        _data = self.parts_weight.copy()
        # 加入其他数据
        _data['装甲板'] = self.armorboards_weight
        _data['轮机'] = self.turbines_weight
        _data['动力系统'] = _data['排烟器'] + _data['轮机']
        del _data['排烟器']
        del _data['轮机']
        # 合并船体数据和传动数据
        _data['船体'] = round(_data['船体'] + _data['传动'], 3)
        del _data['传动']
        # 将装甲舱减去的重量加到船体上
        _data['船体'] += self.armor2hull_weight
        # 把机库增重从船体上减去
        _data['船体'] -= self.aircraft_added_weight
        # 合并装饰和火控和测距仪数据
        _data['装饰'] = _data['装饰'] + _data['火控'] + _data['测距仪'] + _data['弹射器']
        try:
            del _data['火控']
            del _data['测距仪']
            del _data['弹射器']
        except KeyError:
            pass
        # 删除装甲舱毛重
        del _data['装甲']
        # 删除值为0的部件
        for key in list(_data.keys()):
            if _data[key] == 0:
                del _data[key]
        self.WeightRelation = _data

    @staticmethod
    def get_weapons_magazines(weapon_name):
        if weapon_name[1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            weapon_name = weapon_name[2:]

    def get_weapons_magazines_relation(self):
        ...

    def read_parts(self):
        """
        读取零件元素，初始化self.Parts
        :return: self.Parts
        """
        # 初始化result
        result = {category: [] for category in category_mapping.keys()}
        for part in self.root.find('parts').findall('part'):  # 遍历所有的零件
            # 判断是否为武器
            is_weapon = False
            # 判断是否为排烟器
            is_turbine = False
            if part.find('WeaponAimArea') is not None:
                is_weapon = part.find('WeaponAimArea').attrib
            elif part.find('turbine') is not None:
                is_turbine = part.find('turbine').attrib
            # 初始化Part类
            P = Part(  # -----------------------------------------------初始化Part类
                part.attrib['Id'],  # Id
                part.attrib['Name'],  # Name
                str2float(part.attrib['weight']) * WEIGHT_MULTIPLIER,  # Weight
                part.attrib['buoyancy'],  # Buoyancy
                (
                    int(part.find("Rotation").attrib['RotX']),  # Rotation
                    int(part.find("Rotation").attrib['RotY']),
                    int(part.find("Rotation").attrib['RotZ'])
                ), (
                    round(str2float(part.find("position").attrib['posX']), 1),  # Position
                    round(str2float(part.find("position").attrib['posY']), 1),
                    round(str2float(part.find("position").attrib['posZ']), 1)
                ), (
                    str2float(part.find("scale").attrib['ScaX']),  # Scale
                    str2float(part.find("scale").attrib['ScaY']),
                    str2float(part.find("scale").attrib['ScaZ'])
                ), (
                    int(256 * str2float(part.find("Color").attrib['ColorR'])),  # Color
                    int(256 * str2float(part.find("Color").attrib['ColorG'])),
                    int(256 * str2float(part.find("Color").attrib['ColorB']))
                ),
                is_weapon,
                is_turbine
            )  # ----------------------------------------------------------------结束初始化
            if is_turbine:  # 获取排烟器种类等信息
                self.Turbines.append([P.ID, {
                    "单个轮机大小": (P.countX, P.countY),
                    "单烟轮机重量": P.turbine_weight,
                    "单烟轮机数量": P.turbine_num_show,
                    "单烟轮机大小": P.turbine_size
                }])
            _map1 = {'1*1*1': 1, '3*1*2': 6, '2*2*2': 8}
            _map2 = {'1/2': 0.5, '1/3': 1 / 3, '1/6': 1 / 6, '5/6': 5 / 6}
            # 计算装甲舱增重
            if "装甲舱" in P.ID:
                p_volume_in_g = _map1[P.ID[-5:]] if P.ID[-5:] in _map1.keys() else _map1[P.ID[-3:]]
                self.armor2hull_weight += p_volume_in_g * 5.4
            self.armor2hull_weight = round(self.armor2hull_weight, 3)
            # 计算舰载机增重
            if '机库' in P.ID:
                self.aircraft_added_weight += 32.4
            self.aircraft_added_weight = round(self.aircraft_added_weight, 3)
            added_to_category = False
            # 通过part的ID和Name判断part属于哪个category
            for category, part_names in category_mapping.items():
                if any(part_name in P.ID for part_name in part_names) or P.Name in part_names:
                    result[category].append(P)
                    added_to_category = True
                    break
            if not added_to_category:
                result["装饰"].append(P)
        # 得到属性 Parts, parts_weight, turbines_weight
        self.Parts = result
        self.get_parts_weight()
        # 修正装甲重量
        self.parts_weight["装甲舱增重"] = self.parts_weight["装甲"] - self.armor2hull_weight
        # 修正舰载机重量
        self.parts_weight["舰载机增重"] = self.aircraft_added_weight
        # 计算轮机重量
        self.get_turbine_weight()

    def read_armors(self):
        """
        读取装甲板元素，初始化self.ArmorBoards
        :return: self.ArmorBoards
        """
        result = []
        _abs = self.root.find("armorboards")
        if _abs is None:
            self.ArmorBoards = None
            return None
        for armor in _abs.findall('armorboard'):
            A = ArmorBoard(
                armor.attrib['name'],
                int(1000 * str2float(armor.attrib['sizeZ'])),
                (int(armor.attrib['sizeX']), int(armor.attrib['sizeY'])),
                (armor.attrib['posXen'], armor.attrib['posYen'], armor.attrib['posZen']),
                (armor.attrib['rotXen'], armor.attrib['rotYen'], armor.attrib['rotZen']),
                (
                    int(256 * str2float(armor.attrib['colR'])),
                    int(256 * str2float(armor.attrib['colG'])),
                    int(256 * str2float(armor.attrib['colB']))
                ),
                int(armor.attrib['count']),
                int(armor.attrib['cost']),
                int(armor.attrib['time'])
            )
            result.append(A)
        self.ArmorBoards = result
        self.armorboards_weight = round(sum([armor.Weight for armor in self.ArmorBoards]), 3)
        self.get_weight_relation()

    def read_rebars(self):
        """
        读取钢筋元素，初始化self.Rebars
        :return: self.Rebars
        """
        result = []
        _rb = self.root.find("rebars")
        if _rb is None:
            self.Rebars = None
            return None
        for _rebar in _rb.findall('_rebar'):
            R = Rebar(  # -----------------------------------------------初始化Rebar类
                _rebar.attrib['name'],  # name
                (
                    str2float(_rebar.attrib['posX']),  # position
                    str2float(_rebar.attrib['posY']),
                    str2float(_rebar.attrib['posZ'])
                ), (
                    str2float(_rebar.attrib['rotX']),  # rotation
                    str2float(_rebar.attrib['rotY']),
                    str2float(_rebar.attrib['rotZ'])
                ), (
                    str2float(_rebar.attrib['childrotX']),  # child rotation
                    str2float(_rebar.attrib['childrotY']),
                    str2float(_rebar.attrib['childrotZ'])
                ), (
                    int(256 * str2float(_rebar.attrib['colorR'])),  # color
                    int(256 * str2float(_rebar.attrib['colorG'])),
                    int(256 * str2float(_rebar.attrib['colorB']))
                ),
                (str2float(_rebar.attrib['diameterStart']), str2float(_rebar.attrib['diameterEnd'])),  # diameter
                int(_rebar.attrib['lineCount']),  # line count
                str2float(_rebar.attrib['height']),  # height
                str2float(_rebar.attrib['variant']),  # variant
                _rebar.attrib['group'],  # group
                str2float(_rebar.attrib['hallowOut']),  # hallow out
            )
            result.append(R)
        self.Rebars = result


def str2float(string):
    # 如果是科学计数法，转换为float
    if "E" in string:
        return float(string.split("E")[0]) * (10 ** int(string.split("E")[1]))
    elif "e" in string:
        return float(string.split("e")[0]) * (10 ** int(string.split("e")[1]))
    else:
        return float(string)


def multiply_list(list1, list2):
    # 两个列表对应元素相乘
    try:
        assert len(list1) == len(list2)
        return [list1[i] * list2[i] for i in range(len(list1))]
    except AssertionError:
        print("列表长度不一致")
        return None


# if __name__ == '__main__':
#     # 路径
#     XMLs = ['KMS-Graf Zeppelin.xml', 'IJN-Shimakaze.xml', 'test.xml']
#     OwnPath = os.path.abspath('.')
#     design_path = os.path.join(OwnPath, 'Designs', XMLs[0])
#     # 创建读取器
#     _DR_ = ReadDesign(design_path)
#     _DR_.read_parts()  # 读取零件
#     _DR_.read_armors()  # 读取装甲板
#     _DR_.read_rebars()  # 读取钢筋
#     for rebar in _DR_.Rebars:
#         print(rebar)
