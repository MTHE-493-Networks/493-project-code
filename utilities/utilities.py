import networkx as nx
from networkx import spring_layout
import matplotlib as mpl
from matplotlib import pyplot as plt
from pylab import rcParams

# define constants
red_balls_per_node = 50
black_balls_per_node = 50
delta_r = 2
delta_b = 1
time_steps = 100
number_of_nodes = 10

# Generate new network
def generate_barabassi_graph(n):
    return nx.extended_barabasi_albert_graph(n, 1, 0, 0)

def draw_graph(G, step):
    color_lookup = {k: k.total_red for k in G.nodes}

    low, *_, high = sorted(color_lookup.values())
    norm = mpl.colors.Normalize(vmin=low, vmax=high, clip=True)
    mapper = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.coolwarm)

    rcParams['figure.figsize'] = 12, 7

    nx.draw(G.network_plot,
            nodelist=color_lookup,
            node_size=1000,
            node_color=[mapper.to_rgba(i) for i in color_lookup.values()]
            )

    plt.savefig("graphs/Graph" + str(step) + ".png", format="PNG")
    plt.clf()