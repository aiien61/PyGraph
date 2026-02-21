import numpy as np
from icecream import ic


print("""\nMES 甘特圖時間軸 ：linspace（時間離散化）""")
timeline: np.ndarray = np.linspace(0, 24, 97) # 每15分鐘
ic(timeline)
