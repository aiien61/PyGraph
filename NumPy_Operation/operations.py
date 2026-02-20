import numpy as np
from icecream import ic

# 建立 array
a = np.arange(1, 5)
b = np.array([[1, 2], [3, 4]])
c = np.array([[1, 2, 3, 4]])
ic(a.shape)
ic(a)

ic(b.shape)
ic(b)

ic(c.shape)
ic(c)

# 基礎運算
ic(a + 10) # 每個元素加 10
ic(a * 2)  # 每個元素乘 2
ic(a + c)  # broadcasting 自動對齊

a = a.reshape(4, 1)
ic(a + b[0]) # broadcasting 自動對齊
