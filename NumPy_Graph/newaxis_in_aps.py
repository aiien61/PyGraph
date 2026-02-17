import numpy as np
from icecream import ic

"""
Reshaping
"""
arr = np.array(range(3))
ic(arr.shape)
ic(arr)

# Convert 1-D array to column vector by np.newaxis
col_vec = arr[:, np.newaxis]
ic(col_vec.shape)
ic(col_vec)

# same as transposition 
ic(arr.reshape(1, 3).T)

# Convert 1-D array to row vector by np.newaxis
row_vec = arr[np.newaxis, :]
ic(row_vec.shape)
ic(row_vec)

# same as transposition
ic(arr.reshape(3, 1).T)

"""
Broadcasting
"""
a = np.array(range(3))
b = np.array([10, 20, 30])
ic(a.shape)
ic(a)

ic(b.shape)
ic(b)

# target: (3, 3) matrix
result = a[:, np.newaxis] + b
ic(result.shape)
ic(result)

x = np.arange(1, 6)
y = np.arange(1, 6)
ic(x.shape)
ic(x)

ic(y.shape)
ic(y)

addition_table: np.ndarray = x[:, np.newaxis] + y
ic(addition_table.shape)
ic(addition_table)

print("""
用 newaxis 建立「工序×工序時間比較矩陣」
找出：
      誰一定比誰早完成
""")

start: np.ndarray = np.array([0, 3, 5, 8])
ic(start.shape)
ic(start)

proc_time: np.ndarray = np.array([3, 2, 4, 1])
ic(proc_time.shape)
ic(proc_time)

finish: np.ndarray = start + proc_time
ic(finish.shape)
ic(finish)

compare = finish[:, None] <= start[None, :]
ic(compare)
print("compare[i, j] = True  代表 i 完工 ≤ j 開始")

print("""找可並行工序""")
parallel = ~compare & ~compare.T
ic(parallel)
