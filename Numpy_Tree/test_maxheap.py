import pytest
import numpy as np
from maxheap import MaxHeap, heapify, heap_sort

class TestMaxHeap:
    def test_initialization(self):
        """測試初始化是否正確建立 NaN 陣列"""
        capacity = 5
        mh = MaxHeap(capacity=capacity)
        assert mh.size == 0
        assert mh.capacity == capacity
        assert np.isnan(mh.heap).all()
        assert len(mh.heap) == capacity

    def test_push_and_maintains_max_property(self):
        """測試插入元素後，根節點是否始終為最大值"""
        mh = MaxHeap(capacity=10)
        elements = [10, 20, 5, 30, 15]
        for x in elements:
            mh.push(x)
        
        # 最大值應該在 heap[0]
        assert mh.heap[0] == 30
        assert mh.size == len(elements)
    
    def test_pop_order(self):
        """測試連續彈出時，是否依照從大到小的順序"""
        mh = MaxHeap(capacity=10)
        elements = [1, 5, 3, 10, 2]
        for x in elements:
            mh.push(x)
            
        results = []
        while mh.size > 0:
            results.append(mh.pop())
            
        assert results == [10, 5, 3, 2, 1]

    def test_ensure_capacity(self):
        """測試當 size 超過 capacity 時，陣列是否自動翻倍並填充 NaN"""
        initial_capacity = 2
        mh = MaxHeap(capacity=initial_capacity)
        
        # 插入 3 個元素 (超過原本的 2)
        mh.push(10)
        mh.push(20)
        mh.push(30)
        
        assert mh.capacity == 4  # 2 -> 4
        assert mh.size == 3
        assert np.isnan(mh.heap[3])  # 最後一個位置應該還是 NaN
        assert mh.heap[0] == 30  # 確保順序正確
    
    def test_pop_empty_heap(self):
        """測試在空堆積上 pop 的行為 (目前實作可能會報 IndexError，這是一個觀察點)"""
        mh = MaxHeap(capacity=5)
        # 如果你的實作沒有處理 size=0，這裡會報 index error
        with pytest.raises(IndexError):
            mh.pop()

class TestHeapFunctions:
    def test_heapify_basic(self):
        """測試 heapify 函式是否能將 list 轉為符合最大堆積性質的結構"""
        nums = [3, 1, 6, 5, 2, 4]
        heapify(nums)
        # 最大堆積性質：parent >= children
        n = len(nums)
        for i in range(n):
            left = 2 * i + 1
            right = 2 * i + 2
            if left < n:
                assert nums[i] >= nums[left]
            if right < n:
                assert nums[i] >= nums[right]

    def test_heap_sort_random(self):
        """測試堆積排序是否能將隨機數列轉為升冪排列"""
        nums: list[int] = [12, 11, 13, 5, 6, 7]
        expected: list[int] = sorted(nums.copy())
        heap_sort(nums, desc=False)
        assert nums == expected

        """測試堆積排序是否能將隨機數列轉為降冪排列"""
        nums: list[int] = [13, 10, 15, 50, 6, 27]
        expected: list[int] = sorted(nums.copy(), reverse=True)
        heap_sort(nums, desc=True)
        assert nums == expected


    def test_heap_sort_empty_and_single(self):
        """測試空列與單一元素的邊界情況"""
        empty_list = []
        heap_sort(empty_list)
        assert empty_list == []
        
        single_list: list[int] = [42]
        heap_sort(single_list)
        assert single_list == [42]

    def test_heap_sort_duplicates(self):
        """測試包含重複元素的排序"""
        nums: list[int] = [4, 1, 3, 2, 16, 9, 10, 14, 8, 7, 4]
        expected: list[int] = sorted(nums.copy())
        heap_sort(nums, desc=False)
        assert nums == expected