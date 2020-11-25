import networkx as nx

# define constants
red_balls_per_node = 90
black_balls_per_node = 10
delta_r = 1
delta_b = 1
time_steps = 1000
number_of_nodes = 10

# Generate new network
def generate_barabassi_graph(n):
    return nx.extended_barabasi_albert_graph(n, 1, 0, 0)

