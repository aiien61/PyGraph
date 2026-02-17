import numpy as np
from icecream import ic

"""
工序相依： 0 → 1 → 3

1 必須等 0
2 必須等 0
3 必須等 1、2
"""

print("""\n工序相依矩陣 DAG adjacency matrix ：reshape""")
data: list[int] = [
    0,1,1,0,
    0,0,0,1,
    0,0,0,1,
    0,0,0,0
]
adj: np.ndarray = np.array(data).reshape(4, 4)
ic(adj)
print("""adj[i, j] = 1  代表 i → j""")

print("""\n找前置工序""")
predecessors: np.ndarray = adj[:, 3] == 1
ic(predecessors)

print("""\nDAG 向量化 earliest start""")
proc_time: np.ndarray = np.array([3, 5, 2, 4])
ES: np.ndarray = np.zeros(4)

for _ in range(4):
    ES = np.maximum(ES, (ES + proc_time) @ adj)
ic(ES)