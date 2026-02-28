from dataclasses import dataclass, field
from collections import deque
from icecream import ic

from NumPy_Graph.graph import Graph

@dataclass(slots=True)
class UndirectedGraph(Graph):
    _lock: bool = True
    adjacency_list: dict[int, list[int]] = field(default_factory=dict)

    def __repr__(self):
        result: str = ""
        for node, neighbors in self.adjacency_list.items():
            result += f"{node}: {neighbors}"
            result += "\n"
        return result
    
    def lock(self):
        self._lock = True
    
    def unlock(self):
        self._lock = False
    
    def has_node(self, node: int) -> bool:
        if node in self.adjacency_list:
            return True
        return False

    def add_node(self, node: int) -> bool:
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []
            return True
        return False
    
    def add_edge(self, from_node: int, to_node: int) -> bool:
        if self.has_node(from_node) and self.has_node(to_node):
            self.adjacency_list[from_node].append(to_node)
            self.adjacency_list[to_node].append(from_node)
            return True
        return False
    
    def remove_node(self, node: int) -> bool:
        if not self.has_node(node):
            return False
        
        neighbors: list[int] = self.adjacency_list.get(node)
        if neighbors:
            if self._lock:
                return False
        
            for neighbor in neighbors:
                self.adjacency_list[neighbor].remove(node)
        
        del self.adjacency_list[node]
        return True

    def remove_edge(self, from_node: int, to_node: int) -> bool:
        if not self.has_node(from_node) or not self.has_node(to_node):
            return False
        
        if to_node not in self.adjacency_list[from_node]:
            return False

        if from_node not in self.adjacency_list[to_node]:
            return False
             
        self.adjacency_list[from_node].remove(to_node)
        self.adjacency_list[to_node].remove(from_node)
        return True
    
    def dfs(self, start_node: int, seen: set[int] = None) -> list[int]:
        """使用外部傳入的 seen 集合來進行 DFS 遍歷，減少重複開銷"""
        if seen is None:
            seen = set()

        result: list[int] = []

        def _dfs(node: int):
            if node in seen:
                return None
            result.append(node)
            seen.add(node)

            for next_node in self.adjacency_list[node]:
                _dfs(next_node)

        _dfs(start_node)
        return result

    def search_connected_components(self) -> list[list]:
        """找出圖中所有相連元件"""
        seen: set[int] = set()
        all_components: list[list] = []
        
        for node in self.adjacency_list.keys():
            if node not in seen:
                component: list[int] = self.dfs(node, seen)
                all_components.append(component)
        
        return all_components
    
    def hash_path(self, start: int, end: int) -> bool:
        """Verify whether there is a path between the given nodes."""
        seen: set[int] = set()
        def _dfs(node: int):
            if node in seen:
                return None
            seen.add(node)
            for next_node in self.adjacency_list[node]:
                _dfs(next_node)

        _dfs(start)
        return end in seen
    
    def bfs(self, start_node: int) -> list[int]:
        result: list[int] = []
        seen: set[int] = {start_node}
        q: deque[int] = deque([start_node])
        while q:
            node: int = q.popleft()
            result.append(node)

            for next_node in self.adjacency_list[node]:
                if next_node not in seen:
                    seen.add(next_node)
                    q.append(next_node)
        
        return result
    
    def get_bipartite(self):
        color: dict[int, bool] = {}

        def _bfs(start):
            queue: deque[int] = deque([start])
            color[start] = True
            while queue:
                u = queue.popleft()
                for v in self.adjacency_list[u]:
                    if v not in color:
                        color[v] = not color[u]
                        queue.append(v)
                    elif color[v] == color[u]:
                        return False
            return True
        
        unvisited = set(self.adjacency_list)
        while unvisited:
            start = unvisited.pop()

            if start not in color:
                if not _bfs(start):
                    return {}
            
            unvisited -= color.keys()            
        
        return color
    
    @staticmethod
    def path_to(node_from, src, target):
        if target not in node_from:
            raise ValueError("Unreachable")
        path: list[int] = []
        v: int = target
        while v != src:
            path.append(v)
            v = node_from[v]
        
        path.append(src)
        path.reverse()
        return path
