import numpy as np
from icecream import ic

a = np.arange(5)
ic(a)

# append
c = np.append(a, [5, 6])
ic(c)

# concatenate
d = np.concatenate((a, c))
ic(d)
