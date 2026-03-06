from dataclasses import dataclass, field
from typing import Optional
import numpy as np


@dataclass
class MaxHeap:
    capacity: int
    heap: np.ndarray = field(init=False)
    size: int = 0

    def __post_init__(self):
        self.heap = np.full(self.capacity, np.nan, dtype=np.float64)
    
    def _ensure_capacity(self) -> None:
        if self.size == self.capacity:
            extra: np.ndarray = np.full(self.capacity, np.nan, dtype=self.heap.dtype)
            self.heap = np.concatenate([self.heap, extra])
            self.capacity *= 2
        return None
        
    def push(self, value: float) -> bool:
        self._ensure_capacity()
        self.heap[self.size] = value
        self.size += 1
        self._swim(self.size - 1)
        return True

    def pop(self) -> Optional[float]:
        if self.size == 0:
            raise IndexError("pop from empty heap")

        return_value: np.float64 = self.heap[0]
        self._swap(0, self.size - 1)
        self.heap[self.size - 1] = np.nan
        self.size -= 1
        self._sink(0)        
        return return_value

    def _swap(self, u: int, v: int) -> None:
        self.heap[u], self.heap[v] = self.heap[v], self.heap[u]
        return None

    def _sink(self, idx: int) -> None:
        while True:
            left: int = idx * 2 + 1
            right: int = idx * 2 + 2
            largest: int = idx

            if left < self.size and self.heap[largest] < self.heap[left]:
                largest = left

            if right < self.size and self.heap[largest] < self.heap[right]:
                largest = right

            if largest != idx:
                self._swap(idx, largest)
                idx = largest
            else:
                break
    
    def _swim(self, idx: int) -> None:
        while 0 < idx:     
            parent: int = (idx - 1) // 2
            if self.heap[parent] < self.heap[idx]:
                self._swap(parent, idx)
                idx = parent
            else:
                break
    
def heapify(nums: np.ndarray) -> None:
    """
    In-place heapify
    """
    n: int = len(nums)
    for i in range(n // 2 - 1, -1, -1):
        _internal_sink(nums, n, i)
    return None

def heap_sort(nums: np.ndarray, desc: bool = True) -> None:
    """
    In-palce heap sorting
    """
    n: int = len(nums)
    heapify(nums)

    for i in range(n - 1, 0, -1):
        nums[0], nums[i] = nums[i], nums[0]
        _internal_sink(nums, i, 0)
    
    if desc:
        nums[:] = nums[::-1]

    return None

def _internal_sink(nums: np.ndarray, n: int, i: int) -> None:
    parent: int = i
    while True:
        left: int = parent * 2 + 1
        right: int = parent * 2 + 2
        largest: int = parent

        if left < n and nums[largest] < nums[left]:
            largest = left
        
        if right < n and nums[largest] < nums[right]:
            largest = right
        
        if largest == parent:
            break

        nums[parent], nums[largest] = nums[largest], nums[parent]
        parent = largest
    
    return None
