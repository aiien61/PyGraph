from dataclasses import dataclass, field
from collections import deque
from icecream import ic
import numpy as np

@dataclass
class Tree:
    nums_input: list[int]
    nums: np.ndarray = field(init=False)
    size: int = 0

    def __post_init__(self):
        self.nums = np.array(self.nums_input)
        self.size = len(self.nums)

    def bfs_levelorder(self):
        result: list[int] = []
        i: int = 0
        if self.size == 0 or np.isnan(self.nums[i]):
            return result

        queue: deque[int] = deque([i])
        
        while queue:
            i = queue.popleft()

            val: int = self.nums[i]
            result.append(val.item())

            left_i: int = (i + 1) * 2 - 1          
            right_i: int = (i + 1) * 2
            for child_i in [left_i, right_i]:
                if child_i < self.size and not np.isnan(self.nums[child_i]):
                    queue.append(child_i)
        
        return result

bt = Tree([5, 3, 7, 2, 4, 6, 8, 1])
ic(bt.nums)
ic(bt.bfs_levelorder())

