"""
读取xml形式的图纸，提取出图纸的各项参数

该文件引用了https://github.com/ZhangBohan233/PtbStats
"""
import xml.etree.ElementTree as ET
from typing import Tuple
# 项目内部引用
from Data.PartAttrMaps import *

WEIGHT_MULTIPLIER = 0.216  # xml的weight值与真实重量的比例，也就是（3/5）的三次方
HULL_DENSITY = 0.2  # 普通船体的密度
PLANE_WEIGHT = 32.4  # 飞机的增重
NUM_STRS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


class Part:
    ShipsAllParts = []  # 所有零件的列表
    ClassesWeight = {"船体": 0, "装甲舱": 0, "火炮": 0, "鱼雷": 0, "防空炮": 0,
                     "火控": 0, "测距仪": 0, "排烟器": 0, "传动": 0, "弹射器": 0, "装饰": 0}  # 所有零件类别的重量
    plane_weight = 0  # 飞机增重

    def __init__(self, Id, name, weight, buoyancy, rotation, position, scale, color):
        """
        零件基类
        :param Id: 零件Id（str）或者零件名称（str）
        :param name: 零件类名 （str）
        :param weight: 零件重量（float t）
        :param buoyancy: 零件浮力（float t）
        :param rotation: 零件角度（tuple）
        :param position: 零件位置（tuple）
        :param scale: 零件碰撞箱大小（tuple）
        :param color: 零件颜色（tuple）
        """
        # --------------------------------------基础信息-------------------------------------- #
        self.Id = Id
        if self.Id[0] in NUM_STRS:  # 如果是Id
            self.ID = self._id2name(Id)
        else:  # 如果是名称
            self.ID = Id
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
        Part.ShipsAllParts.append(self)
        if "机库" in self.ID:
            Part.plane_weight += PLANE_WEIGHT

    @staticmethod
    def get_all_classes_weight(cls):
        cls.plane_weight = round(cls.plane_weight, 3)

    def __str__(self):
        return f'名称: {self.ID}    类别: {self.Name}\n重量: {self.Weight}      浮力: {self.Buoyancy}\n' \
               f'旋转: {self.Rotation}   坐标: {self.Position}   大小: {self.Scale}   RGB: {self.Color}\n'

    def _id2name(self, Id):
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
        else:
            print(f'遇到未知的零件ID: {Id}\n位置:{self.Position} 大小: {self.Scale} 颜色: {self.Color}\n')
            return Id

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
        else:
            print(f'遇到未知的零件ID: {Id}')
            return Id

    @classmethod
    def get_all_information(cls):
        # 其他子类的信息
        Funnel.get_all()
        MainWeapon.get_all()
        AA.get_all()
        Armor.get_all()

    @classmethod
    def change_ship(cls):
        Funnel.change_ship_()
        MainWeapon.change_ship_()
        AA.change_ship_()
        Armor.change_ship_()
        cls.plane_weight = 0.0
        # 删除所有零件对象
        for part in cls.ShipsAllParts:
            del part
        cls.ShipsAllParts = []


class Funnel(Part):
    funnels = []
    funnels_weight = 0.0
    turbines_weight = 0
    turbines_volume = 0.0  # 格为单位
    TurbinesNum: int = 0

    def __init__(self, Id, name, weight, buoyancy, rotation, position, scale, color, turbine_num):
        """
        :param turbine_num: 一个元组，表示轮机的X和Y数量
        """
        super().__init__(Id, name, weight, buoyancy, rotation, position, scale, color)
        # --------------------------------------计算信息-------------------------------------- #
        self.turbineX = turbine_num[0]
        self.turbineY = turbine_num[1]
        self.turbine_num = self.turbineX * self.turbineY
        self.turbine_num_show = f'{self.turbineX}×{self.turbineY}'
        self.turbine_size = multiply_list(
            TURBINE_DATA[self.ID]["block_size"], [self.turbineX, 1, self.turbineY])
        self.turbine_weight = TURBINE_DATA[self.ID]["block_weight"] * self.turbine_num
        # --------------------------------------计算信息-------------------------------------- #
        Funnel.funnels.append(self)
        Funnel.funnels_weight += self.Weight
        Funnel.turbines_weight += self.turbine_weight
        Funnel.turbines_volume += self.turbine_size[0] * self.turbine_size[1] * self.turbine_size[2]
        Funnel.TurbinesNum += self.turbine_num

    @classmethod
    def get_all(cls):
        cls.funnels_weight = round(cls.funnels_weight, 3)
        cls.turbines_weight = round(cls.turbines_weight, 3)
        cls.turbines_volume = round(cls.turbines_volume, 3)

    @classmethod
    def change_ship_(cls):
        cls.funnels = []
        cls.funnels_weight = 0.0
        cls.turbines_weight = 0
        cls.turbines_volume = 0.0
        cls.TurbinesNum = 0


