"""

"""
import json
import os

import matplotlib.pyplot as plt
import numpy as np

LOCAL_ADDRESS = os.getcwd()
COLOR_MAP = {
    # 吨位关系
    "船体": "#000000",
    "装甲舱增重": "#ffdd00",
    "装甲板": "#ff7744",
    "动力系统": "#00ff00",
    "火炮": "#ff0000",
    "鱼雷": "#aaaaff",
    "防空炮": "#aaffff",
    "舰载机增重": "#eeccff",
    "装饰": "#ee00ff",
    # 耗弹量关系
    "主炮耗弹": "#ff2222",
    "副炮耗弹": "#ff7722",
    "鱼雷耗弹": "#2222ff",
    "防空耗弹": "#22ffff",
}


def generate_weight_relation_report(rate=False, scatter=False):
    # 按照吨位绘制散点图
    x = []
    ys = []
    for value in DATA.values():
        x.append(value['吨位'])
        ys.append(value['吨位关系'])
    get_weight_relation(x, ys, rate, scatter)


def generate_ammo_report(rate=False, scatter=False):
    # 按照吨位绘制散点图
    x = []
    ys = []
    for value in DATA.values():
        x.append(value['吨位'])
        ys.append(value['耗弹关系'])
    get_ammo_relation(x, ys, rate, scatter)


def read_json():
    # 打开reader_cache.json文件
    with open(os.path.join(LOCAL_ADDRESS, 'reader_cache.json'), 'r', encoding='utf-8') as f:
        _data = json.load(f)
    # 进行数据清理
    del_ships = []
    for _key in _data.keys():
        # 船名是否是DEX
        if "DE-X型护航驱逐舰" in _data["设计名称"]:
            del_ships.append(_key)
        weight_relation = _data[_key]['吨位关系']
        plane_num = int(_data[_key]["基础数据"]["right"][7].split("/")[0])
        if plane_num > 12:
            del_ships.append(_key)  # 先不对航母或者航空战列舰进行处理
        # 如果船体占比例小于0.25，则删除该船
        if weight_relation["船体"] / _data[_key]["吨位"] < 0.25:
            del_ships.append(_key)
        # 如果有任何一个部分占比例大于0.6，则删除该船
        for _value in weight_relation.values():
            if _value / _data[_key]["吨位"] > 0.6 and weight_relation[_value] != "装甲板":
                del_ships.append(_key)
    for _key in del_ships:
        del _data[_key]
    return _data


