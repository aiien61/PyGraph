import numpy as np
import heapq
from icecream import ic

def prim_mst(n: int, adj_list: dict) -> tuple[list[tuple[int]], int]:
    # 使用 NumPy 初始化距離向量與訪問標記
    min_weights: np.ndarray = np.full(n, np.inf)
    parent: np.ndarray = np.full(n, -1, dtype=int)
    visited: np.ndarray = np.zeros(n, dtype=bool)
    
    # 起點初始化 (從頂點 0 開始)
    min_weights[0] = 0
    pq: list[tuple[int]] = [(0, 0)]  # (weight, vertex)
    mst_edges: list[tuple[int]] = [] # (parent vertex, vertex, weight)
    total_weight: int = 0
    
    while pq:
        w, u = heapq.heappop(pq)
        
        if visited[u]:
            continue
        
        visited[u] = True
        total_weight += w
        if parent[u] != -1:
            u_parent: int = int(parent[u])
            mst_edges.append((u_parent, u, w))
        
        # 遍歷鄰接表
        for v, weight in adj_list[u]:
            if not visited[v] and weight < min_weights[v]:
                min_weights[v] = weight
                parent[v] = u
                heapq.heappush(pq, (weight, v))
    
    return mst_edges, total_weight


# 初始化鄰接表 (Dict of Lists)
num_nodes = 4
adj = {i: [] for i in range(num_nodes)}

# 建立測試資料 (u, v, weight)
test_edges = [
    (0, 1, 10), (0, 2, 6), (0, 3, 5),
    (1, 3, 15), (2, 3, 4)
]

for u, v, w in test_edges:
    adj[u].append((v, w))
    adj[v].append((u, w))

mst_edges, total_weight = prim_mst(num_nodes, adj)
ic(mst_edges)
ic(total_weight)
