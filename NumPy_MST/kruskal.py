from dataclasses import dataclass, field
from icecream import ic
import numpy as np

@dataclass
class UnionFind:
    n: int
    parent: np.ndarray = field(init=False)
    rank: np.ndarray = field(init=False)

    def __post_init__(self):
        self.parent = np.arange(self.n)
        self.rank = np.zeros(self.n, dtype=int)

    def find(self, i: int):
        if self.parent[i] == i:
            return i
        
        # 路徑壓縮 (Path Compression)
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
    
    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            # Union by Rank
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_j
            else:
                self.parent[root_i] = root_j
                self.rank[root_j] += 1
            return True
        return False

def kruskal_mst(n: int, edges: list[tuple[int]]):
    # edges 格式: [(u, v, weight), ...]
    # 根據權重排序
    dtype = [('u', int), ('v', int), ('weight', float)]
    structured_edges = np.array(edges, dtype=dtype)
    sorted_edges = np.sort(structured_edges, order='weight')
    
    uf = UnionFind(n)
    mst_edges = []
    total_weight: int = 0

    for edge in sorted_edges:
        u, v, w = int(edge['u']), int(edge['v']), float(edge['weight'])
        if uf.union(u, v):
            mst_edges.append((u, v, w))
            total_weight += w
            if len(mst_edges) == n - 1:
                break
    
    return mst_edges, total_weight

# 初始化鄰接表 (Dict of Lists)
num_nodes: int = 4
adj = {i: [] for i in range(num_nodes)}

# 建立測試資料 (u, v, weight)
test_edges = [
    (0, 1, 10), (0, 2, 6), (0, 3, 5),
    (1, 3, 15), (2, 3, 4)
]

for u, v, w in test_edges:
    adj[u].append((v, w))
    adj[v].append((u, w))

mst_edges, total_weight = kruskal_mst(num_nodes, test_edges)
ic(mst_edges)
ic(total_weight)
