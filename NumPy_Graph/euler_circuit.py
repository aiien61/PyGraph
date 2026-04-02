"""
Euler Circuit

In a strongly connected directed graph G = (V, E),
Euler circuit means a path from a random origin vertex goes through 
each edge once and only once to return the origin
"""
from collections import defaultdict

def hierholzer_algorithm(graph):
    """
    Use Hierholzer's Algorithm to find Euler circuit

    graph: dict {u: [v1, v2, ...]}
    """
    g = {u: list(vs) for u, vs in graph.items()}

    start = next(iter(graph))

    stack = [start]
    circuit = []

    while stack:
        u = stack[-1]

        if g[u]: # 還有邊可以走
            v = g[u].pop()
            stack.append(v)
        else:   # 沒邊了 → 回溯
            circuit.append(stack.pop())  
    
    return circuit[::-1]

