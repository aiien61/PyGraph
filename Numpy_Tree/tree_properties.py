import numpy as np

def is_full(tree: np.ndarray) -> bool:
    """
    Each node must have no child node or two child nodes
    """
    n: int = len(tree)
    for i in range(n):
        if np.isnan(tree[i]):
            continue

        left: int = i * 2 + 1
        right: int = i * 2 + 2

        has_left: bool = left < n and not np.isnan(tree[left])
        has_right: bool = right < n and not np.isnan(tree[right])

        if has_left != has_right:
            return False
    return True

def is_perfect(tree: np.ndarray) -> bool:
    """
    Each leaf must at the same level
    """
    n: int = len(tree)
    if n == 0:
        return True
    
    is_power_of_2_minus_1: bool = (n & (n + 1)) == 0
    return is_power_of_2_minus_1 and all(not np.isnan(x) for x in tree)

def is_complete(tree: np.ndarray) -> bool:
    """
    No gap (i.e. null) between nodes
    """
    n: int = len(tree)
    found_none: bool = False
    for i in range(n):
        if np.isnan(tree[i]):
            found_none = True
        elif found_none:
            return False
    return True

def has_single_parent(tree: np.ndarray) -> bool:
    """
    Whether any single parent has only left or right child.
    """
    n: int = len(tree)
    for i in range(n):
        if np.isnan(tree[i]):
            continue

        left: int = i * 2 + 1
        right: int = i * 2 + 2

        has_left: bool = left < n and not np.isnan(tree[left])
        has_right: bool = right < n and not np.isnan(tree[right])

        if (has_left and not has_right) or (has_right and not has_left):
            return True
    return False