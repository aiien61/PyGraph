"""
Kosaraju Algorithm

graph = {
    'a': ['b'],
    'b': ['c', 'e', 'f'],
    'c': ['d', 'g'],
    'd': ['c', 'h'],
    'e': ['a', 'f'],
    'f': ['g'],
    'g': ['f', 'h'],
    'h': ['h']
}
"""
from icecream import ic

# call DFS(G) to compute finish times u.f
def dfs_first_pass(graph: dict[str, list[str]]) -> list[str]:
    visited: set[str] = set()
    finish_stack: list[str] = []

    def dfs(u):
        visited.add(u)
        for v in graph[u]:
            if v not in visited:
                dfs(v)
        
        # 所有子節點走完才加入（finish time）
        finish_stack.append(u)
    
    for node in graph:
        if node not in visited:
            dfs(node)
    
    return finish_stack

# create transpose of G
def transpose_graph(graph):
    transposed = {node: [] for node in graph}

    for u in graph:
        for v in graph[u]:
            transposed[v].append(u)  # 反轉邊: u → v 變成 v → u
    
    return transposed

# call DFS(G^T)，但依照「f[u] 由大到小」順序
def dfs_second_pass(graph, finish_stack):
    visited = set()
    scc_list = []

    def dfs(u, component):
        visited.add(u)
        component.append(u)
        for v in graph[u]:
            if v not in visited:
                dfs(v, component)
    
    # 由 finish time 大 → 小
    while finish_stack:
        node = finish_stack.pop()   # 取最後完成的
        if node not in visited:
            component = []
            dfs(node, component)
            scc_list.append(component)

    return scc_list


def kosaraju(graph):
    # Step 1: 第一次 DFS
    finish_stack = dfs_first_pass(graph)

    # Step 2: 轉置圖
    transposed = transpose_graph(graph)

    # Step 3: 第二次 DFS
    scc = dfs_second_pass(transposed, finish_stack)

    return scc

if __name__ == "__main__":
    graph = {
        'a': ['b'],
        'b': ['c', 'e', 'f'],
        'c': ['d', 'g'],
        'd': ['c', 'h'],
        'e': ['a', 'f'],
        'f': ['g'],
        'g': ['f', 'h'],
        'h': ['h']
    }

    scc = kosaraju(graph)
    ic(scc)
    