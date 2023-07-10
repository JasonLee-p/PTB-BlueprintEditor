"""
读取xml形式的图纸，提取出图纸的各项参数

该文件引用了https://github.com/ZhangBohan233/PtbStats
"""
import xml.etree.ElementTree as ET
import os
from PartID import *

WEIGHT_MULTIPLIER = 0.216  # xml的weight值与真实重量的比例
HULL_DENSITY = 0.2  # 普通船体的密度

TURBINE_DATA = {
    "130000000": {
        "block_size": (2, 2, 2),  # 每个轮机模块大小
        "block_weight": 300,  # 每个轮机模块重量
        "note": "日航烟A"
    },
    "130000001": {
        "block_size": (3, 2, 2), "block_weight": 400, "note": "日航烟B"
    },
    "130000002": {
        "block_size": (3, 2, 2), "block_weight": 400, "note": "德烟A"
    },
    "130000003": {
        "block_size": (3, 3, 2), "block_weight": 425, "note": "德烟B"
    },
    "130000004": {
        "block_size": (3, 3, 2), "block_weight": 450, "note": "德烟C"
    },
    "130000005": {
        "block_size": (3, 3, 2), "block_weight": 350, "note": "英烟A"
    },
    "130000006": {
        "block_size": (2, 2, 1), "block_weight": 150, "note": "驱逐烟"
    },
    "130000007": {
        "block_size": (3.5, 3.5, 2), "block_weight": 300, "note": "鸭滑烟1"
    },
    "130000008": {
        "block_size": (3.5, 3.5, 2), "block_weight": 300, "note": "鸭滑烟2"
    },
    "130000010": {
        "block_size": (3, 3.5, 2), "block_weight": 320, "note": "得梅因烟"
    }
}


class Part:
    def __init__(self, Id, name, weight, buoyancy, rotation, position, scale, color):
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
        # --------------------------------------计算信息-------------------------------------- #

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
        elif Id[0] == '7':
            result = f'1/2甲板{int(Id[2:4])}*1*{int(Id[6:8])}'
            _rel = {'0': '柚右', '1': '柚左', '2': '蓝右', '3': '蓝左', '4': '毡右', '5': '毡左', '6': '空右', '7': '空左'}
            return result + _rel[Id[1]]
        elif Id[0] == '9':
            result = f'{int(Id[-3]) * 50}mm装甲舱'
            _rel = {'1': '1*1*1', '2': '1/2', '3': '1/3', '4': '1/6', '5': '5/6', '6': '3*1*2', '7': '2*2*2'}
            return result + _rel[Id[1]]
        elif Id in PartType11:
            return PartType11[Id]
        elif Id in PartType15:
            return PartType15[Id]


