from dataclasses import dataclass, field
from collections import deque
from icecream import ic
from cytoolz.curried import pipe, sorted as c_sorted
from NumPy_Graph.graph import Graph


@dataclass
class DAG(Graph):
    """Directed Acyclic Graph"""
    adj_list: dict[int, list[int]] = field(default_factory=dict)
    _lock: bool = False

    def __repr__(self):
        return str(self.adj_list)

    def lock(self) -> None:
        self._lock = True
        return None
    
    def unlock(self) -> None:
        self._lock = False
        return None

    def has_node(self, node: int) -> bool:
        return True if node in self.adj_list else False
    
    def add_node(self, node: int) -> bool:
        if self.has_node(node):
            return False
        self.adj_list[node] = []
        return True

    def add_edge(self, predecessor: int, successor: int) -> bool:
        if not self.has_node(predecessor) or not self.has_node(successor):
            return False
        
        self.adj_list[predecessor].append(successor)
        return True

    def remove_edge(self, predecessor: int, successor: int) -> bool:
        if not self.has_node(predecessor) or not self.has_node(successor):
            return False
        
        if successor not in self.adj_list[predecessor]:
            return False
        
        self.adj_list[predecessor].remove(successor)
        return True

    def remove_node(self, node: int) -> bool:
        if not self.has_node(node):
            return False
        
        if self.adj_list[node]:
            if self._lock:
                return False
        
        del self.adj_list[node]
        return True
    
    def topological_sort_dfs(self) -> list[int]:
        visited: set[int] = set()
        in_stack: set[int] = set()
        postorder: list[int] = []

        def _dfs(node: int) -> None:
            if node in in_stack:
                raise ValueError("Graph is not a DAG (cycle detected)")
            if node in visited:
                return
            
            in_stack.add(node)
            for successor in self.adj_list.get(node, []):
                _dfs(successor)
            
            in_stack.remove(node)
            visited.add(node)
            postorder.append(node)
        
        for node in self.adj_list:
            if node not in visited:
                _dfs(node)

        topological_ordering: list[int] = reversed(postorder)
        return topological_ordering
    
    def topological_sort_kahn(self) -> list[int]:
        in_degree: dict[int, int] = {node: 0 for node in self.adj_list}

        for predecessor in self.adj_list:
            for successor in self.adj_list[predecessor]:
                in_degree[successor] = in_degree.get(successor, 0) + 1
        
        queue = deque([node for node in in_degree if in_degree[node] == 0])

        topological_ordering: list[int] = []

        while queue:
            predecessor: int = queue.popleft()
            topological_ordering.append(predecessor)

            for successor in self.adj_list.get(predecessor, []):
                in_degree[successor] -= 1
                if in_degree[successor] == 0:
                    queue.append(successor)
        
        if len(topological_ordering) != len(in_degree):
            raise ValueError("Graph is not a DAG (cycle detected)")
        
        return topological_ordering
