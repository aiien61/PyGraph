import numpy as np
from icecream import ic

x = np.linspace(-1, 1, 3)
y = np.linspace(-1, 1, 3)
X, Y = np.meshgrid(x, y)
ic(X)
ic(Y)