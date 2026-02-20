from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Self, Optional
from collections import deque
from icecream import ic
import numpy as np

@dataclass
class Node:
    value: Optional[int]
    left: Optional[Self] = None
    right: Optional[Self] = None

@dataclass
class BST(ABC):
    @abstractmethod
    def insert(self): raise NotImplementedError

@dataclass
class BST_List(BST):
    root: Optional[Node] = None          

    def insert(self, value) -> bool:
        new_node: Node = Node(value)

        if not self.root:
            self.root = new_node
            return True
        
        temp = self.root
        while True:
            if value == temp.value:
                return False
            
            if value < temp.value:
                if not temp.left:
                    temp.left = new_node
                    return True
                temp = temp.left
            elif value > temp.value:
                if not temp.right:
                    temp.right = new_node
                    return True
                temp = temp.right

    def bfs_levelorder(self) -> list[int]:
        result: list[int] = []

        if not self.root:
            return result
        
        queue: deque[Node] = deque([self.root])
        while queue:
            node: Node = queue.popleft()
            result.append(node.value)

            for child_node in [node.left, node.right]:
                if child_node:
                    queue.append(child_node)

        return result
    
    def contains(self, value: int) -> bool:
        if self.root is None:
            return False
        
        temp: Node = self.root
        while temp is not None:
            if value < temp.value:
                temp = temp.left
            elif temp.value < value:
                temp = temp.right
            else:
                return True
        return False
    
@dataclass
class BST_Array(BST):
    nums_input: list[int] = field(default_factory=list)
    nums: np.ndarray = field(default_factory=lambda: np.array([], dtype=np.float64))
    count: int = 0

    def __post_init__(self):
        if self.nums_input:
            for x in self.nums_input:
                self.insert(x)
    
    def _ensure_capacity(self, target_index: int) -> None:
        """確保陣列長度足以容納目標索引"""
        if target_index >= len(self.nums):
            new_size: int = target_index + 1
            extension = np.full((new_size - len(self.nums),), np.nan)
            self.nums = np.concatenate([self.nums, extension])
        return None
    
    def is_null(self, target_index: int) -> bool:
        if len(self.nums) <= target_index:
            return True
        if np.isnan(self.nums[target_index]):
            return True
        return False
    
    def insert(self, value: int) -> bool:
        if len(self.nums) == 0:
            self.nums = np.array([value], dtype=np.float64)
            self.count += 1
            return True
        
        stack: list[int] = [0]
        
        while stack:
            i: int = stack.pop()
            if self.nums[i] == value:
                return False
            
            left_i: int = (i + 1) * 2 - 1
            right_i: int = (i + 1) * 2
            next_i: int = left_i if value < self.nums[i] else right_i
            self._ensure_capacity(next_i)
            if np.isnan(self.nums[next_i]):
                self.nums[next_i] = value
                self.count += 1
                return True
            stack.append(next_i)

    def bfs_levelorder(self) -> list[int]:
        result: list[int] = []
        if self.count == 0:
            return result

        queue: deque[int] = deque([0])
        while queue:
            i: int = queue.popleft()
            val: np.float64 = self.nums[i]
            if not np.isnan(val):
                result.append(val.item())

            left_i: int = (i + 1) * 2 - 1
            right_i: int = (i + 1) * 2
            for child_i in [left_i, right_i]:
                if len(self.nums) <= child_i:
                    continue
                queue.append(child_i)

        return result
    
    def contains(self, value: int) -> bool:
        if len(self.nums) == 0:
            return False

        i: int = 0
        while not self.is_null(i):
            if value == self.nums[i]:
                return True
            
            left_i: int = (i + 1) * 2 - 1
            right_i: int = (i + 1) * 2
            i = left_i if value < self.nums[i] else right_i
        return False


def main():
    bt = BST_List()
    bt.insert(3)
    bt.insert(1)
    bt.insert(5)
    ic(bt.bfs_levelorder())
    ic(bt.contains(5))
    ic(bt.contains(10))

    bt_array = BST_Array()
    bt_array.insert(3)
    bt_array.insert(1)
    bt_array.insert(5)
    bt_array.insert(2)
    ic(bt_array.nums)
    ic(bt_array.bfs_levelorder())
    ic(bt_array.contains(2))
    ic(bt_array.contains(10))


if __name__ == "__main__":
    main()
