import numpy as np
import time
from maxheap import heap_sort

def stress_test_max_heap_sort():
    N = 100_000
    print(f"正在生成 {N} 筆隨機資料...")
    data = np.random.randn(N)
    
    # 複製一份供對照
    data_to_sort = data.copy()
    
    print("開始執行 max heap_sort...")
    start_time = time.time()
    heap_sort(data_to_sort, desc=True)
    end_time = time.time()
    
    # 驗證結果
    print("正在驗證排序結果...")
    # np.diff: out[i] = a[i+1] - a[i]
    is_sorted = np.all(np.diff(data_to_sort) <= 0)
    
    if is_sorted:
        print(f"✅ 測試通過！")
        print(f"耗時: {end_time - start_time:.4f} 秒")
    else:
        print("❌ 測試失敗：結果未正確排序")

def stress_test_min_heap_sort():
    N = 100_000
    print(f"正在生成 {N} 筆隨機資料...")
    data = np.random.randn(N)
    
    # 複製一份供對照
    data_to_sort = data.copy()
    
    print("開始執行 min heap_sort...")
    start_time = time.time()
    heap_sort(data_to_sort, desc=False)
    end_time = time.time()
    
    # 驗證結果
    print("正在驗證排序結果...")
    # np.diff: out[i] = a[i+1] - a[i]
    is_sorted = np.all(np.diff(data_to_sort) >= 0)
    
    if is_sorted:
        print(f"✅ 測試通過！")
        print(f"耗時: {end_time - start_time:.4f} 秒")
    else:
        print("❌ 測試失敗：結果未正確排序")

if __name__ == "__main__":
    stress_test_max_heap_sort()
    stress_test_min_heap_sort()
