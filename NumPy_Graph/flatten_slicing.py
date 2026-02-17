import numpy as np
from icecream import ic

a = np.arange(1, 5)
ic(a)
b = np.array([[1, 2], [3, 4]])
ic(b)

# flatten
ic(b.flatten())
ic(b.flatten().shape)

# slicing
ic(a[1: 3])
ic(a[1: 3].shape)
ic(b[:, 1])
ic(b[:, 1].shape)
