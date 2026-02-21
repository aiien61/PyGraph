import numpy as np
from icecream import ic


print("\n產能分配 / TOC 平衡 / 解資源平衡 ：")
print("np.linalg.solve(A, b)")
print("""
情境
2 台機器產能要滿足訂單：
      M1 + M2 = 10
     2M1 + M2 = 16
""")
A = np.array([
    [1, 1],
    [2, 1]
])
ic(A)

b = np.array([10, 16])
ic(b)

ic(np.linalg.solve(A, b))
print("M1=6, M2=4")


print("\n系統穩定度 / flow 分析 / 瓶頸分析 ：")
print("np.linalg.eig(matrix)")
print("""
情境
工序轉移矩陣：
    flow = np.array([
        [0, 1, 0],
        [0, 0, 1],
        [0.5, 0, 0]
    ])
""")

flow = np.array([
    [0, 1, 0],
    [0, 0, 1],
    [0.5, 0, 0]
])

print("eigvals, eigvecs = np.linalg.eig(flow)")
eigvals, eigvecs = np.linalg.eig(flow)
ic(eigvals)
ic(eigvecs)
print("""
最大特徵值 ≈ 系統循環強度 or 壅塞程度

用於：生產線穩定度、WIP 爆量預測、瓶頸迴圈偵測
""")