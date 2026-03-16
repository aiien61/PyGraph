import numpy as np
from icecream import ic

def dfs(residual: np.ndarray, s: int, t: int, visited: np.ndarray, parent: np.ndarray) -> bool:
    """使用DFS來尋找 Augmenting Path

    | residual | Residual graph capacity matrix
    | s        | source                         
    | t        | sink                           
    | visited  | 紀錄節點是否訪問                  
    | parent   | 紀錄路徑                         
    """
    # Get the number of nodes
    n = residual.shape[0]

    stack = [s]
    visited[s] = True

    while stack:
        u = stack.pop()

        # Visit all the neighbours
        for v in range(n):
            # 還沒訪問過 且 residual capacity > 0
            if not visited[v] and residual[u, v] > 0:
                # edge u → v 仍可送 flow
                
                # v 是從 u 走來，用 parent 回溯整條 path
                parent[v] = u
                visited[v] = True
                stack.append(v)

                if v == t:
                    # 找到 augmenting path
                    return True
                
    return False

def ford_fulkerson(capacity, source, sink):
    """
    1. 初始化 residual graph
    2. 尋找一條 augmenting path
    3. 找出該路徑的 bottleneck capacity
    4. 更新 residual graph

    Initial graph
        │
        ▼
    Build residual graph
        │
        ▼
    DFS find augmenting path
        │
        ├── No → END
        │
        ▼
    Find bottleneck capacity
        │
        ▼
    Update residual graph
        │
        ▼
    Increase max_flow
        │
        ▼
    Repeat
    """
    # Get the number of nodes
    n: int = capacity.shape[0]

    # Initialise residual graph
    residual = capacity.copy()

    # Initialise parent array
    parent = np.full(n, -1)
    # 0 → 2 → 5 → 7
    # parent[2] = 0
    # parent[5] = 2
    # parent[7] = 5

    max_flow = 0

    # Keep looking for more augmenting path until none can be found
    while True:
        # Reset visited
        # 每次 DFS 都要重新計算
        visited = np.zeros(n, dtype=bool)

        # Use DFS to find augmenting path
        if not dfs(residual, source, sink, visited, parent):
            break

        # 找 bottleneck capacity
        # 計算 min capacity on path
        path_flow = np.inf
        v = sink

        # 回溯路徑：從 sink 一路回到 source
        while v != source:
            u = parent[v]
            # 更新 bottleneck
            path_flow = min(path_flow, residual[u, v])
            v = u

        # 更新 residual graph
        v = sink
        while v != source:
            u = parent[v]

            # u -> v 路徑的流量已消耗，需扣除可用流量
            residual[u, v] -= path_flow

            # u -> v 路徑的流量已消耗，需增加反向路徑 v -> u 的可用流量
            residual[v, u] += path_flow

            v = u

        # 更新 flow
        max_flow += path_flow
    
    return max_flow, residual

# S -3→ A -2→ T
# |     |
# |     1
#  ↘︎    ↓
#    2→ B -3→ T

capacity: np.ndarray = np.array([
    # S  A  B  T
    [0, 3, 2, 0],  # S
    [0, 0, 1, 2],  # A
    [0, 0, 0, 3],  # B
    [0, 0, 0, 0]   # T
])
ic(capacity)

max_flow, residual = ford_fulkerson(capacity, 0, 3)
ic(max_flow)
ic(residual)
