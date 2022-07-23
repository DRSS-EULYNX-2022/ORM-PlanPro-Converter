import numpy as np
from overpy import Node

def dist_nodes(n1, n2):
    # Calculate distance between two nodes
    p1 = np.array((n1.lat, n1.lon))
    p2 = np.array((n2.lat, n2.lon))
    return np.linalg.norm(p2-p1)

def dist_edge(node_before, node_after, signal):
    # Calculate distance from point(signal) to edge between node before and after
    p1 = np.array((node_before.lat, node_before.lon))
    p2 = np.array((node_after.lat, node_after.lon))
    p3 = np.array((signal.lat, signal.lon))
    return np.abs(np.cross(p2-p1, p1-p3)) / np.linalg.norm(p2-p1)

def is_end_node(node, graph):
    if is_signal(node):
        return False
    
    if graph.degree(node.id) == 1 or graph.degree(node.id) == 0:
        return True

def is_signal(node):
    return is_x(node, 'signal')

def is_switch(node):
    return is_x(node, 'switch')

def is_x(node, x: str):
    return 'railway' in node.tags.keys() and node.tags['railway'] == x

def is_same_edge(e1: tuple, e2: tuple):
    if e1 == e2:
        return True
    if e1[0] == e2[1] and e1[1] == e2[0]:
        return True
    return False

def get_signal_function(signal: Node) -> str:
    if not signal.tags['railway'] == 'signal':
        raise Exception('Expected signal node')
    try:
        tag = next(t for t in signal.tags.keys() if t.endswith(':function'))
        if signal.tags[tag] == 'entry':
            return 'Einfahr_Signal'
        elif signal.tags[tag] == 'exit':
            return 'Ausfahr_Signal'
        else:
            return 'andere'
    except StopIteration:
        return 'andere'

def get_signal_kind(signal: Node) -> str:
    if not signal.tags['railway'] == 'signal':
        raise Exception('Expected signal node')
    # TODO: Check the mapping of ORM tags to PlanPro signal kinds
    # ORM Reference: https://wiki.openstreetmap.org/wiki/OpenRailwayMap/Tagging/Signal
    # Supported kinds in Arne's generator: "Hauptsignal", "Mehrabschnittssignal", "Vorsignal", "Sperrsignal", "Hauptsperrsignal", "andere"
    if 'railway:signal:main' in signal.tags.keys():
        return 'Hauptsignal'
    elif 'railway:signal:minor' in signal.tags.keys():
        return 'Vorsignal'
    elif 'railway:signal:combined' in signal.tags.keys():
        return 'Mehrabschnittssignal'
    else:
        return 'andere'
