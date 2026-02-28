import pytest
from collections import deque
from NumPy_Graph.undirected_graph import UndirectedGraph

# -------------------------
# Fixtures
# -------------------------

@pytest.fixture
def empty_graph():
    return UndirectedGraph()

@pytest.fixture
def linear_graph():
    """ 1 - 2 - 3 """
    g = UndirectedGraph()
    for i in [1, 2, 3]: g.add_node(i)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.unlock() # 預設是鎖定的，解鎖以便進行某些刪除測試
    return g

@pytest.fixture
def disconnected_graph():
    """ (1-2)  (3-4) """
    g = UndirectedGraph()
    for i in range(1, 5): g.add_node(i)
    g.add_edge(1, 2)
    g.add_edge(3, 4)
    return g

# -------------------------
# Basic Operations Tests
# -------------------------

def test_add_edge_is_undirected(empty_graph):
    empty_graph.add_node(1)
    empty_graph.add_node(2)
    empty_graph.add_edge(1, 2)
    # 無向圖中，1 的鄰居應有 2，2 的鄰居應有 1
    assert 2 in empty_graph.adjacency_list[1]
    assert 1 in empty_graph.adjacency_list[2]

def test_remove_edge(linear_graph):
    assert linear_graph.remove_edge(1, 2) is True
    assert 2 not in linear_graph.adjacency_list[1]
    assert 1 not in linear_graph.adjacency_list[2]

def test_remove_node_lock_behavior():
    g = UndirectedGraph()
    g.add_node(1)
    g.add_node(2)
    g.add_edge(1, 2)
    
    # 預設 _lock = True，且有鄰居，應刪除失敗
    assert g.remove_node(1) is False
    
    g.unlock()
    assert g.remove_node(1) is True
    assert 1 not in g.adjacency_list[2] # 檢查鄰居的清單是否也更新了

# -------------------------
# Traversal & Path Tests
# -------------------------

def test_dfs_bfs_order(linear_graph):
    # 雖然順序可能因實作而異，但節點集應一致
    assert set(linear_graph.dfs(1)) == {1, 2, 3}
    assert set(linear_graph.bfs(1)) == {1, 2, 3}

def test_hash_path(disconnected_graph):
    assert disconnected_graph.hash_path(1, 2) is True
    assert disconnected_graph.hash_path(1, 4) is False

def test_connected_components(disconnected_graph):
    components = disconnected_graph.search_connected_components()
    # 應該有兩個組件：{1, 2} 和 {3, 4}
    assert len(components) == 2
    comp_sets = [set(c) for c in components]
    assert {1, 2} in comp_sets
    assert {3, 4} in comp_sets

# -------------------------
# Bipartite Tests
# -------------------------

def test_is_bipartite_true(linear_graph):
    # 線性圖 1-2-3 是二分圖 (1:色A, 2:色B, 3:色A)
    color_map = linear_graph.get_bipartite()
    assert bool(color_map) is True
    assert color_map[1] != color_map[2]
    assert color_map[2] != color_map[3]

def test_is_bipartite_false():
    """ 測試三角形 (1-2-3-1)，這不是二分圖 """
    g = UndirectedGraph()
    for i in [1, 2, 3]: g.add_node(i)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 1)
    
    color_map = g.get_bipartite()
    assert color_map == {} # 根據 code，不是二分圖回傳空字典

# -------------------------
# Static Method / Logic Check
# -------------------------

def test_path_to_logic():
    # 這裡我們模擬它的邏輯或呼叫方式
    node_from = {2: 1, 3: 2, 4: 1} # 1是起點, 2來自1, 3來自2, 4來自1
    
    # 測試從 1 到 3 的路徑
    path = UndirectedGraph.path_to(node_from, 1, 3)
    assert path == [1, 2, 3]
    
    with pytest.raises(ValueError, match="Unreachable"):
        UndirectedGraph.path_to(node_from, 1, 99)


class TestUndirectedGraphCoverage:
    def test_repr_and_basic_logic(self, empty_graph):
        # __repr__
        empty_graph.add_node(1)
        empty_graph.add_node(2)
        empty_graph.add_edge(1, 2)
        assert "1: [2]" in str(empty_graph)
        
        # has_node False 分支
        assert empty_graph.has_node(999) is False
        
        # add_node 重複新增
        assert empty_graph.add_node(1) is False

    def test_edge_ops_failures(self, empty_graph):
        empty_graph.add_node(1)
        empty_graph.add_node(2)
        
        # add_edge 節點不存在
        assert empty_graph.add_edge(1, 99) is False
        
        # remove_edge 失敗路徑 (node 不存在、edge 不存在)
        assert empty_graph.remove_edge(1, 99) is False
        assert empty_graph.remove_edge(1, 2) is False

    def test_bipartite_disconnected(self):
        """觸發 get_bipartite 中處理多個連通元件的分支"""
        g = UndirectedGraph()
        # 元件 1
        g.add_node(1); g.add_node(2); g.add_edge(1, 2)
        # 元件 2
        g.add_node(3); g.add_node(4); g.add_edge(3, 4)
        
        color_map = g.get_bipartite()
        assert len(color_map) == 4
        assert color_map[1] != color_map[2]
        assert color_map[3] != color_map[4]
