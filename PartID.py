"""
    This file is used to transform PartID to PartName.
    这是作者爆肝整理出来的所有ID和零件名映射，大家尽情使用吧！
"""
PartType1 = {  # 船体
    '1': '船体1*1*1',
    '101': '船体2*1*1',
    '102': '船体2*2*2',
    '102000000': '船体2*2*2',
    '103': '船体3*1*2'
}
PartTypeSpecial = {  # 奇形船体
    '150000077': '半格船体',
    '150000078': '细船体A',
    '150000079': '细船体B',
    '150000080': '1/2半格船体',
    '150000081': '1/2细船体',
    '150000096': '1/2薄船体',
    '150000105': '梯形船体',
    '150000109': '薄板',
    '150000110': '半薄板',
    '150000111': '小薄板',
    '150000112': '1/2薄板',
    '150000113': '半1/2薄板A',
    '150000114': '半1/2薄板B',
    '150000115': '1/2小薄板',
    '150000117': '2/3船体'
}
PartType10 = {  # 特殊船体
    '101000000': '弹药库',
    '101000001': '机库',
}
PartType11 = {  # 武器
    '110003900': '日100*2', '110008800': '中100*2-Z', '110008810': '中100*2-S',
    '110008000': '英114*1',
    '110001000': '日120*1',
    '110007800': '日127*2-B', '110007810': '日127*2-BKA', '110007820': '日127*2-BDA', '110007830': '日127*2-BKB',
    '110007840': '日127*2-BDB', '110007850': '日127*2-BPT', '110000400': '日127*2-S',
    '110000800': '美127*2-MK38', '110008500': '英127*2-N1',
    '110000900': '美127*1-MK24', '110006500': '美127*1-MK42',
    '110005600': '德128*1', '110003100': '德128*2', '110003110': '德128*2-J',
    '110003000': '苏130*1', '110002800': '苏130*1-C', '110002810': '苏130*1-CY',
    '110009800': '苏130*2-S', '110009810': '苏130*2-Z', '110009820': '苏130*2-LS', '110009830': '苏130*2-LZ',
    '110009200': '苏130*4',
    '110009600': '意135*3',
    '110004700': '中130*2',
    '110001600': '德150*1', '110004200': '德150*2', '110001700': '德150*3',
    '110002400': '英133*2',
    '110000600': '英152*2-MK', '110008200': '英152*4', '110006900': '英152*2-N5',
    '110009900': '法152*3', '110009910': '法152*3-K',
    '110002700': '意152*3', '110002710': '意152*3-J',
    '110005100': '美152*3', '110006700': '美152*2', '110004900': '美152*2-DP',
    '110007300': '苏152*3-B38', '110007310': '苏152*3-B38J', '110007320': '苏152*3-B38L', '110007340': '苏152*3-B38JL',
    '110008600': '荷152*2', '110008610': '荷152*2-J', '110008620': '荷152*2-JL',
    '110001400': '日155*3', '110001420': '日155*3-L',
    '110005300': '苏180*2-B1P', '110009500': '苏180*2-SM45', '110009520': '苏180*2-SM45L',
    '110007400': '英190*1',
    '110003800': '德203*2', '110003820': '德203*2-L', '110003830': '德203*2-LK',
    '110008700': '德203*3', '110008720': '德203*3-L',
    '110001200': '日203*2', '110001220': '日203*2-L',
    '110007100': '英203*2',
    '110006600': '美203*2', '110003200': '美203*3-MK14', '110003210': '美203*3-MK14J', '110005700': '美203*3-MK15',
    '110004300': '美203*3-MK16', '110008900': '美203*1', '110008910': '美203*1-L',
    '110009300': '苏220*3', '110009310': '苏220*3-L',
    '110006200': '英233*2',
    '110009100': '法240*4',
    '110008400': '芬254*2',
    '110005000': '德280*3-SKC28', '110003300': '德280*3-SKC34', '110003330': '德280*3-SKC34K',
    '110006100': '德305*2',
    '110003500': '苏305*1',
    '110004100': '奥305*3', '110004140': '奥305*3-K',
    '110006800': '英305*2',
    '110003400': '苏305*3-B50', '110006400': '苏305*3-SM33', '110006420': '苏305*3-SM33L',
    '110004000': '美305*3',
    '110010000': '日310*3', '110010030': '日310*3-K',
    '110007000': '法330*4',
    '110006000': '英343*2',
    '110002100': '美356*3-MK4', '110001900': '美356*2-MK8', '110001920': '美356*2-MK8L', '110002000': '美356*3-MK9',
    '110007600': '美356*4-MKB',
    '110002200': '英356*2', '110002230': '英356*2K', '110002300': '英356*4', '110002330': '英356*4K',
    '110002500': '日356*2', '110002520': '日356*2-L', '110002900': '日356*2-G', '110002910': '日356*2-T',
    '110000500': '英381*2', '110000520': '英381*2-L', '110000530': '英381*2-LK',
    '110004800': '德380*2-SKL45', '110004810': '德380*2-SKL45J',
    '110001500': '德380*2-SKC34', '110001520': '德380*2-SKC34L', '110001530': '德380*2-SKC34LK',
    '110001800': '意381*3', '110001810': '意381*3-J', '110001830': '意381*3-K',
    '110004500': '法380*4', '110004530': '法380*4-K',
    '110007500': '德406*3',
    '110005500': '美406*2-MK5',
    '110002600': '英406*3-MK1', '110002610': '英406*3-MK1J', '110002630': '英406*3-MK1K',
    '110008300': '英406*3-MK2', '110008330': '英406*3-MK2K', '110008301': '英406*3-MK2G', '110008331': '英406*3-MK2GK',
    '110008100': '美406*2-MK2', '110008110': '美406*2-MK2J', '110008130': '美406*2-MK2JK',
    '110000700': '美406*3-MK6', '110000730': '美406*3-MK6K', '110003600': '美406*3-MK7', '110003620': '美406*3-MK7L',
    '110005200': '苏406*3',
    '110001100': '日410*2', '110001120': '日410*2-K', '110007200': '日410*3', '110007210': '日410*3-L',
    '110004400': '德420*2', '110004430': '德420*2-L',
    '110005900': '法431*4',
    '110009400': '英450*1', '110009410': '英450*2', '110009420': '英450*2-T',
    '110007700': '苏457*3', '110007710': '苏457*3-J', '110007720': '苏457*3-L',
    '110005800': '英457*2', '110005810': '英457*2-G',
    '110005400': '美457*3',
    '110004600': '日460*2', '110004610': '日460*2-G', '110001300': '日460*3', '110001310': '日460*3-K',
    '110009700': '日510*2', '110007900': '日510*4',
    '110009000': '德533*2', '110009010': '德533*2-J',
    # ------------------------------------------------------------------------------------------------鱼雷
    '113000000': '美雷3', '113000010': '美雷3-G',
    '113000100': '美雷4', '113000110': '美雷4-G',
    '113000200': '美雷5', '113000210': '美雷5-G',
    '113000300': '德雷3', '113000310': '德雷3-G',
    '113000700': '德雷4', '113000710': '德雷4-G',
    '113000400': '日雷3', '113000410': '日雷3-G',
    '113000500': '日雷4', '113000510': '日雷4-G',
    '113000600': '日雷5', '113000610': '日雷5-G',
    # ------------------------------------------------------------------------------------------------防空炮
    '112000000': '博福斯40*4', '112000010': '博福斯40*4-D',
    '112000100': '九六式25*3', '112000110': '九六式25*3-D1', '112000130': '九六式25*3-D2', '112000120': '九六式25*3-T',
    '112000200': '厄利空20*1', '112000210': '厄利空20*1-D', '112000300': '厄利空20*2', '112000310': '厄利空20*2-D',
    '112000400': '手拉机37*2', '112000420': '手拉机37*2-D',
    '112000500': '弗莱克20*4', '112000510': '弗莱克20*4-D', '112000600': '弗莱克20*1',
    '112000700': '马克十76*1',
    '112000800': '砰砰炮40*8',
    '112000900': '博福斯40*1',
    '112001000': '布雷达20*2',
    '112001100': '德高炮88*1',
    '112001200': '中高炮57*2',
    '112001300': '斯塔格40*2',
    '112001400': '德高炮55*1',
    '114000200': '喀秋莎火箭炮'
}
PartType12 = {  # 舵
    '121': '舵',
}
PartType13 = {  # 轮机
    '130000000': '日航烟A',
    '130000001': '日航烟B',
    '130000002': '德烟A',
    '130000003': '德烟B',
    '130000004': '德烟C',
    '130000005': '英烟A',
    '130000006': '驱逐烟',
    '130000007': '美烟A',
    '130000008': '美烟A桅杆',
    '130000010': '美烟B'
}
PartType14 = {  # 螺旋桨
    '140000000': '四叶螺旋桨宽',
    '140000001': '螺旋桨传动轴3*1*1',
    '140000002': '三叶螺旋桨',
    '140000003': '五叶螺旋桨',
    '140000004': '四叶螺旋桨窄',
    '140000005': '螺旋桨传动轴5*1*1',
    '140000006': '螺旋桨传动轴4*1*1',
}
PartType15 = {  # 雷达火控，装饰物品
    '150000000': '锚链', '150000001': '船锚',
    '150000002': '球形雷达天线罩',
    '150000003': '舵机',
    '150000004': '挡浪板',
    '150000005': '舱门',
    '150000006': '现代小艇', '150000007': '交通艇', '150000008': '交通艇A', '150000009': '交通艇B',
    '150000010': '日驱前桅', '150000011': '日驱后桅',
    '150000012': '大和测距仪', '150000013': '大和后桅',
    '150000015': '纳尔逊前桅', '150000016': '纳尔逊后桅',
    '150000017': '美系mk38测距仪', '150000018': '美系mk37火控', '150000019': '美系SK-1对空雷达火控', '150000021': '北卡后桅',
    '150000022': '舰桥A',
    '150000023': '1/2舰桥A',
    '150000024': '舰桥B',
    '150000025': '带门舰桥B',
    '150000026': '俾斯麦吊机', '150000027': '俾斯麦后桅', '150000028': 'HB型测距仪', '150000029': '俾斯麦球形火控雷达',
    '150000030': '德系10m测距仪', '150000031': '德系6m测距仪', '150000032': '德系10.5m测距仪',
    '150000033': '栏杆',
    '150000034': '1/2栏杆1',
    '150000035': '1/2栏杆A2', '150000036': '1/2栏杆A3', '150000037': '1/2栏杆A4', '150000038': '1/2栏杆A5',
    '150000039': '1/2栏杆A6', '150000040': '1/2栏杆A7', '150000041': '1/2栏杆A8', '150000042': '1/2栏杆A9',
    '150000043': '1/2栏杆A10',
    '150000044': '1/2栏杆B2', '150000045': '1/2栏杆B3', '150000046': '1/2栏杆B4', '150000047': '1/2栏杆B5',
    '150000048': '1/2栏杆B6', '150000049': '1/2栏杆B7', '150000050': '1/2栏杆B8', '150000051': '1/2栏杆B9',
    '150000052': '1/2栏杆B10',
    '150000053': '圆柱1', '150000054': '圆柱2', '150000055': '圆柱3',
    '150000056': '美系鸟笼桅短', '150000057': '美系鸟笼桅长',
    '150000058': '圆管A', '150000059': '圆管B',
    '150000061': '改进型挡浪板',
    '150000062': '日系吊机桅杆', '150000063': '重型起重机', '150000064': '英系起重机',
    '150000065': '简易起重机A', '150000066': '简易起重机B', '150000067': '美系起重机',
    '150000068': '日系弹射器', '150000069': '英系弹射器', '150000070': '美系弹射器', '150000071': '美系弹射器B',
    '150000074': '英系火控A', '150000075': '英系火控B', '150000076': '英系火控C',
    '150000100': '1/2舷台A', '150000101': '转角舷台', '150000102': '包围式舷台', '150000103': '舷台',
    '150000097': '舰艏旗杆',
    '150000082': '半格舰桥', '150000083': '1/2半格舰桥', '150000084': '1/4半格舰桥',
    '150000085': '圆环',
    '150000086': '探照灯', '150000087': '俾斯麦探照灯', '150000088': '俾斯麦舷台探照灯',
    '150000089': '系缆柱',
    '150000090': '战列舰前桅指挥塔', '150000091': '战列舰后桅指挥塔',
    '150000092': '梯子',
    '150000093': '小型桅杆', '150000094': '舰尾旗杆', '150000095': '三角桅', '150000098': '驱逐前桅', '150000099': '驱逐后桅',
    '150000104': '栏杆挡板',
    '150000020': '美系SK-2对空雷达火控', '150000106': '94式火控',
    '150000107': '梯形舰桥',
    '150000108': '救生筏',
    '150000118': '德系战列舰装甲堡',
    '150000119': '日系高雄4.5m火控',
    '150000120': '意系利托里奥火控',
    '150000121': '意系猫头鹰雷达火控'
}