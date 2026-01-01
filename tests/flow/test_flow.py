import puzzcombinator as pz
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt
from puzzcombinator.flow import Edge, Node, Graph
import pytest
import re

def plot_graph():
    G = nx.DiGraph()
    edges = [
        ("Start", "Level 1"),
        ("Start", "Level 10"),
        #("Level 1", "Branch A1"),
        #("Level 1", "Branch B1"),
        #("Branch A1", "Branch A2"),
        #("Branch B1", "Branch B2"),
        #("Branch B2", "Branch B3"),
        #("Branch A2", "Merge"),
        #("Branch B3", "Merge"),
        #("Level 10", "Cranch D1"),
        #("Level 10", "Cranch C1"),
        #("Cranch D1", "Cranch D2"),
        #("Cranch C1", "Cranch C2"),
        #("Cranch C2", "Cranch C3"),
        #("Cranch D2", "Merge"),
        #("Cranch C3", "Merge"),
        ("Level 1", "PostMerge"),
        ("Level 1", "PostMerge"),
        ("Branch A1", "PostMerge"),
        ("Branch B1", "PostMerge"),
        ("Branch B2", "PostMerge"),
        ("Branch A2", "PostMerge"),
        ("Branch B3", "PostMerge"),
        ("Level 10", "PostMerge"),
        ("Level 10", "PostMerge"),
        ("Cranch D1", "PostMerge"),
        ("Cranch C1", "PostMerge"),
        ("Cranch C2", "PostMerge"),
        ("Cranch D2", "PostMerge"),
        ("Cranch C3", "PostMerge"),
        ("Merge", "End"),
        ("PostMerge", "End")
    ]
    G.add_edges_from(edges)

    # layout with left-to-right flow
    pos = graphviz_layout(G, prog="dot")  # no 'args' here

    # Draw using matplotlib
    nx.draw(
        G,
        pos,
        with_labels=True,
        arrows=True,
        node_size=2000,
        node_color="skyblue",
        node_shape='o',   # circle
        font_size=10
    )
    plt.show()

class StringContent(object):

    def __init__(self, value):
        self._value=value

    def to_file(self, filePath):
        print("Pretend I printed things to a file")
        print(value)

def test_bad_edge():
    content = "This is just some fake hint"
    with pytest.raises(TypeError, match="to_file"):
        edge = Edge(content)
            
def test_edge():
    content = StringContent("This is just some fake hint")
    edge = Edge(content)
            
def test_node():
    graph = Graph()

    ins = [StringContent("first"), StringContent("second"), StringContent("third")]
    outs = [StringContent("out"), StringContent("exit")]

    node = Node(ins, outs, graph)

    for e in node.incoming_edges:
        assert(e.target is not None)
        assert(e.source is None)

    for e in node.outgoing_edges:
        assert(e.target is None)
        assert(e.source is not None)

def generate_graph():
    """
    This is a minimal "treasure hunt" that goes
         S
      A1   B1
      A2   B2
      A3   B3
      AC   BC
         C
         E
    
    Start node splits into two unrelated directions. Then each branch is linear, with each node
    generating a piece that is finally combined into AC/BC. Then AC+BC is combined to C, and the end
    is reached.
    """
    graph = Graph()

    startA = StringContent("Group into team A")
    startB = StringContent("Group into team B")

    postCombo = StringContent("When ready, team up with other team")

    S = Node([], [startA, startB, postCombo], graph, label="S", memo="Intro to game")

    #---------

    FirstA = StringContent("First hint for A")
    Piece1A = StringContent("Piece 1/3 for A")
    A1 = Node([startA], [FirstA, Piece1A], graph, label="A1")

    FirstB = StringContent("First hint for B")
    Piece1B = StringContent("Piece 1/3 for B")
    B1 = Node([startB], [FirstB, Piece1B], graph, label="B1")

    #---------

    SecondA = StringContent("Second hint for A")
    Piece2A = StringContent("Piece 2/3 for A")
    A2 = Node([FirstA], [SecondA, Piece2A], graph, label="A2")

    SecondB = StringContent("Second hint for B")
    Piece2B = StringContent("Piece 2/3 for B")
    B2 = Node([FirstB], [SecondB, Piece2B], graph, label="B2")

    #---------

    ThirdA = StringContent("Put the pieces together A")
    Piece3A = StringContent("Piece 3/3 for A")
    A3 = Node([SecondA], [ThirdA, Piece3A], graph, label="A3")

    ThirdB = StringContent("Put the pieces together B")
    Piece3B = StringContent("Piece 3/3 for B")
    B3 = Node([SecondB], [ThirdB, Piece3B], graph, label="B3")

    #---------

    ComboA = StringContent("All A pieces together")
    AC = Node([Piece1A, Piece2A, Piece3A, ThirdA], [ComboA], graph, label="AC")

    ComboB = StringContent("All B pieces together")
    BC = Node([Piece1B, Piece2B, Piece3B, ThirdB], [ComboB], graph, label="BC")

    #---------

    doubleCombo = StringContent("We did it Joe")
    C = Node([ComboA, ComboB, postCombo], [doubleCombo], graph, label="C")

    E = Node([doubleCombo], [], graph, label="E")

    #---------

    return S

def chronological_order(start_node: Node):
    """
    Returns list of nodes in chronological order (topological sort).
    Advances to a node only when all incoming edges are visited.
    """
    visited = set()
    order = []
    ready = [start_node]

    while ready:
        node = ready.pop(0)
        if node in visited:
            continue
        visited.add(node)
        order.append(node)

        for edge in node.outgoing_edges:
            target = edge.target
            if all(e.source in visited for e in target.incoming_edges):
                ready.append(target)

    return order

def test_graph():
    S = generate_graph()

    print(S)
    print(S.outgoing_edges)

    ordered_nodes = chronological_order(S)
    print(ordered_nodes)

    for n in ordered_nodes:
        print(n.label)
    

def main():
    #plot_graph()
    #edge_test()
    S = generate_graph()
    ordered_nodes = chronological_order(S)

    edges_to_plot = []
    for node in ordered_nodes:
        for e in node.outgoing_edges:
            child = e.target
            if all(p.source in ordered_nodes[:ordered_nodes.index(child)] for p in child.incoming_edges):
                edges_to_plot.append((node.label, child.label))


    G = nx.DiGraph()
    edges = edges_to_plot

    for e in edges:
        print(e)

    G.add_edges_from(edges_to_plot)

    pos = nx.nx_agraph.graphviz_layout(G, prog="sfdp")
    nx.draw(G, pos, with_labels=True, arrows=True)
    plt.show()

if __name__=="__main__":
    main()
