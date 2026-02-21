import numpy as np
from icecream import ic

# 加工時間
proc_time: np.ndarray = np.array([3, 5, 2, 7])
ic(proc_time.shape)
ic(proc_time)

# 開始時間
start: np.ndarray = np.array([0, 3, 8, 10])
ic(start.shape)
ic(start)

# 每個工序所需的機台
machine: np.ndarray = np.array([1, 1, 2, 2])
ic(machine.shape)
ic(machine)
print("工序1和工序2需要機台1，工序3和工序4需要機台2")

# 交期
due: np.ndarray = np.array([10, 12, 15, 20])
ic(due.shape)
ic(due)

print("""\n計算完工時間""")
finish: np.ndarray = start + proc_time
ic(finish)

print("""\nAPS 負載平衡核心： 工序 × 機台 負載矩陣""")
# 升維
ic(proc_time[:, np.newaxis])
ic(machine[:, None])

# 建立工序×機台布林矩陣
mask = machine[:, None] == np.array([1, 2])
ic(mask)

# 負載矩陣
machine_time: np.ndarray = proc_time[:, np.newaxis] * mask
ic(machine_time)

print("""\nAPS 瓶頸機器偵測： 每台機器總負載""")
load = machine_time.sum(axis=0)
ic(load)
