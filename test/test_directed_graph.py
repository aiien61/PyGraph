import pytest
from NumPy_Graph.directed_graph import DirectedGRaph

# -------------------------
# Fixtures
# -------------------------

@pytest.fixture
def empty_graph() -> DirectedGRaph:
    return DirectedGRaph()

@pytest.fixture
def simple_graph() -> DirectedGRaph:
    """
    1 -> 2 -> 3
    """
    g = DirectedGRaph()
    for i in [1, 2, 3]:
        g.add_node(i)
    
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    return g

@pytest.fixture
def cyclic_graph() -> DirectedGRaph:
    """
    1 -> 2 -> 3 -> 1
    """
    g = DirectedGRaph()
    for i in [1, 2, 3]:
        g.add_node(i)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 1)
    return g

@pytest.fixture
def multi_scc_graph():
    """
    SCC1: {1, 2}
    SCC2: {3}
    SCC3: {4, 5}

    1 ↔ 2
    3 alone
    4 ↔ 5
    """
    g = DirectedGRaph()
    for i in [1, 2, 3, 4, 5]:
        g.add_node(i)
    
    g.add_edge(1, 2)
    g.add_edge(2, 1)

    g.add_edge(4, 5)
    g.add_edge(5, 4)

    return g

# -------------------------
# Basic Node / Edge Tests
# -------------------------

def test_add_node(empty_graph):
    assert empty_graph.add_node(1) is True
    assert empty_graph.add_node(1) is False
    assert empty_graph.has_node(1) is True


def test_add_edge(simple_graph):
    assert simple_graph.add_edge(1, 3) is True
    assert simple_graph.add_edge(1, 3) is False
    assert simple_graph.add_edge(1, 99) is False


def test_remove_edge(simple_graph):
    assert simple_graph.remove_edge(1, 2) is True
    assert simple_graph.remove_edge(1, 2) is False

def test_remove_node_lock_behavior(simple_graph):
    simple_graph.lock()
    assert simple_graph.remove_node(2) is False
    simple_graph.unlock()
    assert simple_graph.remove_node(2) is True

# -------------------------
# BFS / DFS Tests
# -------------------------

def test_bfs(simple_graph):
    visited = simple_graph._bfs(1, simple_graph.adj_list)
    assert visited == {1, 2, 3}

def test_dfs(simple_graph):
    visited = simple_graph._dfs(1, simple_graph.adj_list)
    assert visited == {1, 2, 3}

# -------------------------
# Mutual Reachability
# -------------------------

def test_mutual_reachability_true(cyclic_graph):
    assert cyclic_graph.is_mutually_reachable_bfs(1, 3) is True
    assert cyclic_graph.is_mutually_reachable_dfs(1, 3) is True


def test_mutual_reachability_false(simple_graph):
    assert simple_graph.is_mutually_reachable_bfs(1, 3) is False
    assert simple_graph.is_mutually_reachable_dfs(1, 3) is False

# -------------------------
# Strongly Connected
# -------------------------

def test_is_strongly_connected_true(cyclic_graph):
    assert cyclic_graph.is_strongly_connected() is True


def test_is_strongly_connected_false(simple_graph):
    assert simple_graph.is_strongly_connected() is False

# -------------------------
# SCC - Kosaraju
# -------------------------

def test_kosaraju_single_cycle(cyclic_graph):
    scc = cyclic_graph.find_all_strongly_connected_components_kosaraju()
    assert len(scc) == 1
    assert scc[0] == {1, 2, 3}

def test_kosaraju_multi_scc(multi_scc_graph):
    scc = multi_scc_graph.find_all_strongly_connected_components_kosaraju()
    expected = [{1, 2}, {3}, {4, 5}]
    assert {frozenset(s) for s in scc} == {frozenset(s) for s in expected}

# -------------------------
# SCC - Tarjan
# -------------------------

def test_tarjan_single_cycle(cyclic_graph):
    scc = cyclic_graph.find_all_strongly_connected_components_tarjan()
    assert len(scc) == 1
    assert scc[0] == {1, 2, 3}

