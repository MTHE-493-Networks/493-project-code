import networkx as nx
from matplotlib.pyplot import figure, draw, show, savefig, cm, colorbar, Normalize, rcParams, clf
from networkx import draw_networkx_nodes, draw_networkx_edges, kamada_kawai_layout
from numpy import min, max
from math import floor

# define constants
init_red_balls = 57
init_black_balls = 43
init_split = (init_red_balls + init_black_balls)/2
spread_rate = 10
time_steps = 200
number_of_nodes = 20
memory = 5


# Generate new network
def generate_barabassi_graph(n):
    return nx.extended_barabasi_albert_graph(n, 2, 0, 0)


def draw_graph(G, step):
    G = G.network_plot

    color_lookup = {k: k.red_proportion() for k in set(G.nodes())}

    fig = figure(figsize=(8, 6))
    rcParams.update({'font.size': 16, 'mathtext.default': 'regular'})
    ax = fig.gca()
    ax.axis('off')  # Disable axis

    graph = G
    plot_layout = kamada_kawai_layout(graph)
    cmap = cm.get_cmap('coolwarm')

    weights = color_lookup.values()
    sizes = [50 if weight <= .6 else 100 for weight in weights]
    node_colors = [0 if weight <= .6 else 1 for weight in list(weights)]
    if all(node_colors):
        node_colors = 'r'
    # min_val, max_val = min(weights), max(weights)

    draw_networkx_edges(graph, plot_layout, alpha=0.05)
    draw_networkx_nodes(graph, plot_layout, node_size=sizes, linewidths=.5, edgecolors='k', node_color=node_colors,
                        cmap=cmap)

    savefig("graphs/Graph" + str(step) + ".png", format="PNG")
    clf()


def delta_b(node):
    total_black = node.total_black
    for i in node.neighbours:
        total_black += i.total_black

    db = floor((total_black/init_split) / (len(node.neighbours)+1))

    if db == 0:
        db = 1

    return db


def delta_r(node):
    total_red = node.total_red
    for i in node.neighbours:
        total_red += i.total_red

    db = floor(((total_red + spread_rate)/init_split) / (len(node.neighbours)+1))

    if db == 0:
        db = 1

    return db
