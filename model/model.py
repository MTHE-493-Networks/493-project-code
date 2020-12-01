import random
from numpy import empty
from utilities.utilities import generate_barabassi_graph, red_balls_per_node, black_balls_per_node, delta_r, delta_b, memory
from model.node import polya_node
from typing import List
import networkx as nx

class network:
    nodes: List[polya_node]

    def __init__(self, n):
        self.network_plot = generate_barabassi_graph(n)
        self.nodes = empty(n, dtype=polya_node)     # Array of nodes

        self.n = n              # Number of nodes
        self.steps = 0          # Polya step counter
        self.current = 0        # Iteration index
        self.Z = [[] for _ in range(n)]     # Matrix containing Z(i,n) for last m draws
        for i in range(n):
            for j in range(memory):
                self.Z[i].append(-1) #initialize Z values to -1

        self.generate_network()     # Generate networ

    # Function to generate network
    def generate_network(self):
        mapping = {}
        for i, ind in enumerate(self.network_plot):    # Generate nodes
            new_node = polya_node(red_balls_per_node, black_balls_per_node, ind)
            mapping[i] = new_node
            self.nodes[ind] = new_node

        for i, node in enumerate(self.nodes):   # Add neighbours to nodes
            neighbour_indexes = [ind for ind in self.network_plot.neighbors(i)]
            self.nodes[i].add_neighbours([self.nodes[ind] for ind in neighbour_indexes])

        self.network_plot = nx.relabel_nodes(self.network_plot, mapping)

    def add_draw_data(self, node_index, Z):
        # FIFO queue
        for j in range(memory-1):
            self.Z[node_index][memory-j-1] = self.Z[node_index][memory-j-2]
        self.Z[node_index][0] = Z
        
    def recompute_urns(self):
        node_index = 0
        for node in self.nodes:
            node.total_red = node.init_red
            node.total_black = node.init_black
            for n in range(memory):
                node.total_red += delta_r * self.Z[node_index][n]
                node.total_black += delta_b * (1 - self.Z[node_index][n])
            node_index += 1
            
    #draws a ball from every superurn in the network
    def supernode_run_step(self):
        red_to_add = []
        black_to_add = []
        node_index = 0
        for node in self.nodes:
            total_red = node.total_red
            total_black = node.total_black
            for i in node.neighbours:
                total_red += i.total_red
                total_black += i.total_black
            red_percent = total_red / (total_red + total_black)
            roll = random.random()
            if roll > red_percent:
                black_to_add.append(node)
                self.add_draw_data(node_index, 0)
            else:
                red_to_add.append(node)
                self.add_draw_data(node_index, 1)
            node_index += 1
        # end of drawing, time to re-compute graph
        self.recompute_urns()