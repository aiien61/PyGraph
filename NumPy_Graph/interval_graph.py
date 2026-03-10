import numpy as np

def build_interval_adjacency_matrix(intervals):
    """
    使用 NumPy 廣播機制建構鄰接矩陣
    intervals: shape (n, 2), 每行代表 [start, end]
    """
    # 提取所有起點與終點
    starts = intervals[:, 0]
    ends = intervals[:, 1]

    # 利用廣播 (Broadcasting) 計算所有成對的 max(start_i, start_j) 與 min(end_i, end_j)
    # starts[:, None] 變成 (n, 1), starts[None, :] 變成 (1, n)
    # 結果 max_starts 會是 (n, n)
    max_starts = np.maximum(starts[:, None], starts[None, :])
    min_ends = np.minimum(ends[: None], ends[None, :])

    # 判斷重疊：max_start < min_end
    adj_matrix = max_starts < min_ends

    # 移除自環 (節點與自己必重疊，但在圖論中通常不計自環)
    np.fill_diagonal(adj_matrix, 0)

    return adj_matrix.astype(int)

def color_interval_graph(intervals):
    n = intervals.shape[0]
    # 取得排序後的索引（按起點排序）
    idx = np.argsort(intervals[:, 0])
    sorted_intervals = intervals[idx]

    colors = np.full(n, -1, dtype=int)
    # 這裡可以用一個 Heap 來維護每種顏色目前的結束時間
    # 但為了展示 NumPy 邏輯，我們簡單描述其概念
    # 1. 遍歷排序後的區間
    # 2. 找到第一個結束時間早於目前起點的可用「顏色槽」
    pass


# 範例
intervals = np.array([
    [1, 5],
    [2, 6],
    [8, 10],
    [4, 9]
])

adj = build_interval_adjacency_matrix(intervals)
print(adj)