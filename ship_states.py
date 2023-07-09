"""
工艺战舰船只报告生成器

作者: zbh
version: 0.1.1
"""

import os.path
import sys
import traceback
from xml.etree import ElementTree
from functools import reduce

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


def num(raw_text: str) -> float:
    """
    从可能带有引号的字符串中提取数字

    :param raw_text:
    :return:
    """
    if raw_text.startswith("'") or raw_text.startswith('"'):
        raw_text = raw_text[1:-1]
    return float(raw_text)


def calculate_xyz(scale: ElementTree.Element, rotation: ElementTree.Element) -> \
        (float, float, float):
    """
    返回部件旋转后占用的(x,y,z)，格数

    :param scale:
    :param rotation:
    :return:
    """
    scale_x = num(scale.get("ScaX"))
    scale_y = num(scale.get("ScaY"))
    scale_z = num(scale.get("ScaZ"))
    rot_x = num(rotation.get("RotX"))
    rot_y = num(rotation.get("RotY"))
    rot_z = num(rotation.get("RotZ"))

    x_fix = rot_x == 0 or rot_x == 180
    y_fix = rot_y == 0 or rot_y == 180
    z_fix = rot_z == 0 or rot_z == 180

    if x_fix:
        if y_fix:
            z = scale_z
            if z_fix:
                x = scale_x
                y = scale_y
            else:
                x = scale_y
                y = scale_x
        else:
            x = scale_z
            if z_fix:
                y = scale_y
                z = scale_x
            else:
                y = scale_x
                z = scale_y
    else:
        if y_fix:
            y = scale_z
            if z_fix:
                x = scale_x
                z = scale_y
            else:
                x = scale_y
                z = scale_x
        else:
            x = scale_z
            if z_fix:
                y = scale_x
                z = scale_y
            else:
                y = scale_y
                z = scale_x

    return x, y, z


def armor_plate_weight(xml: ElementTree.Element) -> float:
    return num(xml.get("sizeX")) * num(xml.get("sizeY")) * \
           num(xml.get("sizeZ")) * 7.81


def armor_block_density(thickness: int, heavy: bool) -> float:
    """
    计算装甲舱室的密度

    :param thickness: 厚度，毫米
    :param heavy: 是否为重型装甲
    :return:
    """
    thick_factor = thickness / 50
    den_factor = 0.4 if heavy else 0.5
    if heavy:  # 密度公式很神奇，重甲的最后两个厚度居然不是线性的
        if thickness == 250:
            return 2.6
        if thickness == 300:
            return 3.0
    return HULL_DENSITY + thick_factor * den_factor


class Part:
    """
    船上的一个部件
    """

    def __init__(self, x: float, y: float, z: float,
                 sca_x: float, sca_y: float, sca_z: float,
                 real_buoyancy: float):
        # 部件中心的坐标
        self.x = x
        self.y = y
        self.z = z
        # 旋转后的绝对xyz尺寸，格
        self.sca_x = sca_x
        self.sca_y = sca_y
        self.sca_z = sca_z
        self.real_buoyancy = real_buoyancy


