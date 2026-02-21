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

# 機台
machine: np.ndarray = np.array([1, 1, 2, 2])
ic(machine.shape)
ic(machine)

# 交期
due: np.ndarray = np.array([10, 12, 15, 20])
ic(due.shape)
ic(due)

print("""\n取某機台全部工序：slicing（切片）""")
m1_jobs: np.ndarray = proc_time[machine == 1]
ic(m1_jobs)