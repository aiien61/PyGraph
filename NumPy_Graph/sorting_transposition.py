import numpy as np
from icecream import ic

arr = np.array([[3, 1, 5], [4, 2, 3]])
ic(np.sort(arr, axis=1))  # 每列排序
ic(arr.T)