def test_tarjan_multi_scc(multi_scc_graph):
    scc = multi_scc_graph.find_all_strongly_connected_components_tarjan()
    expected = [{1, 2}, {3}, {4, 5}]
    assert {frozenset(s) for s in scc} == {frozenset(s) for s in expected}

# -------------------------
# Consistency Check
# -------------------------

def test_tarjan_vs_kosaraju_consistency(multi_scc_graph):
    kosaraju = multi_scc_graph.find_all_strongly_connected_components_kosaraju()
    tarjan = multi_scc_graph.find_all_strongly_connected_components_tarjan()

    kosaraju_sets = [set(s) for s in kosaraju]
    tarjan_sets = [set(s) for s in tarjan]

    assert len(kosaraju_sets) == len(tarjan_sets)
    assert {frozenset(s) for s in kosaraju_sets} == {frozenset(s) for s in tarjan_sets}

# -------------------------
# Cycle Detection Tests
# -------------------------

@pytest.mark.parametrize("method_name", [
    "has_cycle_by_dfs",
    "has_cycle_by_three_colors",
    "has_cycle_by_kahn"
])
class TestCycleDetection:
    """測試三種不同的環偵測演算法"""

    def test_no_cycle(self, simple_graph, method_name):
        # 1 -> 2 -> 3 (無環)
        method = getattr(simple_graph, method_name)
        assert method() is False

    def test_has_cycle_simple(self, cyclic_graph, method_name):
        # 1 -> 2 -> 3 -> 1 (有環)
        method = getattr(cyclic_graph, method_name)
        assert method() is True

    def test_empty_graph(self, empty_graph, method_name):
        # 空圖不應該有環
        method = getattr(empty_graph, method_name)
        assert method() is False

    def test_self_loop(self, empty_graph, method_name):
        # 自環測試: 1 -> 1
        empty_graph.add_node(1)
        empty_graph.add_edge(1, 1)
        method = getattr(empty_graph, method_name)
        assert method() is True

    def test_disconnected_cycles(self, method_name):
        """
        測試多個連通元件中，其中一個有環的情況
        Graph: 1->2, 3->4->5->3
        """
        g = DirectedGRaph()
        for i in range(1, 6):
            g.add_node(i)
        
        # 組件 1: 無環
        g.add_edge(1, 2)
        # 組件 2: 有環
        g.add_edge(3, 4)
        g.add_edge(4, 5)
        g.add_edge(5, 3)
        
        method = getattr(g, method_name)
        assert method() is True

    def test_complex_dag(self, method_name):
        """
        測試複雜的有向無環圖 (DAG)
        1 -> 2 -> 4
        1 -> 3 -> 4
        """
        g = DirectedGRaph()
        for i in range(1, 5):
            g.add_node(i)
        g.add_edge(1, 2)
        g.add_edge(1, 3)
        g.add_edge(2, 4)
        g.add_edge(3, 4)
        
        method = getattr(g, method_name)
        # 雖然有兩條路徑到 4，但這不是環
        assert method() is False


class TestDirectedGraphCoverage:
    def test_missing_error_paths(self, empty_graph):
        # add_edge 節點不存在
        assert empty_graph.add_edge(1, 2) is False
        
        # remove_edge 節點不存在
        assert empty_graph.remove_edge(1, 2) is False
        
        # remove_node 節點不存在
        assert empty_graph.remove_node(999) is False

    def test_scc_edge_cases(self, empty_graph):
        # is_strongly_connected 空圖應回傳 True
        assert empty_graph.is_strongly_connected() is True
        
        # get_strongly_connected_component 節點不存在
        assert empty_graph.get_strongly_connected_component(999) == set()

    def test_cycle_detection_edge_cases(self, simple_graph):
        # 增加對已標記節點但不在 stack 中的覆蓋
        # 這通常發生在多個連通元件的 DFS 遍歷
        simple_graph.add_node(10)
        simple_graph.add_node(11)
        simple_graph.add_edge(10, 11)
        assert simple_graph.has_cycle_by_dfs() is False