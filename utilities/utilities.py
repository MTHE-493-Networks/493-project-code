import networkx as nx
from matplotlib.pyplot import figure, draw, show, savefig, cm, colorbar, Normalize, rcParams, clf
from networkx import draw_networkx_nodes, draw_networkx_edges, kamada_kawai_layout
from numpy import min, max
from math import floor

# define constants
init_red_balls = 1
init_black_balls = 1
init_split = (init_red_balls + init_black_balls)/2
spread_rate = 10
time_steps = 200
number_of_nodes = 100
memory = 5


# Generate new network
def generate_barabassi_graph(n):
    return nx.extended_barabasi_albert_graph(n, 2, 0, 0)

  
    

'''
def delta_b(node):
    total_black = node.total_black
    for i in node.neighbours:
        total_black += i.total_black

    # db = floor((total_black/init_split) / (len(node.neighbours)+1))
    db = floor(total_black / (len(node.neighbours) + 1))

    if db == 0:
        db = 1

    return db

def delta_r(node):
    total_red = node.total_red
    for i in node.neighbours:
        total_red += i.total_red

    # dr = floor(((total_red + spread_rate)/init_split) / (len(node.neighbours)+1))
    dr = floor(total_red/(len(node.neighbours)+1))

    if dr == 0:
        dr = 1

    return dr
'''
