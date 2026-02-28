from dataclasses import dataclass, field
from collections import deque
from NumPy_Graph.graph import Graph
from enum import Enum

@dataclass
class DirectedGRaph(Graph):
    """Directed Graph"""
    _lock: bool = False
    adj_list: dict[int, list[int]] = field(default_factory=dict)

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
        
        if successor in self.adj_list[predecessor]:
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
    
    def _bfs(self, start: int, graph: dict[int, list[int]]) -> set[int]:
        queue: deque[int] = deque([start])
        visited: set[int] = set()
        while queue:
            node: int = queue.popleft()
            if node in visited:
                continue

            visited.add(node)
            
            for successor in graph[node]:
                if successor not in visited:
                    queue.append(successor)
        
        return visited
    
    def _dfs(self, start: int, graph: dict[int, list[int]]) -> set[int]:
        stack: list[int] = [start]
        visited: set[int] = set()
        while stack:
            node: int = stack.pop()
            if node not in visited:
                visited.add(node)
                stack.extend(graph[node])

        return visited
    
    def _reverse_graph(self) -> dict[int, list[int]]:
        reverse_graph = {node: [] for node in self.adj_list}
        for predecessor in self.adj_list:
            for successor in self.adj_list[predecessor]:
                reverse_graph[successor].append(predecessor)
        return reverse_graph

    def is_mutually_reachable_bfs(self, u: int, v: int) -> bool:
        """verify mutual reachability between two nodes"""
        if not self.has_node(u) or not self.has_node(v):
            return False

        if u == v:
            return True
        
        reachable_from_u: bool = v in self._bfs(u, self.adj_list)
        if not reachable_from_u:
            return False
        
        reachable_from_v: bool = u in self._bfs(v, self.adj_list)
        return reachable_from_v
    
    def is_mutually_reachable_dfs(self, u: int, v: int) -> bool:
        """verify mutual reachability between two nodes"""
        if not self.has_node(u) or not self.has_node(v):
            return False
        
        if u == v:
            return True
        
        reachable_from_u: bool = v in self._dfs(u, self.adj_list)
        if not reachable_from_u:
            return False
        
        reachable_from_v: bool = u in self._dfs(v, self.adj_list)
        return reachable_from_v

    def is_strongly_connected(self) -> bool:
        if not self.adj_list:
            return True
        
        start = next(iter(self.adj_list))

        visited_forward = self._dfs(start, self.adj_list)
        if len(visited_forward) != len(self.adj_list):
            return False
        
        reverse_graph = self._reverse_graph()
        visited_reverse = self._dfs(start, reverse_graph)
        return len(visited_reverse) == len(self.adj_list)

    def get_strongly_connected_component(self, s: int) -> set[int]:
        if not self.has_node(s):
            return set()
        
        forward: set[int] = self._dfs(s, self.adj_list)
        reverse_graph: dict[int, list[int]] = self._reverse_graph()
        backward: set[int] = self._dfs(s, reverse_graph)
        
        return forward & backward
    
    def find_all_strongly_connected_components_kosaraju(self) -> list[set[int]]:
        """
        Implementation of Kosaraju's algorithm
        complexity: O(V + E)

        steps:
        1. find the order of finishing time
        2. reverse the graph
        3. run dfs based on finishing time order
        """
        visited: set[int] = set()
        order: list[int] = []

        def dfs1(node: int) -> None:
            visited.add(node)
            for successor in self.adj_list[node]:
                if successor not in visited:
                    dfs1(successor)
            order.append(node)
            return None

        # first pass: order by finish time
        for node in self.adj_list:
            if node not in visited:
                dfs1(node)
        
        reverse_graph: dict[int, list[int]] = self._reverse_graph()
        visited.clear()
        scc_list: list[set[int]] = []

        # second pass on reversed graph
        def dfs2(node: int, component: set[int]) -> None:
            visited.add(node)
            component.add(node)
            for successor in reverse_graph[node]:
                if successor not in visited:
                    dfs2(successor, component)
            return None
        
        for node in reversed(order):
            if node not in visited:
                scc = set()
                dfs2(node, scc)
                scc_list.append(scc)

        return scc_list
    
    def find_all_strongly_connected_components_tarjan(self) -> list[set[int]]:
        """
        Implementation of Tarjan's algorithm
        """
        index: int = 0
        stack: list[int] = []
        on_stack: set[int] = set()

        indices: dict[int, int] = {}
        lowlink: dict[int, int] = {}

        scc_list: list[set[int]] = []

        def strongconnect(node: int):
            nonlocal index

            indices[node] = index
            lowlink[node] = index
            index += 1

            stack.append(node)
            on_stack.add(node)

            for successor in self.adj_list.get(node, []):
                if successor not in indices:
                    strongconnect(successor)
                    lowlink[node] = min(lowlink[node], lowlink[successor])
                elif successor in on_stack:
                    lowlink[node] = min(lowlink[node], indices[successor])

            if lowlink[node] == indices[node]:
                scc: set[int] = set()
                while True:
                    w: int = stack.pop()
                    on_stack.remove(w)
                    scc.add(w)
                    if w == node:
                        break
                scc_list.append(scc)

        for node in list(self.adj_list.keys()):
            if node not in indices:
                strongconnect(node)

        return scc_list
    
    def has_cycle_by_dfs(self) -> bool:
        """
        A → B → C → D
            ↑       ↓
            └───────┘
        
        Concept:
        1. 當 DFS 走到 D
        2. D 指向 B
        3. B 還在 recursion stack
        4. 發現 cycle    
        """
        marked: set[int] = set()
        in_stack: dict[int, bool] = {}

        def _dfs(predecessor):
            in_stack[predecessor] = True
            marked.add(predecessor)

            for successor in self.adj_list[predecessor]:
                if successor not in marked:
                    # if cycle found
                    if _dfs(successor):
                        return True
                else:
                    # if successor was visited and is still in stack i.e. back edge
                    if in_stack.get(successor):
                        return True
            
            in_stack[predecessor] = False
            return False
        
        for node in self.adj_list:
            if node not in marked:
                if _dfs(node):
                    return True
        return False
    
    def has_cycle_by_three_colors(self) -> bool:
        class State(Enum):
            UNVISITED = "unvisited"
            VISITING = "visiting"
            VISITED = "visited"
        
        state: dict[int, State] = {v: State.UNVISITED for v in self.adj_list}

        def _dfs(predecessor: int):
            state[predecessor] = State.VISITING

            for successor in self.adj_list[predecessor]:
                if state[successor] == State.VISITING:
                    return True  # back edge
                if state[successor] == State.UNVISITED:
                    if _dfs(successor):
                        return True
            
            state[predecessor] = State.VISITED
            return False
        
        for v in self.adj_list:
            if state[v] == State.UNVISITED:
                if _dfs(v):
                    return True
        
        return False
    
    def has_cycle_by_kahn(self) -> bool:
        indegree: dict[int, int] = {v: 0 for v in self.adj_list}

        for predecessor in self.adj_list:
            for successor in self.adj_list[predecessor]:
                indegree[successor] = indegree.get(successor, 0) + 1
        
        queue: deque[int] = deque([v for v in self.adj_list if indegree[v] == 0])
        count: int = 0

        while queue:
            predecessor = queue.popleft()
            count += 1

            for successor in self.adj_list[predecessor]:
                indegree[successor] -= 1
                if indegree[successor] == 0:
                    queue.append(successor)

        return count != len(self.adj_list)
