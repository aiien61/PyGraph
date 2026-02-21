import numpy as np
from icecream import ic

print("""
MES 常要把：
      工序 × 時段占用矩陣
轉成：
      一維事件序列

""")

schedule = np.array([
    [1, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
])
ic(schedule)

events = schedule.flatten()
ic(events)