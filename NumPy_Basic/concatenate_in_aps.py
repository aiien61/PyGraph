import numpy as np
from icecream import ic

# 加工時間
proc_time_1: np.ndarray = np.array([3, 5, 2, 7])
ic(proc_time_1.shape)
ic(proc_time_1)

# 開始時間
proc_time_2: np.ndarray = np.array([1, 3, 8, 10])
ic(proc_time_2.shape)
ic(proc_time_2)

print("""\nappend（較少用，因為會複製）""")
ic(np.append(proc_time_1, [4]))

print("""\n合併兩批製令：concatenate（APS 常用""")
all_proc_time: np.ndarray = np.concatenate([proc_time_1, proc_time_2])
ic(all_proc_time)