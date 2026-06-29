import networkx as nx
from .concepts import CONCEPTS

def build_concept_graph() -> nx.DiGraph:
    G = nx.DiGraph()
    for name, concept in CONCEPTS.items():
        G.add_node(name, description=concept.description)
        for req in concept.requires:
            G.add_edge(req, name)
    return G

def validate_ontology(graph: nx.DiGraph = None) -> bool:
    if graph is None:
        graph = build_concept_graph()
    try:
        cycles = list(nx.simple_cycles(graph))
        return len(cycles) == 0
    except nx.NetworkXNoCycle:
        return True
