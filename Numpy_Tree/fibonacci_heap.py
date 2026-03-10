from dataclasses import dataclass, field
from typing import Optional, Self

@dataclass
class FibonacciHeapNode:
    key: int
    value: int
    degree: int = 0
    parent: Optional[int] = None
    child: Optional[int] = None
    left: Self = field(init=False)
    right: Self = field(init=False)
    mark: bool = False

    def __post_init__(self):
        self.left = self
        self.right = self

class FibonacciHeap:
    def __init__(self):
        self.min_node = None
        self.total_nodes = 0

    def insert(self, key, value):
        # O(1) 實作：建立節點並加入根列表
        pass

    def extract_min(self):
        # O(log n) 實作：移除最小節點並進行 Consolidate
        pass

    def decrease_key(self, node, new_key):
        # O(1) 實作：如果違反堆疊性質，執行 Cut 與 Cascading Cut
        pass