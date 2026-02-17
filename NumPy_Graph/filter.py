import numpy as np
from icecream import ic

arr = np.array([10, 20, 30, 40])
ic(arr)
ic(np.where(arr > 25, "大於25", "小於等於25"))