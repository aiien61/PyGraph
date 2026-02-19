from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Self, Optional
import numpy as np

@dataclass
class Node:
    value: Optional[int]
    left: Optional[Self] = None
    right: Optional[Self] = None

@dataclass
class BST(ABC):
    @abstractmethod
    def insert(self): raise NotImplementedError

@dataclass
class BST_List(BST):
    root: Optional[Node] = None

    def __str__(self):
        ...            

    def insert(self, value) -> bool:
        new_node: Node = Node(value)

        if not self.root:
            self.root = new_node
            return True
        
        temp = self.root
        while True:
            if value == temp.value:
                return False
            
            if value < temp.value:
                if not temp.left:
                    temp.left = new_node
                    return True
                temp = temp.left
            elif value > temp.right:
                if not temp.right:
                    temp.right = new_node
                    return True
                temp = temp.right
                



def main():
    BST_List()

if __name__ == "__main__":
    main()