class MainWeapon(Part):
    Gun = []
    Torpedo = []
    # 重量
    GunTotalWeight = 0.0
    TorpedoTotalWeight = 0.0
    # 弹药
    MainCaliber = 0
    TotalNeedMagazines = 0.0
    GunNeedMagazines = 0.0
    MainGunNeedMagazines = 0.0
    OtherGunNeedMagazines = 0.0
    TorpedoNeedMagazines = 0.0
    # 投射量
    TotalFireRate = 0.0

    def __init__(self, Id, name, weight, buoyancy, rotation, position, scale, color, weapon_aim_area):
        """
        :param weapon_aim_area: 武器射界，一个四映射字典，表示武器的射界
        """
        super().__init__(Id, name, weight, buoyancy, rotation, position, scale, color)
        self.weapon_aim_area = weapon_aim_area
        # --------------------------------------信息-------------------------------------- #
        if self.ID[1] in NUM_STRS:  # 火炮
            self.Caliber = int(self.ID[1:4])
            self.Multi = int(self.ID[5])
            self.Magazine = float((self.Caliber ** 2) / 10000 * self.Multi)
            if self.Caliber > MainWeapon.MainCaliber:  # 主炮重量计算
                MainWeapon.MainCaliber = self.Caliber
                MainWeapon.MainGunNeedMagazines = 0.0
            elif self.Caliber == MainWeapon.MainCaliber:
                MainWeapon.MainGunNeedMagazines += self.Magazine
            try:  # 其他性能数据
                self.ReloadTime = MainWeaponsData[self.ID][2]  # 装填时间s
                self.Range = MainWeaponsData[self.ID][3]  # 射程
                self.InitialSpeed = MainWeaponsData[self.ID][5]  # 初速
                self.Accuracy = MainWeaponsData[self.ID][8]  # 精度m/km
                self.ShellWeight = MainWeaponsData[self.ID][10]  # 弹重
                # 穿深
                self.Penetration = (
                    MainWeaponsData[self.ID][-5],
                    MainWeaponsData[self.ID][-4],
                    MainWeaponsData[self.ID][-3],
                    MainWeaponsData[self.ID][-2]
                )
                self.RecommendedNum = MainWeaponsData[self.ID][-1]
                self.FireRate = round(self.ShellWeight * self.Multi * (60 / self.ReloadTime), 2)  # 投射量（kg/min）
                self.FireRate_per_Magazine = round(self.FireRate / self.Magazine, 2)
                if self.FireRate_per_Magazine > 1200:
                    print(self.FireRate_per_Magazine)
                    print(f"警告：武器{self.ID}的单位弹药库投射量超出了范围，可能是数据错误。")
                    raise Warning
                if self.FireRate > 12000:
                    print(self.FireRate)
                    print(f"警告：武器{self.ID}的投射量超出了范围，可能是数据错误。")
                    raise Warning

                # --------------------------------------计算信息-------------------------------------- #
                MainWeapon.TotalFireRate += self.FireRate
            except KeyError:
                print(f"未找到武器{self.ID}的数据，武器投射量的相关数据将会不准确。")
                self.FireRate = 0
                self.FireRate_per_Magazine = 0
            MainWeapon.Gun.append(self)
            # --------------------------------------计算信息-------------------------------------- #
            MainWeapon.GunTotalWeight += self.Weight
            MainWeapon.TotalNeedMagazines += self.Magazine
            MainWeapon.GunNeedMagazines += self.Magazine

        elif self.ID[1] == "雷":
            self.Caliber = {"美": 533, "日": 610, "德": 533}[self.ID[0]]
            self.Multi = int(self.ID[2])
            self.Magazine = self.Multi
            self.ReloadTime = MainWeaponsData[self.ID][2]  # 装填时间s
            self.Range = MainWeaponsData[self.ID][3]  # 射程
            MainWeapon.Torpedo.append(self)
            # --------------------------------------计算信息-------------------------------------- #
            MainWeapon.TorpedoTotalWeight += self.Weight
            MainWeapon.TotalNeedMagazines += self.Magazine
            MainWeapon.TorpedoNeedMagazines += self.Magazine

    @classmethod
    def get_all(cls):
        # 重量
        cls.GunTotalWeight = round(cls.GunTotalWeight, 3)
        cls.TorpedoTotalWeight = round(cls.TorpedoTotalWeight, 3)
        # 弹药库数量
        cls.TotalNeedMagazines = round(cls.TotalNeedMagazines, 3)
        cls.GunNeedMagazines = round(cls.GunNeedMagazines, 3)
        cls.MainGunNeedMagazines = round(cls.MainGunNeedMagazines, 3)
        cls.OtherGunNeedMagazines = cls.GunNeedMagazines - cls.MainGunNeedMagazines
        cls.TorpedoNeedMagazines = round(cls.TorpedoNeedMagazines, 3)
        cls.TotalFireRate = round(cls.TotalFireRate, 3)

    @classmethod
    def change_ship_(cls):
        cls.Gun = []
        cls.Torpedo = []
        # 重量
        cls.GunTotalWeight = 0.0
        cls.TorpedoTotalWeight = 0.0
        # 弹药库数量
        cls.TotalNeedMagazines = 0.0
        cls.GunNeedMagazines = 0.0
        cls.MainGunNeedMagazines = 0.0
        cls.OtherGunNeedMagazines = 0.0
        cls.TorpedoNeedMagazines = 0.0
        cls.MainCaliber = 0
        # 火炮投射量
        cls.TotalFireRate = 0.0


