from dataclasses import dataclass, field
from collections import deque
from icecream import ic
import numpy as np

@dataclass
class Tree:
    nums_input: list[int]
    nums: np.ndarray = field(init=False)
    size: int = field(init=False)

    def __post_init__(self):
        self.nums = np.array(self.nums_input)
        self.size = len(self.nums)

    def is_null(self, index: int) -> bool:
        if self.size <= index:
            return True

        val: int = self.nums[index] 
        if np.issubdtype(self.nums.dtype, np.floating):
            return np.isnan(val)
        return False

    def dfs_preorder(self) -> list[int]:
        result: list[int] = []
        stack: list[int] = [0]
        while stack:
            i: int = stack.pop()

            val: np.int64 = self.nums[i]

            if self.size <= i or np.isnan(val):
                continue

            result.append(val.item())
            
            right_i: int = (i + 1) * 2
            if right_i < self.size:
                stack.append(right_i)
            
            left_i: int = (i + 1) * 2 - 1
            if left_i < self.size:
                stack.append(left_i)
        return result

    def dfs_inorder(self) -> list[int]:
        result: list[int] = []
        stack: list[int] = []
        i: int = 0
        while stack or i < self.size:
            while not self.is_null(i):
                stack.append(i)
                left_i: int = (i + 1) * 2 - 1
                i = left_i
            
            i = stack.pop()
            result.append(self.nums[i].item())

            right_i: int = (i + 1) * 2
            i = right_i
        
        return result        

    def dfs_postorder(self):
        result: list[int] = []
        stack: list[int] = []
        i: int = 0
        last_visited: int = -1
        while stack or i < self.size:
            while not self.is_null(i):
                stack.append(i)
                left_i: int = (i + 1) * 2 - 1
                i = left_i

            parent_i: int = stack[-1]
            right_i: int = (parent_i + 1) * 2
            if self.is_null(right_i) or last_visited == right_i:
                parent_i = stack.pop()
                result.append(self.nums[parent_i].item())
                last_visited = parent_i
            else:
                i = right_i
        return result


bt = Tree([5,3,7,2,4,6,8,1])
ic(bt.nums)
ic(bt.dfs_preorder())
ic(bt.dfs_inorder())
ic(bt.dfs_postorder())
