import networkx as nx
from networkx import spring_layout


# define constants
red_balls_per_node = 50
black_balls_per_node = 50
delta_r = 2
delta_b = 1
time_steps = 10
number_of_nodes = 5
memory = 5

# Generate new network
def generate_barabassi_graph(n):
    return nx.extended_barabasi_albert_graph(n, 1, 0, 0)