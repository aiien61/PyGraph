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

print("""\n計算完工時間""")
finish: np.ndarray = start + proc_time
ic(finish)

print("""\n找出逾期工序: filter by where""")
late: np.ndarray = finish > due
late_jobs: np.ndarray = np.where(late, "逾期", "達交")
ic(late_jobs)
