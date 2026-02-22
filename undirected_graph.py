from dataclasses import dataclass, field
from icecream import ic

@dataclass(slots=True)
class UndirectedGraph:
    _lock: bool = False
    adjacency_list: dict[str, list[str]] = field(default_factory=dict)

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
    
    def has_node(self, node: str) -> bool:
        if node in self.adjacency_list:
            return True
        return False

    def add_node(self, node: str) -> bool:
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []
            return True
        return False
    
    def add_edge(self, from_node: str, to_node: str) -> bool:
        if self.has_node(from_node) and self.has_node(to_node):
            self.adjacency_list[from_node].append(to_node)
            self.adjacency_list[to_node].append(from_node)
            return True
        return False
    
    def remove_node(self, node: str) -> bool:
        if not self.has_node(node):
            return False
        
        neighbors: list[str] = self.adjacency_list.get(node)
        if neighbors:
            if self._lock:
                return False
        
            for neighbor in neighbors:
                self.adjacency_list[neighbor].remove(node)
        
        del self.adjacency_list[node]
        return True

    def remove_edge(self, from_node: str, to_node: str) -> bool:
        if not self.has_node(from_node) or not self.has_node(to_node):
            return False
        
        if to_node not in self.adjacency_list[from_node]:
            return False

        if from_node not in self.adjacency_list[to_node]:
            return False
             
        self.adjacency_list[from_node].remove(to_node)
        self.adjacency_list[to_node].remove(from_node)
        return True
    

graph = UndirectedGraph()
for new_node in 'ABCDE':
    graph.add_node(new_node)

graph.add_edge('A', 'B')
graph.add_edge('B', 'C')
graph.add_edge('C', 'D')
graph.add_edge('D', 'E')
graph.add_edge('E', 'A')
ic(graph)

graph.add_node('F')
ic(graph)

graph.remove_edge('A', 'F')
ic(graph)

graph.remove_edge('A', 'B')
graph.remove_edge('A', 'E')
ic(graph)


graph.remove_node('A')
ic(graph)

graph.lock()
graph.remove_node('E')
ic(graph)

graph.unlock()
graph.remove_node('E')
ic(graph)

