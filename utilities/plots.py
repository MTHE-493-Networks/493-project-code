import networkx as nx
import matplotlib as mpl
from matplotlib import pyplot as plt
from pylab import rcParams
from utilities import time_steps


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

    plt.savefig("graphs/network-images/Graph" + str(step) + ".png", format="PNG")
    plt.clf()

def plot_ave_red_proportion(red_prop_data):
    time = []
    average_red_prop = []  # average proportion of red balls over time
    for j in range(time_steps):
        average_red_prop.append(sum(red_prop_data[j])/len(red_prop_data[j]))
        time.append(j)
     
    plt.plot(time, average_red_prop)
    plt.xlabel('Step')
    plt.ylabel('Average proportion of red balls over all urns ')
    plt.show()
    
def plot_ave_infection_rate(superred_prop_data):
    time = []
    average_red_prop = []  # average proportion of red balls in superurn over time
    for j in range(time_steps):
        average_red_prop.append(sum(superred_prop_data[j])/len(superred_prop_data[j]))
        time.append(j)
    plt.plot(time, average_red_prop)
    plt.xlabel('Step')
    plt.ylabel('Average Infection Rate over time')
    plt.show()