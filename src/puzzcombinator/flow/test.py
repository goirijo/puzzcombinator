import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt

G = nx.DiGraph()
edges = [
    ("Start", "Level 1"),
    ("Level 1", "Branch A1"),
    ("Level 1", "Branch B1"),
    ("Branch A1", "Branch A2"),
    ("Branch B1", "Branch B2"),
    ("Branch B2", "Branch B3"),
    ("Branch A2", "Merge"),
    ("Branch B3", "Merge"),
    ("Merge", "End")
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

