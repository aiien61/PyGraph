import numpy as np
from icecream import ic

x = np.linspace(-1, 1, 3)
y = np.linspace(-1, 1, 3)
X, Y = np.meshgrid(x, y)
ic(X)
ic(Y)

print("""\n所有「機台 × 時段」組合： meshgrid""")
t = np.arange(0, 24)
ic(t)
m = np.array(["M1", "M2", "M3"])
ic(m)

T, M = np.meshgrid(t, m)
ic(T, M)
print("""
T：時間平面
M：機器平面
形成：
      所有「機器×時間」座標
""")

print("""找可排程區域：只允許白班""")
print("available = (T >= 8) & (T <= 20)")
available = (T >=8) & (T <= 20)
ic(available)