def get_weight_relation(x_: list, ys_: list, rate=False, scatter=False):
    global REPORT
    _datas = {
        "船体": [[], []],
        "装甲舱增重": [[], []],
        "装甲板": [[], []],
        "动力系统": [[], []],
        "火炮": [[], []],
        "鱼雷": [[], []],
        "防空炮": [[], []],
        "舰载机增重": [[], []],
        "装饰": [[], []]
    }
    # 向 _datas 中添加点坐标数据，如（x, y）
    for i in range(len(ys_)):
        for key in ys_[i].keys():
            _datas[key][0].append(x_[i])
            if rate:
                _datas[key][1].append(ys_[i][key] / sum(ys_[i].values()))
            else:
                _datas[key][1].append(ys_[i][key])
    # 非线性回归曲线拟合
    curves = {}
    # 获取方差曲线
    standard_d = {}
    for key in _datas.keys():
        # if key == "动力系统":
        #     # 用类反比例函数拟合
        #     curves[key], *_ = curve_fit(
        #         lambda x, a, b, c, d: a / (b * x - c) + d,
        #         _datas[key][0],
        #         _datas[key][1],
        #         maxfev=100000
        #     )
        # else:
        # 使用五次多项式拟合
        curves[key] = np.polyfit(_datas[key][0], _datas[key][1], 6)
        standard_d[key] = {"standard_d": [], "points": [[[], []] for _ in range(24)], "curve": None}
        # 计算每个吨位段的方差
        for i in range(24):
            displacement_range = [i * 5000, (i + 1) * 5000]
            points = [[], []]
            # 获取该吨位段的所有点
            for j in range(len(_datas[key][0])):
                if displacement_range[0] <= _datas[key][0][j] < displacement_range[1]:
                    points[0].append(_datas[key][0][j])
                    points[1].append(_datas[key][1][j])
            # 计算该吨位段的标准差
            standard_d[key]["points"][i][0] = points[0]
            standard_d[key]["points"][i][1] = points[1]
            if len(points[1]) == 0 or len(points[1]) == 1:
                standard_d[key]["standard_d"].append(0.02)
            else:
                standard_d[key]["standard_d"].append(np.std(points[1]))
        # 使用二次多项式拟合
        standard_d[key]["curve"] = np.polyfit(
            [i * 5000 + 2500 for i in range(24)],
            standard_d[key]["standard_d"],
            2
        )
    # 绘制图像
    plt.figure(figsize=(10, 6))
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.title("吨位与船体各部分重量占比关系图")
    plt.xlabel("吨位")
    plt.ylabel("占比")
    plt.xlim(0, 100000)
    if rate:
        plt.ylim(0, 0.7)
    else:
        plt.ylim(0, 60000)
    plt.grid()
    for key in _datas.keys():
        # 绘制曲线
        _x = np.linspace(0, 100000, 1000)
        if scatter:
            plt.scatter(_datas[key][0], _datas[key][1], color=COLOR_MAP[key], s=5)
        # if key == "动力系统":  # 类反比例函数
        #     _y = curves[key][0] / (_x * curves[key][1] - curves[key][2]) + curves[key][3]
        #     plt.plot(_x, _y, color=COLOR_MAP[key])
        #     # 原曲线减方差曲线的值
        #     y_down = curves[key][0] / (_x * curves[key][1] - curves[key][2]) + curves[key][3] - \
        #              np.polyval(standard_d[key]["curve"], _x)
        #     # 原曲线加方差曲线的值
        #     y_up = curves[key][0] / (_x * curves[key][1] - curves[key][2]) + curves[key][3] + \
        #            np.polyval(standard_d[key]["curve"], _x)
        # else:
        _y = np.polyval(curves[key], _x)
        # plt.plot(_x, _y, color=COLOR_MAP[key])
        REPORT += f"    '{key}比例': {[c for c in curves[key]]},\n" if rate else f"    '{key}重量': {[c for c in curves[key]]},\n"
        standard_d_curve = standard_d[key]['curve']
        REPORT += f"    '{key}比例标准差': {[c for c in standard_d_curve]},\n" if rate else f"    '{key}重量标准差': {[c for c in standard_d_curve]},\n"
        y_down = np.polyval(curves[key], _x) - np.polyval(standard_d_curve, _x)
        y_up = np.polyval(curves[key], _x) + np.polyval(standard_d_curve, _x)
        plt.fill_between(_x, y_down, y_up, color=COLOR_MAP[key], alpha=0.3, label=key, linewidth=0)

    plt.legend()
    plt.show()


