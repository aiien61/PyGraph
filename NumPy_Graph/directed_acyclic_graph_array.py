from dataclasses import dataclass, field
from collections import deque
from icecream import ic
from cytoolz.curried import pipe, sorted as c_sorted


@dataclass
class DAG:
    """Array-based Directed Acyclic Graph"""

    N: int
    predecessors: list[list[int]] = field(init=False)
    successors: list[list[int]] = field(init=False)
    in_degree: list[int] = field(init=False)
    _lock: bool = False

    def __post_init__(self):
        self.predecessors = [[] for _ in range(self.N)]
        self.successors = [[] for _ in range(self.N)]
        self.in_degree = [0] * self.N
    
    def __repr__(self):
        return str(self.successors)
    
    # -------------------------
    # Lock control
    # -------------------------
    def lock(self) -> None:
        self._lock = True
        return None
    
    def unlock(self) -> None:
        self._lock = False
        return None
    
    # -------------------------
    # Edge operations
    # -------------------------
    def add_edge(self, predecessor: int, successor: int) -> bool:
        if self._lock:
            return False
        
        if not (0 <= predecessor < self.N and 0 <= successor < self.N):
            return False
        
        self.successors[predecessor].append(successor)
        self.predecessors[successor].append(predecessor)
        self.in_degree[successor] += 1

        return True
    
    def remove_edge(self, predecessor: int, successor: int) -> bool:
        if self._lock:
            return False
        
        if predecessor not in self.predecessors[successor]:
            return False

        if successor not in self.successors[predecessor]:
            return False
        
        self.predecessors[successor].remove(predecessor)
        self.successors[predecessor].remove(successor)

        self.in_degree[successor] -= 1

        return True
    
    # -------------------------
    # Topological Sort (Kahn)
    # -------------------------
    def topological_sort(self) -> list[int]:
        """Get topological ordering by Kahn's algorithm"""
        in_degree: list[int] = self.in_degree.copy()
        queue: deque[int] = deque([i for i in range(self.N) if in_degree[i] == 0])
        ordering: list[int] = []

        while queue:
            predecessor: int = queue.popleft()
            ordering.append(predecessor)
            for successor in self.successors[predecessor]:
                in_degree[successor] -= 1
                if in_degree[successor] == 0:
                    queue.append(successor)
        
        if len(ordering) != len(in_degree):
            raise ValueError("Cycle detected")
        
        return ordering
