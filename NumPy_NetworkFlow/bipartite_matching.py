"""
Convert Bipartite Matching problem to Maximum Flow problem
Use Ford-Fulkerson algorithm to solve maximum flow problem

Bipartite graph
        ↓
轉換成 flow network
        ↓
求 max flow
        ↓
flow 的 edge = matching
"""

import numpy as np
from Ford_Fulkerson import ford_fulkerson
from icecream import ic

def bipartite_matching(num_u, num_v, edges):
    """
    | num_u   | 左側集合 U 的節點數 
    | num_v   | 右側集合 V 的節點數 
    | edges   | U → V 的連線  

    U = {u0, u1, u2}
    V = {v0, v1}

    edges = [
        (0,0),
        (0,1),
        (1,1),
        (2,0)
    ] 

    代表
    u0 → v0
    u0 → v1
    u1 → v1
    u2 → v0

    """
    n: int = 2 + num_u + num_v
    source: int = 0
    sink: int = n - 1

    # 節點 index 排列為：
    # 0                           source
    # 1 .. num_u                  U nodes
    # num_u + 1 .. num_u + num_v  V nodes
    # n - 1                       sink

    # 例如：
    # 0  source
    # 1  u0
    # 2  u1
    # 3  u2
    # 4  v0
    # 5  v1
    # 6  sink

    # 建立 capacity matrix = adjacency matrix
    capacity: np.ndarray = np.zeros((n, n))

    # Build network flow
    # source -> U
    
    # source → u0
    # source → u1
    # source → u2
    
    # source
    #   │
    #   ├─u0
    #   ├─u1
    #   └─u2
    for i in range(num_u):
        capacity[source, 1 + i] = 1
    
    # U → V
    # u node index = 1 + u
    # v node index = 1 + num_u + v

    # (0,1)
    # u0 → v1 變成 capacity[1, 5] = 1


    for u, v in edges:
        capacity[1 + u, 1 + num_u + v] = 1

    # V → sink
    for j in range(num_v):
        capacity[1 + num_u + j, sink] = 1

    # 現在 graph 是：
    # source
    #     │
    #     ├── u0
    #     │    ├── v0
    #     │    └── v1
    #     │
    #     ├── u1
    #     │    └── v1
    #     │
    #     └── u2
    #         └── v0

    # v0 → sink
    # v1 → sink

    max_flow, residual = ford_fulkerson(capacity, source, sink)

    matching = []

    for u, v in edges:
        # 這條 edge 的 capacity 被用掉
        if residual[1 + u, 1 + num_u + v] == 0:
            # 這條 edge 有 flow
            matching.append((u, v))

    return matching


edges = [
    (0,0),
    (0,1),
    (1,1),
    (2,0)
]

matching = bipartite_matching(3,2,edges)
ic(matching)

