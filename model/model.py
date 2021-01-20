import random
from numpy import empty
from utilities.utilities import generate_barabassi_graph, init_black_balls, init_red_balls, memory
# from utilities.utilities import delta_r, delta_b
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
        self.Z = [[] for _ in range(n)]     # Matrix of Z(i,n) (ie. R or B) for last m draws
        
        self.draw_data = [[] for _ in range(n)]    # num balls added for each urn over last m draws
        self.generate_network()     # Generate network
        for i in range(n):          # initialize Z 
            for j in range(memory):
                self.Z[i].append(-1)
        for i in range(n):          # initialize draw_data
            for j in range(memory):
                self.draw_data[i].append(-1) 



    # Function to generate network
    def generate_network(self):
        mapping = {}
        for i, ind in enumerate(self.network_plot):    # Generate nodes
            if random.random() <= 1:
                new_node = polya_node(init_red_balls, init_black_balls, ind)
            else:
                new_node = polya_node(init_black_balls, init_red_balls, ind)
            mapping[i] = new_node
            self.nodes[ind] = new_node

        for i, node in enumerate(self.nodes):   # Add neighbours to nodes
            neighbour_indexes = [ind for ind in self.network_plot.neighbors(i)]
            self.nodes[i].add_neighbours([self.nodes[ind] for ind in neighbour_indexes])

        self.network_plot = nx.relabel_nodes(self.network_plot, mapping)
        self.update_deltas()
        
    def update_deltas(self):
        for node in self.nodes:
            node.set_delta_r()
            node.set_delta_b()
            
    def add_draw_data(self, node, Z):
        # FIFO queue
        for j in range(memory-1):
            self.Z[node.id][memory-j-1] = self.Z[node.id][memory-j-2]
        self.Z[node.id][0] = Z
        
        for j in range(memory-1):
            self.draw_data[node.id][memory-j-1] = self.draw_data[node.id][memory-j-2]
        
        if Z == 0:   # black ball selected
            self.draw_data[node.id][0] = node.delta_b
        if Z == 1: 
            self.draw_data[node.id][0] = node.delta_r
        
    def recompute_urns(self):
        for node in self.nodes:
            total_red = node.init_red
            total_black = node.init_black
            for n in range(memory):
                if self.Z[node.id][n] == 0:
                    total_black += self.draw_data[node.id][n]
                elif self.Z[node.id][n] == 1:
                    total_red += self.draw_data[node.id][n]
            node.total_red = total_red
            node.total_black = total_black
        
    #draws a ball from every superurn in the network
    def supernode_run_step(self):
        for node in self.nodes:
            total_red = node.total_red
            total_black = node.total_black
            for i in node.neighbours:
                total_red += i.total_red
                total_black += i.total_black
            red_percent = total_red / (total_red + total_black)
            roll = random.random()
            if roll > red_percent:
                self.add_draw_data(node, 0)
            else:
                self.add_draw_data(node, 1)
        # end of drawing, time to re-compute graph
        self.recompute_urns()
        self.update_deltas()
