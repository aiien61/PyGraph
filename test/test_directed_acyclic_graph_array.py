import pytest
from NumPy_Graph.directed_acyclic_graph_array import DAG

# -------------------------
# Fixtures
# -------------------------

@pytest.fixture
def empty_dag():
    return DAG(N=5)

@pytest.fixture
def simple_dag():
    """
    0 -> 1 -> 3
    0 -> 2 -> 3
    """
    dag = DAG(N=4)
    dag.add_edge(0, 1)
    dag.add_edge(0, 2)
    dag.add_edge(1, 3)
    dag.add_edge(2, 3)
    return dag

# -------------------------
# Tests
# -------------------------

class TestDAGArrayBasic:
    def test_init(self, empty_dag):
        assert empty_dag.N == 5
        assert len(empty_dag.successors) == 5
        assert all(d == 0 for d in empty_dag.in_degree)
    
    def test_repr(self, simple_dag):
        # 測試 __repr__ 以確保 coverage
        rep = repr(simple_dag)
        assert "[[1, 2], [3], [3], []]" in rep
    
    def test_add_edge_bounds(self, empty_dag):
        # 測試索引越界
        assert empty_dag.add_edge(-1, 2) is False
        assert empty_dag.add_edge(0, 10) is False
        assert empty_dag.add_edge(0, 1) is True
    
    def test_lock_mechanism(self, empty_dag):
        empty_dag.lock()
        # 鎖定時無法新增或刪除
        assert empty_dag.add_edge(0, 1) is False
        assert empty_dag.in_degree[1] == 0
        
        empty_dag.unlock()
        assert empty_dag.add_edge(0, 1) is True
        assert empty_dag.in_degree[1] == 1

        empty_dag.lock()
        assert empty_dag.remove_edge(0, 1) is False
        assert empty_dag.in_degree[1] == 1
        
        empty_dag.unlock()
        assert empty_dag.remove_edge(0, 1) is True
        assert empty_dag.in_degree[1] == 0

    def test_remove_edge_failure(self, simple_dag):
        # 測試刪除不存在的邊
        assert simple_dag.remove_edge(0, 3) is False # 雖然節點存在但沒邊
        assert simple_dag.remove_edge(1, 0) is False # 方向相反

class TestTopologicalSort:
    def test_kahn_success(self, simple_dag):
        ordering = simple_dag.topological_sort()
        # 合法順序可以是 [0, 1, 2, 3] 或 [0, 2, 1, 3]
        assert ordering[0] == 0
        assert ordering[-1] == 3
        assert set(ordering) == {0, 1, 2, 3}

        # 驗證順序邏輯
        pos: dict[int, int] = {node: i for i, node in enumerate(ordering)}
        assert pos[0] < pos[1]
        assert pos[0] < pos[2]
        assert pos[1] < pos[3]
        assert pos[2] < pos[3]

    def test_cycle_detection(self):
        # 建立一個有環的圖 0 -> 1 -> 0
        dag = DAG(N=2)
        dag.add_edge(0, 1)
        dag.add_edge(1, 0)
        
        with pytest.raises(ValueError, match="Cycle detected"):
            dag.topological_sort()

    def test_disconnected_graph(self):
        # 測試不連通的圖 (0->1) 和 (2)
        dag = DAG(N=3)
        dag.add_edge(0, 1)
        ordering = dag.topological_sort()
        assert set(ordering) == {0, 1, 2}

