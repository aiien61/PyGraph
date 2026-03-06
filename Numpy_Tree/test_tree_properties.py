import pytest
import numpy as np
from tree_properties import is_full, is_perfect, is_complete, has_single_parent

class TestTreeProperties:
    
    # 1. 測試 Is Full Binary Tree
    def test_is_full(self):
        # 滿二元樹：每個節點 0 或 2 個小孩
        assert is_full(np.array([1, 2, 3])) is True
        assert is_full(np.array([1])) is True
        assert is_full(np.array([1, 2, 3, 4, 5, 6, 7])) is True
        
        # 非滿二元樹：有一個節點只有左小孩
        assert is_full(np.array([1, 2, np.nan])) is False
        # 非滿二元樹：中間有空缺導致單親
        assert is_full(np.array([1, 2, 3, 4, np.nan, 6, 7])) is False

    # 2. 測試 Is Perfect Binary Tree
    def test_is_perfect(self):
        # 完美二元樹：節點數必須是 2^h - 1 且全滿
        assert is_perfect(np.array([1])) is True  #(h=1, n=1)
        assert is_perfect(np.array([1, 2, 3])) is True # (h=2, n=3)
        assert is_perfect(np.array([1, 2, 3, 4, 5, 6, 7])) is True # (h=3, n=7)
        
        # 非完美：數量不對 (n=2)
        assert is_perfect(np.array([1, 2])) is False
        # 非完美：數量對但中間有 nan
        assert is_perfect(np.array([1, 2, np.nan])) is False

    # 3. 測試 Is Complete Binary Tree
    def test_is_complete(self):
        # 完全二元樹：節點靠左，中間無空隙
        assert is_complete(np.array([1, 2, 3, 4])) is True
        assert is_complete(np.array([1, 2, 3, 4, 5])) is True
        
        # 非完全：中間有 nan (gap)
        assert is_complete(np.array([1, np.nan, 3])) is False
        assert is_complete(np.array([1, 2, 3, np.nan, 5])) is False

    # 4. 測試 Has Single Parent
    def test_has_single_parent(self):
        # 存在單親的情況
        assert has_single_parent(np.array([1, 2, np.nan])) is True
        assert has_single_parent(np.array([1, np.nan, 3])) is True
        
        # 不存在單親 (或是葉子，或是雙親)
        assert has_single_parent(np.array([1, 2, 3])) is False
        assert has_single_parent(np.array([1])) is False
        # 完美樹一定沒有單親
        assert has_single_parent(np.array([1, 2, 3, 4, 5, 6, 7])) is False

    # 5. 邊界情況：空樹
    def test_empty_tree(self):
        empty = np.array([])
        assert is_full(empty) is True
        assert is_perfect(empty) is True
        assert is_complete(empty) is True
        assert has_single_parent(empty) is False
