
"""

"""

import math
specialized_map = {
    # 特化海员效率, 特化最大弹药数量
    "UB": (0, 0),
}


class Calculator:
    def __init__(self):
        ...

    @staticmethod
    def get_max_ammo(specialization: str, displacement: float):
        """
        计算最大弹药数量
        :param specialization: 特化类型（字母代号）
        :param displacement: 排水量（吨）
        :return:
        """
        # 最大弹药数量=MAX(
        #    (66.772*LN(吨位)-501.96)/特化海员效率,
        #    特化最大弹药数量
        # )
        return max(
            (66.772 * math.log(displacement) - 501.96) / specialized_map[specialization][0],
            specialized_map[specialization][1]
        )
