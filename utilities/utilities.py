import networkx as nx
from networkx import spring_layout

# define constants

init_red_balls = 57
init_black_balls = 43
init_split = (init_red_balls + init_black_balls)/2

time_steps = 10
number_of_nodes = 5
spread_rate = 10
memory = 5

# Generate new network
def generate_barabassi_graph(n):
    return nx.extended_barabasi_albert_graph(n, 1, 0, 0)