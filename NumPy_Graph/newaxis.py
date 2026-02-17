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
