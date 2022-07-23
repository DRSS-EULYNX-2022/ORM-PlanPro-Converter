from dataclasses import dataclass
from overpy import Node
from typing import Tuple

from utils import dist_edge, dist_nodes

@dataclass
class BoundingBox:
    x1: float
    y1: float
    x2: float
    y2: float

    def __repr__(self):
        x1,x2 = min(self.x1,self.x2), max(self.x1,self.x2)
        y1,y2 = min(self.y1,self.y2), max(self.y1,self.y2)
        return f'{x1},{y1},{x2},{y2}'

@dataclass
class Signal:
    node: Node
    edge: Tuple[Node, Node]
    function: str = "andere"
    kind: str = "andere"

    def __str__(self) -> str:
        node_before, node_after = self.edge
        distance_side = dist_edge(node_before, node_after, self.node)
        distance_node_before = dist_nodes(node_before, self.node)
        # ToDo extend arnes planpro generator to take dist_side as input, only then pos of signal is unambigous
        signal_str = f"signal {node_before.id} {node_after.id} {distance_node_before} {self.function} {self.kind}\n"
        return signal_str