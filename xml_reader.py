import xml.etree.ElementTree as ET
import os


class ReadDesign:
    def __init__(self, path):
        self.path = path
        # 读取xml形式的图纸：
        self._tree = ET.parse(self.path)
        self.root = self._tree.getroot()
        # ShipInfo
        self.ShipInfo = self.root.find('ShipInfo')
        self.ShipName = self.ShipInfo.attrib['ShipName']
        self.HP = int(self.ShipInfo.attrib['HP'])
        self.CP = int(self.ShipInfo.attrib['CP'])
        self.weight = float(self.ShipInfo.attrib['weight'])
        self.TotalBuoyancy = float(self.ShipInfo.attrib['TotalBuoyancy'])
        self.SecurityCode = self.ShipInfo.attrib['SecurityCode']
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
        self.Volume_in_m = round(27 * self.Volume, 3)
        self.Displacement_in_t = round(27 * self.Displacement, 3)
        self.Drag = self.ShipCard.find('Drag').attrib['Value']
        self.AA = self.ShipCard.find('AA').attrib['Value']
        self.Planes = self.ShipCard.find('Plane').attrib['Value']
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
        print(f"舰高：{self.Height_in_m}")
        print(f"吃水：{self.Draft_in_m}")
        print(f"方形系数：{self.SquareCoefficient}")
        print(f"阻力系数：{self.Drag}")


if __name__ == '__main__':
    OwnPath = os.path.abspath('.')
    design_path = os.path.join(OwnPath, 'Designs', 'KMS-Z36.xml')
    D1 = ReadDesign(design_path)