class AA(Part):
    aas = []
    total_weight = 0.0
    NeedMagazines = 0.0

    def __init__(self, Id, name, weight, buoyancy, rotation, position, scale, color):
        super().__init__(Id, name, weight, buoyancy, rotation, position, scale, color)
        self.Caliber = int(self.ID[3:5])
        self.Multi = int(self.ID[6])
        self.Magazine = round(float(self.Caliber ** 2 / 10000) * self.Multi, 3)
        AA.aas.append(self)
        AA.total_weight += self.Weight
        AA.NeedMagazines += self.Magazine

    @classmethod
    def get_all(cls):
        cls.total_weight = round(cls.total_weight, 3)
        cls.NeedMagazines = round(cls.NeedMagazines, 3)

    @classmethod
    def change_ship_(cls):
        cls.total_weight = 0.0
        cls.NeedMagazines = 0.0


class Armor(Part):
    armors = []
    total_weight = 0.0
    total_added_weight = 0.0
    total_original_weight = 0.0

    def __init__(self, Id, name, weight, buoyancy, rotation, position, scale, color):
        super().__init__(Id, name, weight, buoyancy, rotation, position, scale, color)
        self.Thickness = int(self.ID.split('mm')[0])
        ID2volume5 = {'1*1*1': 1, '3*1*2': 6, '2*2*2': 8}
        ID2volume3 = {'1/2': 0.5, '1/3': 1 / 3, '1/6': 1 / 6, '5/6': 5 / 6}
        # 根据ID计算体积，因为图纸中的scale都是1*1*1，而不是实际的体积，所以要靠ID来计算
        self.volume = ID2volume5[self.ID[-5:]] if self.ID[-5:] in ID2volume5.keys() else ID2volume3[self.ID[-3:]]
        # 5.4是1*1*1的船体的重量，经过实验，船体的质量和体积是线性关系
        self.added_weight = self.Weight - 5.4 * self.volume
        # --------------------------------------计算信息-------------------------------------- #
        Armor.armors.append(self)
        Armor.total_added_weight += self.added_weight
        Armor.total_weight += self.Weight

    @classmethod
    def get_all(cls):
        cls.total_original_weight = cls.total_weight - cls.total_added_weight
        cls.total_original_weight = round(cls.total_original_weight, 3)
        cls.total_added_weight = round(cls.total_added_weight, 3)
        cls.total_weight = round(cls.total_weight, 3)

    @classmethod
    def change_ship_(cls):
        cls.armors = []
        cls.total_weight = 0.0
        cls.total_added_weight = 0.0
        cls.total_original_weight = 0.0


class ArmorBoard:
    armorboards = []
    total_weight = 0.0

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
        # --------------------------------------计算信息-------------------------------------- #
        ArmorBoard.armorboards.append(self)
        ArmorBoard.total_weight += self.Weight

    @classmethod
    def get_all_information(cls):
        cls.total_weight = round(cls.total_weight, 3)

    @classmethod
    def change_ship(cls):
        cls.armorboards = []
        cls.total_weight = 0.0

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

    @classmethod
    def get_all_information(cls):
        pass

    @classmethod
    def change_ship(cls):
        pass


class AdvancedHull:
    currentHull = None

    def __init__(
            self, ship_name, position: Tuple[float], dock, rail, waterLineHeight,
            hullColor, waterLineColor,
            slices_dict
    ):
        self.ShipName = ship_name
        self.Position = position
        self.Dock = dock
        self.Rail = rail
        self.WaterLineHeight = waterLineHeight
        self.HullColor = hullColor
        self.WaterLineColor = waterLineColor
        self.Slices = slices_dict
        # --------------------------------------计算信息-------------------------------------- #
        self.SlicesPoints = {}
        # SlicePoints 键值对是：分段名称 和 节点集合，其中节点先从前到后遍历左边再从前到后遍历右边，方向一致。
        for key, value in self.Slices.items():
            add_list = []
            for _i in value["points"]:
                add_list.append((float(value['pos']), float(_i[0]), float(_i[1])))
            # 另一半
            for _i in value["points"]:
                add_list.append((float(value['pos']), -float(_i[0]), float(_i[1])))
            self.SlicesPoints[key] = add_list
        # print(self.SlicesPoints)
        AdvancedHull.currentHull = self

    @classmethod
    def change_ship(cls):
        del cls.currentHull
        cls.currentHull = None