class ArmorBoard:
    def __init__(self, name, thickness, size, position, rotation, color, count):
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
        # --------------------------------------破解信息-------------------------------------- #
        self.crack_rot = {
            ("aItFb4DVGMA=", "EyeSI9BZ8iA=", "EyeSI9BZ8iA="): "上",
            ("EyeSI9BZ8iA=", "vBtdNgUkMhJnDj8rAJ8W1Q==", "EyeSI9BZ8iA=") : "前",
            ("EyeSI9BZ8iA=", "wqy+hTD7/OU=", "EyeSI9BZ8iA=") : "右",
            ("EyeSI9BZ8iA=", "aItFb4DVGMA=", "EyeSI9BZ8iA=") : "后",
            ("EyeSI9BZ8iA=", "DCkAZTY/6PH2Ya3NmrBXVQ==", "EyeSI9BZ8iA=") : "左",
            ("cTYnG36Sjc0=", "EyeSI9BZ8iA=", "EyeSI9BZ8iA=") : "下",
        }

    def __str__(self):
        return f'名称: {self.Name}    大小: {self.Size}\n' \
               f'旋转: {self.Rotation}   坐标: {self.Position}   RGB: {self.Color}\n'


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
        self.HP = int(self.ShipInfo.attrib['HP'])
        #
        self.Parts = None
        try:
            self.CP = int(self.ShipInfo.attrib['CP'])
            self.SecurityCode = self.ShipInfo.attrib['SecurityCode']
        except KeyError:
            self.CP = None
            self.SecurityCode = None
        self.weight = float(self.ShipInfo.attrib['weight'])
        self.TotalBuoyancy = float(self.ShipInfo.attrib['TotalBuoyancy'])
        try:
            # ShipType
            self.ShipType = self.root.find('ShipType')
            self.Type = self.ShipType.attrib['type']
            self.efficiency = float(self.ShipType.attrib['efficiency'])
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
        self.Length = float(self.ShipCard.find('Length').attrib['Value'])
        self.Width = float(self.ShipCard.find('Width').attrib['Value'])
        self.Height = float(self.ShipCard.find('Height').attrib['Value'])
        self.Draft = float(self.ShipCard.find('Draft').attrib['Value'])
        self.Volume = float(self.ShipCard.find('Volume').attrib['Value'])
        self.Displacement = float(self.ShipCard.find('Displacement').attrib['Value'])
        self.Length_in_m = round(3 * self.Length, 3)
        self.Width_in_m = round(3 * self.Width, 3)
        self.Height_in_m = round(3 * self.Height, 3)
        self.Draft_in_m = round(3 * self.Draft, 3)
        self.Len_Wid = round(self.Length / self.Width, 2)
        self.Dra_Wid = round(self.Draft / self.Width, 2)
        self.Len_Wid_Dra = f"{self.Len_Wid}  :1  :{self.Dra_Wid}"
        self.Volume_in_m = round(27 * self.Volume, 3)
        self.Displacement_in_t = round(27 * self.Displacement, 3)
        self.Drag = float(self.ShipCard.find('Drag').attrib['Value'])
        self.Range = int(self.ShipCard.find('Range').attrib['Value'])
        self.Power = int(self.ShipCard.find('HP').attrib['Value'])
        self.ViewRange = 0
        self.Concealment = 0
        try:
            self.AmmoSupply = int(self.ShipCard.find('Magazine').attrib['Value'])
        except TypeError:
            self.AmmoSupply = 0
        try:
            self.NeedAmmo = int(self.ShipCard.find('NeedMagazine').attrib['Value'])
        except TypeError:
            self.NeedAmmo = 0
        self.Ammo = f"需求 {self.NeedAmmo} 供给 {self.AmmoSupply}"
        try:
            self.MainWeapon = int(self.ShipCard.find('MainWeapon').attrib['Value'])
        except TypeError:
            self.MainWeapon = 0
        try:
            self.MainArmor = int(float(self.ShipCard.find('MainArmor').attrib['Value']))
        except TypeError:
            self.MainArmor = 0
        try:
            self.AA = self.ShipCard.find('AA').attrib['Value']
        except AttributeError:
            self.AA = "0 / 0 / 0"
        try:
            self.Aircraft = self.ShipCard.find('Plane').attrib['Value']
        except AttributeError:
            self.Aircraft = "0"
        try:
            self.SpendTime = float(self.ShipCard.find('SpendTime').attrib['Value'])
        except AttributeError:
            self.SpendTime = 0
        try:
            self.Price = int(self.ShipCard.find('SpendMoney').attrib['Value'])
        except ValueError:
            # 把科学计数法转换为整数
            _sp = self.ShipCard.find('SpendMoney').attrib['Value'].split('E')
            self.Price = int(float(_sp[0]) * 10 ** int(_sp[1]))

        # ________________________________________________________________________________钢筋
        self._rebars = self.root.find('rebars')
        self.Rebars = {
            "name": [],
            "posX": [],
            "posY": [],
            "posZ": [],
            "rotX": [],
            "rotY": [],
            "rotZ": [],
            "childrotX": [],
            "childrotY": [],
            "childrotZ": [],
            "lineCount": [],
            "diameterStart": [],
            "diameterEnd": [],
            "height": [],
            "colorR": [],
            "colorG": [],
            "colorB": [],
            "variant": [],
            "group": [],
            "hallowOut": [],
        }
        if self._rebars is None:
            self.Rebars = None
        else:
            for rebar in self._rebars:
                for key in self.Rebars.keys():
                    self.Rebars[key].append(rebar.attrib[key])
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
        # ________________________________________________________________________________装甲板
        self._armors = self.root.find('armorboards')
        self.ArmorBoards = {
            "name": [],
            "sizeX": [],
            "sizeY": [],
            "sizeZ": [],
            "posXen": [],
            "posYen": [],
            "posZen": [],
            "rotXen": [],
            "rotYen": [],
            "rotZen": [],
            "colR": [],
            "colG": [],
            "colB": [],
            "count": [],
            "time": [],
            "cost": [],
        }
        if self._armors is None:
            self.ArmorBoards = None
        else:
            for armor in self._armors:
                for key in self.ArmorBoards.keys():
                    self.ArmorBoards[key].append(armor.attrib[key])
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

    def show_data(self):
        print(f"安全码：\n{self.CheckCode1}\n{self.CheckCode2}")
        print(f"舰船名称：{self.ShipName}")
        print(f"舰船类型：{self.Type}")
        print(f"设计师ID：{self.DesignerID}")
        print(f"设计师昵称：{self.Designer}")
        print(f"排水量：{self.Displacement_in_t}")
        print(f"总体积：{self.Volume_in_m}")
        print(f"排水体积比：{self.weight_ratio}")
        print(f"水线长：{self.Length_in_m}")
        print(f"水线宽：{self.Width_in_m}")
        print(f"吃水：{self.Draft_in_m}")
        print(f"长宽吃水比：{self.Length_in_m / self.Width_in_m}")
        print(f"舰高：{self.Height_in_m}")
        print(f"方形系数：{self.SquareCoefficient}")
        print(f"阻力系数：{self.Drag}")

    def read_parts(self):
        """
        读取零件元素，初始化self.Parts
        :return: self.Parts
        """
        result = {
            "船体": [], "装甲": [],
            "火炮": [], "鱼雷": [], "防空炮": [],
            "火控": [], "测距仪": [],
            "排烟器": [], "传动": [], "弹射器": [], "装饰": [],
        }
        for part in self.root.find('parts').findall('part'):
            P = Part(
                part.attrib['Id'],
                part.attrib['Name'],
                float(part.attrib['weight']) * (3/5)**3,
                part.attrib['buoyancy'],
                (
                    int(part.find("Rotation").attrib['RotX']),
                    int(part.find("Rotation").attrib['RotY']),
                    int(part.find("Rotation").attrib['RotZ'])
                ), (
                    round(float(part.find("position").attrib['posX']), 1),
                    round(float(part.find("position").attrib['posY']), 1),
                    round(float(part.find("position").attrib['posZ']), 1)
                ), (
                    float(part.find("scale").attrib['ScaX']),
                    float(part.find("scale").attrib['ScaY']),
                    float(part.find("scale").attrib['ScaZ'])
                ), (
                    int(256 * float(part.find("Color").attrib['ColorR'])),
                    int(256 * float(part.find("Color").attrib['ColorG'])),
                    int(256 * float(part.find("Color").attrib['ColorB']))
                )
            )
            if "船体" in P.ID or "薄板" in P.ID or P.ID in ("弹药库", "机库"):
                result["船体"].append(P)
            elif "装甲" in P.ID:
                result["装甲"].append(P)
            elif P.Name == "Main_Weapon":
                result["火炮"].append(P)
            elif P.Name == "Torpedo":
                result["鱼雷"].append(P)
            elif P.Name == "AA":
                result["防空炮"].append(P)
            elif "火控" in P.ID:
                result["火控"].append(P)
            elif "测距仪" in P.ID:
                result["测距仪"].append(P)
            elif "烟" in P.ID:
                result["排烟器"].append(P)
            elif "螺旋桨" in P.ID or P.ID == "舵":
                result["传动"].append(P)
            elif "弹射器" in P.ID:
                result["弹射器"].append(P)
            else:
                result["装饰"].append(P)
        self.Parts = result
        return result

    def read_armors(self):
        """
        读取装甲板元素，初始化self.ArmorBoards
        :return: self.ArmorBoards
        """
        result = {
            "左": [], "右": [],
            "前": [], "后": [],
            "上": [], "下": [],
            "其他": []
        }
        for armor in self._armors.findall('armorboard'):
            A = ArmorBoard(
                armor.attrib['name'],
                int(1000 * float(armor.attrib['sizeZ'])),
                (
                    int(armor.attrib['sizeX']),
                    int(armor.attrib['sizeY']),
                ), (
                    armor.attrib['posXen'],
                    armor.attrib['posYen'],
                    armor.attrib['posZen']
                ), (
                    armor.attrib['rotXen'],
                    armor.attrib['rotYen'],
                    armor.attrib['rotZen']
                ), (
                    int(256 * float(armor.attrib['colR'])),
                    int(256 * float(armor.attrib['colG'])),
                    int(256 * float(armor.attrib['colB']))
                ),
                int(armor.attrib['count']),
            )
            if A.Rotation in A.crack_rot:
                print(f"装甲板{A.Name}的放置方向：{A.crack_rot[A.Rotation]}")
            else:
                print(f"装甲板{A.Name}的放置无法破解")


if __name__ == '__main__':
    OwnPath = os.path.abspath('.')
    design_path = os.path.join(OwnPath, 'Designs', 'KMS-Graf Zeppelin.xml')
    # design_path = os.path.join(OwnPath, 'Designs', 'IJN-Shimakaze.xml')
    # design_path = os.path.join(OwnPath, 'Designs', 'test.xml')
    D1 = ReadDesign(design_path)
    D1.read_parts()
    for cls, parts in D1.Parts.items():
        parts_names = [part.Weight for part in parts]
        print(cls, parts_names)