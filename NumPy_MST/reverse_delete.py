import numpy as np

def reverse_delete_mst(adj_matrix):
    V = adj_matrix.shape[0]
    mst_adj = adj_matrix.copy()

    # 1. 取得所有邊 (只取上三角以避免重複)
    rows, cols = np.triu_indices(V, k=1)
    weights = adj_matrix[rows, cols]

    # 過濾掉權重為 0 的邊（不連通的邊）
    mask = weights > 0
    edge_list = np.column_stack((rows[mask], cols[mask], weights[mask]))

    # 2. 依照權重由大到小排序 (Reverse Sort)
    sorted_indices = np.argsort(edge_list[:, 2])[::-1]
    sorted_edges = edge_list[sorted_indices]

    # 3. 嘗試刪除邊
    for i in range(len(sorted_edges)):
        u, v, w = sorted_edges[i]
        u, v = int(u), int(v)

        # 暫時移除邊 (對稱矩陣)
        mst_adj[u, v] = 0
        mst_adj[v, u] = 0

        # 如果移除後導致不連通，則補回來
        if not is_connected(mst_adj, V):
            mst_adj[u, v] = w
            mst_adj[v, u] = w
    
    return mst_adj


def is_connected(adj_matrix, num_nodes: int) -> bool:
    """使用 BFS 檢查圖是否連通"""
    if num_nodes == 0:
        return True
    
    visited: np.ndarray = np.zeros(num_nodes, dtype=bool)
    queue: list[int] = [0]
    visited[0] = True
    count: int = 1

    while queue:
        u: int = queue.pop(0)
        # 找出所有與 u 相連且未訪問過的節點
        neighbors = np.where((adj_matrix[u] > 0) & (~visited))[0]
        for v in neighbors:
            visited[v] = True
            queue.append(v)
            count += 1
    
    return count == num_nodes