class SplitAdHull(AdvancedHull):
    def __init__(
            self, ship_name, position, dock, rail, waterLineHeight,
            hullColor, waterLineColor,
            slices_dict,
            change_pos=False
    ):
        super().__init__(
            ship_name, position, dock, rail, waterLineHeight,
            hullColor, waterLineColor,
            slices_dict
        )
        self.change_pos = change_pos
        # 交换点坐标的顺序
        if change_pos:
            self.change_position2NA()
        # SlicePoints 键值对是：分段名称 和 节点集合，其中节点先从前到后遍历左边再从前到后遍历右边，方向一致。
        self.SlicesPoints_half = {}  # 前一半
        for key, value in self.SlicesPoints.items():
            self.SlicesPoints_half[key] = value[:len(value) // 2]
        # 初始化所有y,z值
        self.y_list = []
        self.z_list = []
        # 范围
        self.x_range, self.y_range, self.z_range = self.get_range()

    def change_position2NA(self):
        for key, value in self.SlicesPoints.items():
            for i in range(len(value)):
                # x, y, z = z, y, x
                # 如果要显示，则z应该是1，y是2，x是0
                # 如果是Navalart，z应该是0，y是1，x是2
                # 如果是PTB，z应该是2，y是0，x是1
                # 1, 2, 0
                value[i] = (value[i][1], value[i][2], value[i][0])

    def change_position2PTB(self):
        for key, value in self.SlicesPoints.items():
            for i in range(len(value)):
                # x, y, z = z, y, x
                # 如果要显示，则z应该是1，y是2，x是0
                # 如果是Navalart，z应该是0，y是1，x是2
                # 如果是PTB，z应该是2，y是0，x是1
                # 0, 2, 1
                value[i] = (value[i][0], value[i][2], value[i][1])

    def get_range(self):
        x_range = []
        y_range = []
        z_range = []
        for key, value in self.SlicesPoints.items():
            for dot in value:
                x_range.append(dot[0])
                y_range.append(dot[1])
                z_range.append(dot[2])
                self.y_list.append(dot[1])
                self.z_list.append(dot[2])
        x_range = (min(x_range), max(x_range))
        y_range = (min(y_range), max(y_range))
        z_range = (min(z_range), max(z_range))
        self.y_list.sort()
        self.z_list.sort()
        return x_range, y_range, z_range

    def get_xz_from_y(self, y):
        """
        根据y值获取xz值，注意只有左边的点
        :param y:
        :return:
        """
        xz = []
        if y < self.y_range[0] or y > self.y_range[1]:
            raise ValueError('y超出范围')
        for key, value in self.SlicesPoints.items():
            value_left = value[:len(value) // 2]
            for i in range(len(value_left) - 1):
                if value_left[i][1] <= y <= value_left[i + 1][1] or value_left[i][1] >= y >= value_left[i + 1][1]:
                    # 计算x
                    x = value_left[i][0] + (value_left[i + 1][0] - value_left[i][0]) * (
                            y - value_left[i][1]) / (value_left[i + 1][1] - value_left[i][1])
                    # 计算z
                    z = value_left[i][2] + (value_left[i + 1][2] - value_left[i][2]) * (
                            y - value_left[i][1]) / (value_left[i + 1][1] - value_left[i][1])
                    xz.append((x, z))
        return xz

    def get_plane_dots(self):
        # 当有多个点有相同的y值时，把这些点收集起来
        y_dict = {}
        result_y_dict = {}
        for y in self.y_list:
            try:
                y_dict[y] += 1
            except KeyError:
                y_dict[y] = 1
        # 删除只有一个点的y值
        for plane_y, value in y_dict.items():
            if value != 2:
                _list = []
                for _, _value in self.SlicesPoints_half.items():
                    for dot in _value:
                        if dot[1] == plane_y:
                            if _list and abs(dot[2] - _list[-1][2]) > 0.1:
                                _list.append(dot)
                            elif not _list:
                                _list.append(dot)
                _list.sort(key=lambda x: x[2])
                result_y_dict[plane_y] = _list
        # 清除长度小于2的
        result_y_dict = {key: value for key, value in result_y_dict.items() if len(value) > 1}
        # 如果z值之间有其他的Z值，就把这个点删除
        for plane_y, value in result_y_dict.items():
            _value = value.copy()
            for i in range(len(value) - 1):
                for _z in self.z_list:
                    if value[i][2] < _z < value[i + 1][2]:
                        _value[i] = None
            _value = [i for i in _value if i]
            result_y_dict[plane_y] = _value
        # 清除长度小于2的
        result_y_dict = {key: value for key, value in result_y_dict.items() if len(value) > 1}
        return result_y_dict

    def find_bottom(self, shift=0.1):
        """
        找到底部截取点
        :return:
        """
        start, end = self.y_range
        max_width = self.x_range[1] - self.x_range[0]
        times = (self.y_range[1] - self.y_range[0])/shift
        for i in range(int(times)):
            y = start + shift * i
            xz = self.get_xz_from_y(y)
            width = xz[-1][0] - xz[0][0]
            if width > max_width:
                max_width = width
                end = y


class ReadXML:
    """
    读取XML文件，把数据分别存放到各个类里分别使用
    """

    def __init__(self, path):
        self.path = path
        # 把整个文件读取为嵌套字典：
        self.tree = ET.parse(self.path)
        self.root = self.tree.getroot()
        self.design = {
            "ShipInfo": self.get_ShipInfo(),
            "Parts": self.get_parts(),
            "ShipType": self.get_ShipType(),
            "ShipCard": self.get_ShipCard(),
            "CheakCode": self.get_CheakCode(),
            "CopyWriting": self.get_CopyWriting(),
            "Collaborators": self.get_Collaborators(),
            "Lines2": self.get_lines2(),
            "painters": self.get_painters(),
            "appliques": self.get_appliques(),
            "rebars": self.get_rebars(),
            "airfixs": self.get_airfixs(),
            "armorboards": self.get_armorboards(),
            "seaspyplanes": self.get_seaspyplanes(),
            "mods": self.get_mods(),
            "adHull": self.get_adHull()
        }

    # ----------------------------------------------------------------- 开始读取子节点信息
    def get_ShipInfo(self):
        # 把信息读取为字典：
        _result = {}
        for attr in self.root[0].attrib:
            _result[attr] = self.root[0].attrib[attr]
        return _result

    def get_parts(self):
        # 初始化result
        result = {category: [] for category in category_mapping.keys()}
        for part in self.root.find('parts').findall('part'):  # 遍历所有的零件
            try:
                name = part.attrib['Name']
            except KeyError:
                name = ""
            try:
                weight = str2float(part.attrib['weight']) * WEIGHT_MULTIPLIER
            except KeyError:
                weight = 0
            try:
                buoyancy = part.attrib['buoyancy']
            except KeyError:
                buoyancy = 0
            try:
                rotation = (
                    int(part.find("Rotation").attrib['RotX']),
                    int(part.find("Rotation").attrib['RotY']),
                    int(part.find("Rotation").attrib['RotZ'])
                )
                position = (
                    round(str2float(part.find("position").attrib['posX']), 1),
                    round(str2float(part.find("position").attrib['posY']), 1),
                    round(str2float(part.find("position").attrib['posZ']), 1)
                )
                scale = (
                    str2float(part.find("scale").attrib['ScaX']),
                    str2float(part.find("scale").attrib['ScaY']),
                    str2float(part.find("scale").attrib['ScaZ'])
                )
                color = (
                    int(256 * str2float(part.find("Color").attrib['ColorR'])),
                    int(256 * str2float(part.find("Color").attrib['ColorG'])),
                    int(256 * str2float(part.find("Color").attrib['ColorB']))
                )
            except KeyError and AttributeError:
                rotation = (None, None, None)
                position = (None, None, None)
                scale = (None, None, None)
                color = (None, None, None)
            if '110' in part.attrib["Id"][:3] or '113' in part.attrib["Id"][:3]:  # -------------------初始化火炮
                MW = MainWeapon(part.attrib['Id'], name, weight, buoyancy, rotation, position, scale, color,
                                part.find('WeaponAimArea') if not part.find('WeaponAimArea') else part.find(
                                    'WeaponAimArea').attrib)
                if MW.Name == "Torpedo":
                    result['鱼雷'].append(MW)
                else:
                    result['火炮'].append(MW)
            elif part.find('turbine') is not None:
                Fn = Funnel(part.attrib['Id'], name, weight, buoyancy, rotation, position, scale, color, (
                    int(part.find('turbine').attrib["countX"]), int(part.find('turbine').attrib["countY"])
                ))
                result['排烟器'].append(Fn)
            elif '112' in part.attrib["Id"][:3]:  # --------------------------------------------------初始化AA
                AA_ = AA(part.attrib['Id'], name, weight, buoyancy, rotation, position, scale, color)
                result['防空炮'].append(AA_)
            elif "装甲舱" in Part.id2name(part.attrib['Id']):  # --------------------------------------初始化装甲舱
                Armor_ = Armor(part.attrib['Id'], name, weight, buoyancy, rotation, position, scale, color)
                result['装甲舱'].append(Armor_)
            else:
                P = Part(  # ------------------------------------------------------------------------初始化Part
                    part.attrib['Id'], name, weight, buoyancy, rotation, position, scale, color)
                # 对零件进行分类装入result，通过mapping来匹配
                added_to_category = False  # 是否被添加到result中
                for category, part_names in category_mapping.items():
                    if any(part_name in P.ID for part_name in part_names) or P.Name in part_names:
                        result[category].append(P)
                        added_to_category = True
                        break
                if not added_to_category:
                    result["装饰"].append(P)
        return result

    def get_ShipType(self):
        result = {}
        try:
            ShipType = self.root.find('ShipType')
            result['type'] = ShipType.attrib['type'] if ShipType.attrib['type'] != 'auto' else '未知_未知'
            result['efficiency'] = str2float(ShipType.attrib['efficiency'])
            result['checkCode'] = ShipType.attrib['checkCode']
        except AttributeError:
            result['type'] = '未知_未知'
            result['efficiency'] = '未知'
            result['checkCode'] = '无'
        return result

    def get_ShipCard(self):
        result = {}
        ShipCard = self.root.find('ShipCard')
        if ShipCard is None:
            return result
        result['Designer'] = ShipCard.find('Designer').attrib['Value']
        result['ShipName'] = ShipCard.find('ShipName').attrib['Value']
        result['Length'] = str2float(ShipCard.find('Length').attrib['Value'])
        result['Width'] = str2float(ShipCard.find('Width').attrib['Value'])
        result['Height'] = str2float(ShipCard.find('Height').attrib['Value'])
        result['Draft'] = str2float(ShipCard.find('Draft').attrib['Value'])
        result['Volume'] = str2float(ShipCard.find('Volume').attrib['Value'])
        result['Displacement'] = str2float(ShipCard.find('Displacement').attrib['Value'])
        result['Drag'] = str2float(ShipCard.find('Drag').attrib['Value'])
        result['Range'] = int(ShipCard.find('Range').attrib['Value'])
        result['Power'] = round(float(ShipCard.find('HP').attrib['Value']), 1)
        result['MainWeapon'] = int(ShipCard.find('MainWeapon').attrib['Value'])
        result['MainArmor'] = int(str2float(ShipCard.find('MainArmor').attrib['Value']))
        result['SpendTime'] = str2float(ShipCard.find('SpendTime').attrib['Value'])
        result['SpendMoney'] = int(ShipCard.find('SpendMoney').attrib['Value'])
        result['MagazineSupply'] = int(ShipCard.find('Magazine').attrib['Value'])  # 弹药供给
        result['MagazineNeed'] = int(ShipCard.find('NeedMagazine').attrib['Value'])
        try:
            result['AA'] = ShipCard.find('AA').attrib['Value']
            result['Plane'] = ShipCard.find('Plane').attrib['Value']
        except AttributeError:
            result['AA'] = '0 / 0 / 0'
            result['Plane'] = '0'
        return result

    def get_CheakCode(self):
        result = {}
        try:
            CheakCode = self.root.find('CheakCode')
            result['DesignerID'] = CheakCode.attrib['Designer']
            result['DesignTimeID'] = CheakCode.attrib['DesignTime']
            result['Code'] = CheakCode.attrib['Code']
        except AttributeError:
            result['DesignerID'] = '未知'
            result['DesignTimeID'] = '未知'
            result['Code'] = '无'
        return result

    def get_CopyWriting(self):
        try:
            return self.root.find('CopyWriting').attrib['Text']
        except AttributeError:
            return ''

    def get_Collaborators(self):
        try:
            return [c.attrib['Id'] for c in self.root.find('Collaborators')]
        except TypeError:
            return []

    def get_lines2(self):
        result = {}
        return result

    def get_painters(self):
        result = {}
        return result

    def get_appliques(self):
        result = {}
        return result

    def get_rebars(self):
        result = {}
        return result

    def get_airfixs(self):
        result = {}
        return result

    def get_armorboards(self):
        """
        读取装甲板元素，初始化self.ArmorBoards
        :return: self.ArmorBoards
        """
        result = []
        _abs = self.root.find("armorboards")
        if not _abs:
            return result
        for armor_b in _abs.findall('armorboard'):
            try:
                position = (armor_b.attrib['posXen'], armor_b.attrib['posYen'], armor_b.attrib['posZen'])
                rotation = (armor_b.attrib['rotXen'], armor_b.attrib['rotYen'], armor_b.attrib['rotZen'])
            except KeyError:
                position = (armor_b.attrib['posX'], armor_b.attrib['posY'], armor_b.attrib['posZ'])
                rotation = (armor_b.attrib['rotX'], armor_b.attrib['rotY'], armor_b.attrib['rotZ'])
            try:
                color = (int(256 * str2float(armor_b.attrib['colR'])),
                         int(256 * str2float(armor_b.attrib['colG'])),
                         int(256 * str2float(armor_b.attrib['colB'])))
            except KeyError:
                color = (None, None, None)
            try:
                count = int(armor_b.attrib['count'])
                cost = int(armor_b.attrib['cost'])
                time = int(armor_b.attrib['time'])
            except KeyError:
                count = "未知"
                cost = "未知"
                time = "未知"
            A = ArmorBoard(armor_b.attrib['name'], int(1000 * str2float(armor_b.attrib['sizeZ'])),
                           (int(armor_b.attrib['sizeX']), int(armor_b.attrib['sizeY'])),
                           position, rotation, color, count, cost, time)
            result.append(A)
        return result

    def get_seaspyplanes(self):
        result = {}
        return result

    def get_mods(self):
        result = {}
        return result

    def get_adHull(self):
        try:
            adHull_attr = self.root.find('adHull').attrib
            adHull_all = self.root.find('adHull').findall('slice')
        except AttributeError:
            return None
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
        AdH = SplitAdHull(
            self.root.find('ShipInfo').attrib['ShipName'],
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
        result = AdH
        return result

    @staticmethod
    def dict_str(_dict):
        _str = ""
        for key in _dict:
            _str += f"{key}: {_dict[key]}\n"
        return _str

    def __str__(self):
        _str = str(
            f"ShipInfo: {self.dict_str(self.design['ShipInfo'])}\n"
            f"Parts: {self.dict_str(self.design['Parts'])}\n"
            f"ShipType: {self.dict_str(self.design['ShipType'])}\n"
            f"ShipCard: {self.dict_str(self.design['ShipCard'])}\n"
            f"CheakCode: {self.dict_str(self.design['CheakCode'])}\n"
            f"CopyWriting: {self.dict_str(self.design['CopyWriting'])}\n"
            f"Collaborators: {self.dict_str(self.design['Collaborators'])}\n"
            f"Lines2: {self.dict_str(self.design['Lines2'])}\n"
            f"painters: {self.dict_str(self.design['painters'])}\n"
            f"appliques: {self.dict_str(self.design['appliques'])}\n"
            f"rebars: {self.dict_str(self.design['rebars'])}\n"
            f"airfixs: {self.dict_str(self.design['airfixs'])}\n"
            f"armorboards: {self.dict_str(self.design['armorboards'])}\n"
            f"seaspyplanes: {self.dict_str(self.design['seaspyplanes'])}\n"
            f"mods: {self.dict_str(self.design['mods'])}\n"
            f"adHull: {self.dict_str(self.design['adHull'])}\n"
        )
        return _str

    @staticmethod
    def change_ship():
        Part.change_ship()
        ArmorBoard.change_ship()
        Rebar.change_ship()
        AdvancedHull.change_ship()


class DesignAnalyser:

    def __init__(self, DR_dict):
        """

        :param DR_dict: 读取的xml文件的字典
        """
        # 初始化在函数部分计算的数据：
        self.turbine_names = ''
        self.showed_turbine_names()
        self.turbine_nums = ''
        self.showed_turbine_nums()
        # 需要计算的数据
        self.ViewRange = 0  # TODO:视野
        self.Concealment = 0  # TODO:隐蔽能力
        # Introduction-------------------------------------------------------------------------Introduction
        # ShipCard-------------------------------------------------------------------------ShipCard
        if DR_dict['ShipCard'] == {}:
            return
        ShipCard = DR_dict['ShipCard']
        # ShipCard原始数据
        self.Designer = ShipCard['Designer']
        self.ShipName = ShipCard['ShipName']
        # ShipCard换算后的数据
        self.Length = round(3 * ShipCard['Length'], 3)
        self.Width = round(3 * ShipCard['Width'], 3)
        self.Height = round(3 * ShipCard['Height'], 3)
        self.Draft = round(3 * ShipCard['Draft'], 3)
        self.Volume = round(27 * ShipCard['Volume'], 3)
        self.Displacement = round(27 * ShipCard['Displacement'], 3)
        self.ShipType = DR_dict['ShipType']['type'][:2]
        self.ShipSpecial = DR_dict['ShipType']['type'][3:]
        # ShipCard简单计算得到的数据
        self.Len_Wid = round(ShipCard['Length'] / ShipCard['Width'], 1)
        self.Dra_Wid = round(ShipCard['Draft'] / ShipCard['Width'], 1)
        self.Len_Wid_Dra = f"{self.Len_Wid}—1—{self.Dra_Wid}"
        self.Ammo = f"需求 {ShipCard['MagazineSupply']} 供给 {ShipCard['MagazineNeed']}"
        self.DisplacementVolume_ratio = round(self.Displacement / self.Volume, 2)
        self.BlockEfficiency = round(self.Displacement / (self.Length * self.Width * self.Draft), 3)
        self.Power = ShipCard['Power']

        # 对零件的统计计算

        # 对装甲板的统计计算

        # 呈现数据计算
        self.left_frame_data = {
            '设计者ID': DR_dict['CheakCode']['DesignerID'],
            # '战舰类型': DR_dict['ShipType']['type'],
            '排水体积比': self.DisplacementVolume_ratio,
            '长宽吃水比': self.Len_Wid_Dra,
            '方形系数': self.BlockEfficiency,
            '装甲板重量': ArmorBoard.total_weight,
            '装甲舱增重': Armor.total_added_weight,
            '火炮重量': MainWeapon.GunTotalWeight,
            '排烟器种类': self.turbine_names,
            '轮机数量': self.turbine_nums,
            '轮机重量': Funnel.turbines_weight,
            '推重比': round(self.Power / self.Displacement, 3),
        }
        self.right_frame0_data = {
            "left": [
                f"{self.Displacement} 吨",
                f"{self.Length} 米",
                f"{self.Height} 米",
                f"{self.Power} 米制马力",
                f"{self.ViewRange} 米",
                f"{ShipCard['MainWeapon']} 毫米",
                f"{ShipCard['MainArmor']} 毫米",
                self.Ammo,
                f"{ShipCard['SpendMoney']} 资源点"
            ],
            "right": [
                f"{self.Volume} 立方米",
                f"{self.Width} 米",
                f"{self.Draft} 米",
                ShipCard['Drag'],
                f"{self.Concealment} %",
                f"{ShipCard['Range']} 米",
                ShipCard['AA'],
                str(ShipCard['Plane']),
                f"{round(ShipCard['SpendTime'] / 3600, 1)} 小时"
            ]
        }
        self.weight_relation_data = {  # 重量关系
            "船体": sum(
                p.Weight for p in (DR_dict['Parts']['船体'] + DR_dict['Parts']['传动'] + DR_dict['Parts']['弹射器'])
            ) + Armor.total_original_weight - Part.plane_weight,
            "装甲舱增重": Armor.total_added_weight,
            "装甲板": ArmorBoard.total_weight,
            "动力系统": Funnel.turbines_weight + Funnel.funnels_weight,
            "火炮": MainWeapon.GunTotalWeight,
            "鱼雷": MainWeapon.TorpedoTotalWeight,
            "防空炮": AA.total_weight,
            "舰载机增重": Part.plane_weight,
            "装饰": sum(
                p.Weight for p in (DR_dict['Parts']['装饰'] + DR_dict['Parts']['测距仪'] + DR_dict['Parts']['火控'])
            )
        }

        self.right_frame0_data1 = {
            "主炮耗弹": MainWeapon.MainGunNeedMagazines,
            "副炮耗弹": MainWeapon.OtherGunNeedMagazines,
            "鱼雷耗弹": MainWeapon.TorpedoNeedMagazines,
            "防空耗弹": AA.NeedMagazines,
        }

        self.right_frame0_data2 = {}
        for mw_ in MainWeapon.Gun:
            self.right_frame0_data2[mw_.ID] = mw_.FireRate_per_Magazine
        self.right_frame0_data3 = {}
        for mw_ in MainWeapon.Gun:
            self.right_frame0_data3[mw_.ID] = mw_.FireRate

    def showed_turbine_names(self):
        # 初步处理部分数据
        if len(Funnel.funnels) == 0:  # 没有排烟器
            self.turbine_names = "无"
        elif len(Funnel.funnels) == 1:  # 单个排烟器
            self.turbine_names = Funnel.funnels[0].ID
        else:  # 多个排烟器
            names = {}
            for i in Funnel.funnels:
                if i not in names.keys():
                    names[i] = 1
                else:
                    names[i] += 1
            for k, v in names.items():
                if v > 1:
                    self.turbine_names += f"{k.ID}x{v}"
                else:
                    self.turbine_names += f"{k.ID}"
                self.turbine_names += ' '

    def showed_turbine_nums(self):
        if len(Funnel.funnels) == 0:
            self.turbine_nums = "无"
        elif len(Funnel.funnels) == 1:
            self.turbine_nums = f"{Funnel.funnels[0].turbine_num_show}"
        else:
            self.turbine_nums = Funnel.TurbinesNum


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


if __name__ == '__main__':
    import os
    # 路径
    XMLs = ['KMS-Graf Zeppelin.xml', 'IJN-Shimakaze.xml', 'test.xml']
    OwnPath = os.path.dirname(os.path.abspath(__file__))
    design_path = os.path.join(OwnPath, 'Designs', XMLs[1])
