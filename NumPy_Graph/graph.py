from abc import ABC, abstractmethod

class Graph(ABC):
    @abstractmethod
    def add_node(self, node: int): raise NotImplementedError

    @abstractmethod
    def add_edge(self): raise NotImplementedError

    @abstractmethod
    def remove_node(self, node: int): raise NotImplementedError

    @abstractmethod
    def remove_edge(self): raise NotImplementedError
