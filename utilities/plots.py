import numpy as np
import networkx as nx
import matplotlib as mpl
from scipy.signal import savgol_filter
from matplotlib import pyplot as plt
from utilities.utilities import time_steps
from matplotlib.pyplot import figure, draw, show, savefig, cm, colorbar, Normalize, rcParams, clf
from networkx import draw_networkx_nodes, draw_networkx_edges, kamada_kawai_layout
from model.model import network


def draw_graph(G, step, l):
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
    sizes = [200 if weight <= .6 else 400 for weight in weights]
    node_colors = [0 if weight <= .6 else 1 for weight in list(weights)]
    if all(node_colors):
        node_colors = 'r'
    # min_val, max_val = min(weights), max(weights)

    draw_networkx_edges(graph, plot_layout,alpha=0.5, width=1)
    draw_networkx_nodes(graph, plot_layout, node_size=sizes, linewidths=.5, edgecolors='k', node_color=node_colors,
                        cmap=cmap)

    savefig("graphs/network-images/" + str(l) + "Graph" + str(step) + ".png", format="PNG")
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
    plt.savefig("graphs/Average proportion of red balls over time.PNG", format="PNG")
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
    plt.savefig("graphs/Average infection rate over time.PNG", format="PNG")
    plt.clf()

def total_infected_plot(G):
    time = range(time_steps)

    plt.plot(time, G.total_infected)
    plt.xlabel('Step')
    plt.ylabel('Number of Infected')
    plt.savefig("graphs/TotalNumInfected.PNG", format="PNG")
    plt.clf()
    
def total_deaths_plot(G):
    time = range(time_steps)

    plt.plot(time, G.total_deaths)
    plt.xlabel('Step')
    plt.ylabel('Total Deaths')
    plt.savefig("graphs/TotalDeaths.PNG", format="PNG")
    plt.clf()

def average_total_infected_plot(G):
    time = range(time_steps)

    yhat = savgol_filter(G.total_infected, 51, 3) # window size 51, polynomial order 3

    plt.plot(time, G.total_infected)
    plt.plot(time,yhat, color='red')
    plt.xlabel('Step')
    plt.ylabel('Number of Infected')
    plt.savefig("graphs/TotalNumInfected.PNG", format="PNG")
    plt.clf()