class ShipStats:
    def __init__(self, file_name: str):
        self.etree = ElementTree.parse(file_name)
        self.ship_card = self.etree.find("ShipCard")
        self.ship_info = self.etree.find("ShipInfo")
        self.name = self.ship_info.get("ShipName")
        self.horse_power = int(num(self.ship_info.get("HP")))
        self.displacement = num(self.ship_card.find("Displacement").get("Value")) * 27
        self.water_length = num(self.ship_card.find("Length").get("Value")) * 3
        self.water_width = num(self.ship_card.find("Width").get("Value")) * 3
        self.draught = num(self.ship_card.find("Draft").get("Value")) * 3
        self.main_armor = num(self.ship_card.find("MainArmor").get("Value"))
        self.min_armor = max(min(self.main_armor / 6.0, 76), 24)  # 低于这个厚度的不算装甲

        self.block_coe = self.displacement / (self.water_length * self.water_width * self.draught)
        self.prismatic_coe = 0

        self.armor_plates_weight = 0  # 装甲板总重
        self.armor_block_extra_weight = 0  # 装甲舱室总重-占用体积的船体重量
        self.non_armor_plates = 0  # 厚度不够的装甲总重

        self.engine_self_weight = 0  # 烟囱自身重量
        self.turbine_module_weight = 0  # 轮机舱总重
        self.turbine_volume = 0  # 轮机舱总体积，立方米
        self.other_propulsion_weight = 0  # 动力系统其他部件，如螺旋桨和舵

        self.magazine = num(self.ship_card.find("Magazine").get("Value"))
        self.weapon_weight = 0
        self.aa_weight = 0
        self.torpedo_weight = 0
        self.hangar_count = 0  # 机库数量

        self.decor_weight = 0  # 装饰物品

        self.upper_deck_y = float("-inf")  # 上甲板的y值
        self.castle_deck_y = float("-inf")  # 楼甲板的y值

        self.hull_vol = 0
        self.superstructure_vol = 0

        self.total_x = num(self.ship_info.get("TotalX"))
        self.total_y = num(self.ship_info.get("TotalY"))
        self.total_z = num(self.ship_info.get("TotalZ"))
        self.low_x = float("inf")
        self.low_y = num(self.ship_info.get("NegY"))
        self.low_z = float("inf")
        self.water_line_y = float("-inf")

        self.parts: [Part] = []
        # 三维矩阵，xyz值，每0.5格为一个单元，从xyz的low值开始
        self.vol_matrix = [
            [
                [
                    0 for _ in range(int(self.total_z * 2))
                ] for _ in range(int(self.total_y * 2))
            ] for _ in range(int(self.total_x * 2))
        ]

        self._calculate()

    def generate_report(self):
        # 动力系统总重为 烟囱重+轮机重+轮机舱占用的船体重
        engine_total_weight = self.engine_self_weight + self.turbine_module_weight + \
                              self.other_propulsion_weight + self.turbine_volume * HULL_DENSITY
        magazine_weight = self.magazine * 5.4
        hangar_weight = self.hangar_count * 97.2
        armor_total_weight = self.armor_plates_weight + self.armor_block_extra_weight
        hull_weight = \
            self.displacement - armor_total_weight - engine_total_weight - self.weapon_weight - \
            self.torpedo_weight - self.aa_weight - magazine_weight - hangar_weight - \
            self.decor_weight
        hull_pure_weight = hull_weight - self.non_armor_plates

        detail = f"\n方形系数: {round(self.block_coe, 3)}\n" \
                 f"菱形系数: {round(self.prismatic_coe, 3)}\n" \
                 f"型深: {(self.castle_deck_y - self.low_y) * 3} 米\n" \
                 f"船体体积: {round(self.hull_vol, 2)} 立方米\n" \
                 f"上层建筑体积: {round(self.superstructure_vol, 2)} 立方米\n"

        weights = "\n重量分布:\n" \
                  f"排水量: {round(self.displacement, 2)} 吨\n" \
                  f"装甲总重: {round(armor_total_weight, 2)} 吨，" \
                  f"占比: {round(armor_total_weight / self.displacement * 100, 2)}%\n" \
                  f"  装甲板重: {round(self.armor_plates_weight, 2)} 吨，" \
                  f"占比: {round(self.armor_plates_weight / self.displacement * 100, 2)}%\n" \
                  f"  装甲舱重: {round(self.armor_block_extra_weight, 2)} 吨\n" \
                  f"动力系统总重: {round(engine_total_weight, 2)} 吨，功率: {self.horse_power} 马力\n" \
                  f"火炮总重（含炮塔）: {round(self.weapon_weight, 2)} 吨\n" \
                  f"鱼雷总重: {round(self.torpedo_weight, 2)} 吨\n" \
                  f"防空炮总重: {round(self.aa_weight, 2)} 吨\n" \
                  f"弹药库总重: {round(magazine_weight, 2)} 吨\n" \
                  f"机库总重: {round(hangar_weight, 2)} 吨\n" \
                  f"装饰物品总重: {round(self.decor_weight, 2)} 吨\n" \
                  f"船体重量: {round(hull_weight, 2)} 吨\n" \
                  f"  船身重量: {round(hull_pure_weight, 2)} 吨\n" \
                  f"  薄板材重量: {round(self.non_armor_plates, 2)} 吨\n"

        return f"{self.name}\n" + detail + weights

    def _index_x(self, x: float) -> int:
        return int((x - self.low_x) * 2)

    def _index_y(self, y: float) -> int:
        return int((y - self.low_y) * 2)

    def _index_z(self, z: float) -> int:
        return int((z - self.low_z) * 2)

    def _total_vol_of_y(self, y: float):
        y_index = self._index_y(y)
        vol = 0
        for xs in self.vol_matrix:
            vol += sum(xs[y_index])
        return vol

    def _mid_section_vol(self):
        vol = 0
        for ys in self.vol_matrix[len(self.vol_matrix) // 2]:
            vol += sum(ys)
        return vol

    def _add_part(self, part: ElementTree.Element):
        real_buoyancy = num(part.get("buoyancy")) * WEIGHT_MULTIPLIER
        scale = part.find("scale")
        rotation = part.find("Rotation")
        rotated_scale = calculate_xyz(scale, rotation)

        center_x = num(part.find("position").get("posX"))
        center_y = num(part.find("position").get("posY"))
        center_z = num(part.find("position").get("posZ"))

        self.parts.append(Part(center_x, center_y, center_z,
                               rotated_scale[0], rotated_scale[1], rotated_scale[2],
                               real_buoyancy))

        start_x = center_x - rotated_scale[0] / 2
        start_z = center_z - rotated_scale[2] / 2
        if start_x < self.low_x:
            self.low_x = start_x
        if start_z < self.low_z:
            self.low_z = start_z

    def _calculate_volumes(self):
        for part in self.parts:
            sep_vol = part.real_buoyancy / (part.sca_x * part.sca_y * part.sca_z * 8)
            x = part.x - part.sca_x / 2
            start_y = part.y - part.sca_y / 2
            start_z = part.z - part.sca_z / 2

            while x < part.x + part.sca_x / 2:
                y = start_y
                while y < part.y + part.sca_y / 2:
                    z = start_z
                    while z < part.z + part.sca_z / 2:
                        try:
                            self.vol_matrix[self._index_x(x)][self._index_y(y)][
                                self._index_z(z)] += sep_vol
                        except IndexError:
                            print("Scale error, range:", (self.low_x, self.low_x + self.total_x),
                                  (self.low_y, self.low_y + self.total_y),
                                  (self.low_z, self.low_z + self.total_z),
                                  "Actual:", x, y, z,
                                  "Position:",
                                  part.x, part.y, part.z, file=sys.stderr)
                        z += 0.5
                    y += 0.5
                x += 0.5

    def _calculate(self):
        self._traversal_parts()
        self._calculate_volumes()
        self._calculate_decks()
        self._calculate_coefficients()
        self._traversal_armors()

    def _traversal_armors(self):
        armors = self.etree.find("armorboards")
        for ab in armors.findall("armorboard"):
            plate_weight = armor_plate_weight(ab)
            if plate_weight >= self.min_armor:
                self.armor_plates_weight += plate_weight
            else:
                self.non_armor_plates += plate_weight

    def _traversal_parts(self):
        parts = self.etree.find("parts")
        for part in parts.findall("part"):
            part_id = part.get("Id")
            part_type = part.get("Name")
            real_weight = num(part.get("weight")) * WEIGHT_MULTIPLIER

            if "Hull" == part_type:
                if part_id in TURBINE_DATA:
                    tur_data = TURBINE_DATA[part_id]
                    turbine = part.find("turbine")
                    count_x = num(turbine.get("countX"))
                    count_y = num(turbine.get("countY"))

                    self.engine_self_weight += real_weight
                    self.turbine_module_weight += tur_data["block_weight"] * count_x * count_y
                    turbine_volume = \
                        count_x * count_y * reduce(lambda a, b: a * b, tur_data["block_size"]) * 27
                    self.turbine_volume += turbine_volume
                elif (len(part_id) == 9 and part_id[:2] == "14") or (part_id == "121"):
                    # 螺旋桨，舵，传动轴
                    self.other_propulsion_weight += real_weight
                elif len(part_id) == 9 and part_id[:2] == "15":  # 装饰
                    self.decor_weight += real_weight
                else:
                    # 普通船体或类普通船体
                    self._add_part(part)

            elif "Main_Weapon" == part_type:
                self.weapon_weight += real_weight
            elif "AA" == part_type:
                self.aa_weight += real_weight
            elif "Torpedo" == part_type:
                self.torpedo_weight += real_weight
            elif "magazine" == part_type:
                if part_id == "102000000":  # 机库
                    self.hangar_count += 1
                self._add_part(part)
            elif "Dock" == part_type or "Armor" == part_type:
                if len(part_id) == 8 and part_id[0] == "9":  # 装甲舱室
                    # xml内并没有记录舱室的尺寸，只能靠重量和厚度逆推
                    thickness = int(part_id[-3:]) // 2
                    density = armor_block_density(thickness, part_id[-4] == "1")
                    volume = real_weight / density
                    block_weight = real_weight - volume * HULL_DENSITY
                    self.armor_block_extra_weight += block_weight

                self._add_part(part)

    def _calculate_decks(self):
        self.water_line_y = self.low_y + self.draught / 3

        # 上甲板层的最低体积要求
        upper_deck_vol_req = self.water_length * self.water_width * self.block_coe * 1.5
        # 艏楼/艉楼/舯楼层最低体积要求
        castle_deck_vol_req = upper_deck_vol_req / 2

        y_vols = {}
        y = 0
        while y < self.total_y:
            real_y = y + self.low_y
            y_vol = self._total_vol_of_y(real_y)
            if y_vol != 0:
                y_vols[real_y] = y_vol
            y += 0.5

        y_list = sorted(y_vols.keys())
        for y in reversed(y_list):  # 从上往下遍历
            vol = y_vols[y]
            if self.castle_deck_y == -float("inf") and vol >= castle_deck_vol_req:
                self.castle_deck_y = y + 0.5
            if self.upper_deck_y == -float("inf") and vol >= upper_deck_vol_req:
                self.upper_deck_y = y + 0.5
                break
        for y in y_list:
            vol = y_vols[y]
            if y < self.castle_deck_y:
                self.hull_vol += vol
            else:
                self.superstructure_vol += vol

    def _calculate_coefficients(self):
        mid_section = self.vol_matrix[len(self.vol_matrix) // 2]
        fully_under_water = int(self.draught / 1.5)  # 完全在水下的半格数
        up_under_water_ratio = self.draught % 1.5 / 1.5  # 正好在水线那一格被水浸没的比例

        block_area = self.draught * self.water_width

        mid_section_area = 0  # 水线以下中截面面积
        for yi in range(fully_under_water):
            mid_section_area += sum(mid_section[yi]) / 1.5
        mid_section_area += sum(mid_section[fully_under_water]) / 1.5 * up_under_water_ratio

        cm = mid_section_area / block_area  # 中横剖面系数
        self.prismatic_coe = self.block_coe / cm


def generate_report(ship_name: str):
    if not os.path.exists(ship_name):
        raise FileNotFoundError(ship_name)
    ship = ShipStats(ship_name)
    report = ship.generate_report()
    # print(report)
    pure_name = ship_name.replace("\\", "/").split("/")[-1][:-4]
    out_dir = "reports"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    out = os.path.join("reports", pure_name)
    with open(out + ".txt", "w", encoding="utf8") as f:
        f.write(report)


if __name__ == '__main__':
    path = os.getcwd()

    print("欢迎使用工艺战舰船只报告生成器！")
    print('请输入战舰名称，或<help>查看帮助，<:q>退出。')

    input_ = input(path + ">")

    while input_ != ":q" and input_ != "：q":
        cmd = input_.strip()
        if cmd == "ls" or cmd.startswith("ls "):
            if cmd == "ls":
                list_path = path
            else:
                list_path = os.path.join(path, cmd[3:].strip())
            try:
                file_list = os.listdir(list_path)
                to_print = "\n".join(file_list)
                print(to_print)
            except FileNotFoundError:
                print("路径不存在")
        elif cmd.startswith("cd "):
            cd_path = cmd[3:].strip()
            if cd_path == ".." or cd_path == "../":
                new_path = os.path.dirname(path)
            elif cd_path == "." or cd_path == "./":
                new_path = path
            else:
                new_path = os.path.join(path, cmd[3:].strip())
            if os.path.exists(new_path):
                path = new_path
            else:
                print("路径不存在")
        elif cmd == "all" or cmd.startswith("all "):
            if cmd == "all":
                list_path = path
            else:
                list_path = os.path.join(path, cmd[4:].strip())
            if os.path.exists(list_path):
                listed_files = os.listdir(list_path)
                blueprints = []
                for listed_file in listed_files:
                    if listed_file.endswith(".xml"):
                        blueprints.append(os.path.join(list_path, listed_file))
                confirm = input(f"检测到{len(blueprints)}张图纸，是否继续？继续:Y / N:取消")
                if confirm.strip().upper() == "Y":
                    failures = 0
                    successes = 0
                    for blueprint in blueprints:
                        try:
                            print(f"[{successes + failures + 1}/{len(blueprints)}]"
                                  f" 正在分析: {blueprint}")
                            generate_report(blueprint)
                            successes += 1
                        except Exception as e:
                            print("生成失败！", blueprint, file=sys.stderr)
                            traceback.print_exc()
                            failures += 1
                    print(f"批量生成完成！成功 {successes} 张，失败 {failures} 张。")
            else:
                print("路径不存在")
        elif cmd == "help":
            print('请输入战舰名称，或<help>查看帮助，<:q>退出。')
            print("命令:")
            print("  all [dir]  -- 批量生成当前目录或指定目录下的所有图纸\n"
                  "  cd <dir>   -- 跳转到目录\n"
                  "  ls         -- 列出当前目录下的所有文件\n"
                  "  ls <dir>   -- 列出指定目录下的所有文件\n")
        else:
            blueprint = os.path.join(path, cmd)
            if not blueprint.endswith(".xml"):
                blueprint += ".xml"
            try:
                generate_report(blueprint)
                print("报告生成成功！")
            except IOError:
                print("找不到该图纸！")
            except Exception as e:
                print("哦豁，生成失败，原因各人看:")
                traceback.print_exc()

        input_ = input(path + ">")