def get_ammo_relation(x_, ys_, relation=False, scatter=False):
    """
    获取弹药重量与吨位的关系
    :return:
    """
    global REPORT
    _datas = {
        "主炮耗弹": [[], []],
        "副炮耗弹": [[], []],
        "鱼雷耗弹": [[], []],
        "防空耗弹": [[], []]
    }
    # 向 _datas 中添加点坐标数据，如（x, y）
    for i in range(len(ys_)):
        for key in ys_[i].keys():
            _datas[key][0].append(x_[i])
            if relation:
                _datas[key][1].append(ys_[i][key] / sum(ys_[i].values()))
            else:
                _datas[key][1].append(ys_[i][key])
    # 非线性回归曲线拟合
    curves = {}
    # 获取方差曲线
    standard_d = {}
    for key in _datas.keys():
        # 使用六次多项式拟合
        curves[key] = np.polyfit(_datas[key][0], _datas[key][1], 6)
        standard_d[key] = {"standard_d": [], "points": [[[], []] for _ in range(24)], "curve": None}
        # 计算每个吨位段的方差
        for i in range(24):
            displacement_range = [i * 5000, (i + 1) * 5000]
            points = [[], []]
            # 获取该吨位段的所有点
            for j in range(len(_datas[key][0])):
                if displacement_range[0] <= _datas[key][0][j] < displacement_range[1]:
                    points[0].append(_datas[key][0][j])
                    points[1].append(_datas[key][1][j])
            # 计算该吨位段的标准差
            standard_d[key]["points"][i][0] = points[0]
            standard_d[key]["points"][i][1] = points[1]
            if len(points[1]) == 0 or len(points[1]) == 1:
                standard_d[key]["standard_d"].append(0.02)
            else:
                standard_d[key]["standard_d"].append(np.std(points[1]))
        # 使用二次多项式拟合
        standard_d[key]["curve"] = np.polyfit(
            [i * 5000 + 2500 for i in range(24)],
            standard_d[key]["standard_d"],
            2
        )
    # 绘制图像
    plt.figure(figsize=(10, 6))
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.xlim(0, 100000)
    plt.xlabel("吨位")
    if relation:
        plt.title("吨位与各类武器弹药占比关系图")
        plt.ylabel("弹药占比")
        plt.ylim(0, 1)
    else:
        plt.title("吨位与各类武器弹药关系图")
        plt.ylabel("弹药数量")
        plt.ylim(0, 250)
    plt.grid()
    for key in _datas.keys():
        # 绘制曲线
        _x = np.linspace(0, 100000, 1000)
        if scatter:
            plt.scatter(_datas[key][0], _datas[key][1], color=COLOR_MAP[key], s=5)
        # if key == "动力系统":
        #     _y = curves[key][0] / (_x * curves[key][1] - curves[key][2]) + curves[key][3]
        #     plt.plot(_x, _y, color=COLOR_MAP[key])
        #     # 原曲线减方差曲线的值
        #     y_down = curves[key][0] / (_x * curves[key][1] - curves[key][2]) + curves[key][3] - \
        #              np.polyval(standard_d[key]["curve"], _x)
        #     # 原曲线加方差曲线的值
        #     y_up = curves[key][0] / (_x * curves[key][1] - curves[key][2]) + curves[key][3] + \
        #            np.polyval(standard_d[key]["curve"], _x)
        # else:
        _y = np.polyval(curves[key], _x)
        # plt.plot(_x, _y, color=COLOR_MAP[key])
        REPORT += f"    '{key}比例': {[c for c in curves[key]]},\n" if relation else f"    '{key}': {[c for c in curves[key]]},\n"
        standard_d_curve = standard_d[key]['curve']
        REPORT += f"    '{key}比例标准差': {[c for c in standard_d_curve]},\n" if relation else f"    '{key}标准差': {[c for c in standard_d_curve]},\n"
        # 原曲线减方差曲线的值
        y_down = np.polyval(curves[key], _x) - np.polyval(standard_d_curve, _x)
        # 原曲线加方差曲线的值
        y_up = np.polyval(curves[key], _x) + np.polyval(standard_d_curve, _x)
        # 填充加方差和减方差之间的区域
        plt.fill_between(_x, y_down, y_up, color=COLOR_MAP[key], alpha=0.3, label=key, linewidth=0)

    plt.legend()
    plt.show()


if __name__ == '__main__':
    REPORT = ""
    DATA = read_json()
    generate_weight_relation_report(rate=True)
    generate_weight_relation_report(rate=False)
    generate_ammo_report(rate=True)
    generate_ammo_report(rate=False)
    with open("report.txt", "w", encoding="utf-8") as f:
        f.write(REPORT)

