import networkx as nx
import matplotlib.pyplot as plt
from range_tree import Range_tree as rt


def draw_range_tree(root):
    G = nx.DiGraph()

    def add_nodes_edges(node, parent=None):
        if node is not None:
            G.add_node(node)
            if parent is not None:
                G.add_edge(parent, node)
            add_nodes_edges(node.left, node)
            add_nodes_edges(node.right, node)

    add_nodes_edges(root)
    pos = nx.drawing.spring_layout(G)
    nx.draw(G, pos, with_labels=True, arrows=False)
    plt.show()


tree = rt.build_range_tree()
draw_range_tree(tree.root)
