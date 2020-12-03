import networkx as nx
import matplotlib as mpl
from matplotlib import pyplot as plt
from utilities.utilities import time_steps
from matplotlib.pyplot import figure, draw, show, savefig, cm, colorbar, Normalize, rcParams, clf
from networkx import draw_networkx_nodes, draw_networkx_edges, kamada_kawai_layout



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

    savefig("graphs/network-images/Graph" + str(step) + ".png", format="PNG")
    clf()

def plot_ave_red_proportion(red_prop_data):
    time = []
    average_red_prop = []  # average proportion of red balls over time
    for j in range(time_steps):
        average_red_prop.append(sum(red_prop_data[j])/len(red_prop_data[j]))
        time.append(j)
     
    plt.plot(time, average_red_prop)
    plt.xlabel('Step')
    plt.ylabel('Average proportion of red balls in each urn')
    plt.savefig("graphs/Average proportion of red balls over time.png", format="PNG")
    plt.clf()
    
def plot_ave_infection_rate(superred_prop_data):
    time = []
    average_red_prop = []  # average proportion of red balls in superurn over time
    for j in range(time_steps):
        average_red_prop.append(sum(superred_prop_data[j])/len(superred_prop_data[j]))
        time.append(j)
    plt.plot(time, average_red_prop)
    plt.xlabel('Step')
    plt.ylabel('Average infection rate')
    plt.savefig("graphs/Average infection rate over time.png", format="PNG")
    plt.clf()