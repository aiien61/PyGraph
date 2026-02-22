from dataclasses import dataclass, field
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
    
    def dfs_preorder_recursive_standard(self) -> list[int]:
        result: list[int] = []
        
        def _dfs(i: int):
            if self.is_null(i):
                return None
            
            result.append(self.nums[i].item())

            _dfs(i * 2 + 1)
            _dfs(i * 2 + 2)
        
        _dfs(0)
        return result
    
    def dfs_preorder_recursive_gen(self, i: int):
        if self.is_null(i):
            return None
        
        yield self.nums[i].item()
        yield from self.dfs_preorder_recursive_gen(i * 2 + 1)
        yield from self.dfs_preorder_recursive_gen(i * 2 + 2)

    def dfs_inorder_recursive_standard(self) -> list[int]:
        result: list[int] = []

        def _dfs(i: int):
            if self.is_null(i):
                return None
            
            _dfs(i * 2 + 1)
            result.append(self.nums[i].item())
            _dfs(i * 2 + 2)

        _dfs(0)
        return result
    
    def dfs_inorder_recursive_gen(self, i: int):
        if self.is_null(i):
            return None
        
        yield from self.dfs_inorder_recursive_gen(i * 2 + 1)
        yield self.nums[i].item()
        yield from self.dfs_inorder_recursive_gen(i * 2 + 2)

    def dfs_postorder_recursive_standard(self) -> list[int]:
        result: list[int] = []

        def _dfs(i: int):
            if self.is_null(i):
                return None
            
            _dfs(i * 2 + 1)
            _dfs(i * 2 + 2)
            result.append(self.nums[i].item())

        _dfs(0)
        return result
    
    def dfs_postorder_recursive_gen(self, i: int):
        if self.is_null(i):
            return None
        
        yield from self.dfs_postorder_recursive_gen(i * 2 + 1)
        yield from self.dfs_postorder_recursive_gen(i * 2 + 2)
        yield self.nums[i].item()


bt = Tree([5,3,7,2,4,6,8,1])
ic(bt.nums)
ic(bt.dfs_preorder())
ic(bt.dfs_inorder())
ic(bt.dfs_postorder())
ic(bt.dfs_preorder_recursive_standard())
ic(list(bt.dfs_preorder_recursive_gen(0)))
ic(bt.dfs_inorder_recursive_standard())
ic(list(bt.dfs_inorder_recursive_gen(0)))
ic(bt.dfs_postorder_recursive_standard())
ic(list(bt.dfs_postorder_recursive_gen(0)))
