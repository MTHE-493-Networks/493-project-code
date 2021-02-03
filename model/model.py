import random
from numpy import empty
from utilities.utilities import generate_barabassi_graph, init_black_balls, init_red_balls, memory
# from utilities.utilities import delta_r, delta_b
from model.node import polya_node
from typing import List
import networkx as nx

class network:
    nodes: List[polya_node]

    def __init__(self, version):
        version = version.lower()

        self.steps = 0          # Polya step counter
        self.current = 0        # Iteration index
        
        self.Z = []     # Matrix of Z(i,n) (ie. R or B) for last m draws
        self.draw_data = []   # num balls added for each urn over last m draws
        
        self.network_plot = nx.Graph()  # init empty graph
        self.nodes = []     # empty array of nodes - initialized in generate_network()
        self.generate_network(version)     # Generate network




    # Function to generate network
    def generate_network(self, version):
        # mapping = {}
        if version == "new":
            n = 0              # Number of nodes
            # self.nodes = empty(n, dtype=polya_node) 
            
        elif version == "b":
            n = 100              # Number of nodes
            # self.nodes = empty(n, dtype=polya_node)
            # curr = 0  # tracker of current node index
            
            for i in range(0,12):  # pink beds 0-11
                self.add_node("mid", i)
            for i in range(12,20):  # yellow beds 12-19
                self.add_node("hi", i)
            for i in range(20,72):  # blue beds 20-71
                self.add_node("mid", i)
            for i in range(72,100):  # staff 72-99 {pink(6) 72-77, yellow(4) 78-81, blue(18) 82-99}
                self.add_node("mid", i)
            self.network_plot.add_nodes_from(self.nodes)
            
            # edges
            for i in range(3):  # pink connections
                # b/t roommates
                self.network_plot.add_edge(self.nodes[2*i],self.nodes[(2*i)+1])
                self.network_plot.add_edge(self.nodes[(2*i)+6],self.nodes[(2*i)+7])
                # b/t nurses and roommates
                self.network_plot.add_edge(self.nodes[2*i],self.nodes[i+72])
                self.network_plot.add_edge(self.nodes[(2*i)+6],self.nodes[i+72+3])
                
            # yellow connections to nurses
            self.network_plot.add_edge(self.nodes[78],self.nodes[12])
            self.network_plot.add_edge(self.nodes[78],self.nodes[13])
            self.network_plot.add_edge(self.nodes[79],self.nodes[14])
            self.network_plot.add_edge(self.nodes[79],self.nodes[15])
            self.network_plot.add_edge(self.nodes[80],self.nodes[16])
            self.network_plot.add_edge(self.nodes[80],self.nodes[17])
            self.network_plot.add_edge(self.nodes[81],self.nodes[18])
            self.network_plot.add_edge(self.nodes[81],self.nodes[19])
            
            for i in range(8):  # blue triple room connections
                # between roommates
                self.network_plot.add_edge(self.nodes[(3*i)+20],self.nodes[(3*i)+21])
                self.network_plot.add_edge(self.nodes[(3*i)+20],self.nodes[(3*i)+22])
                self.network_plot.add_edge(self.nodes[(3*i)+21],self.nodes[(3*i)+22])
                self.network_plot.add_edge(self.nodes[(3*i)+20+26],self.nodes[(3*i)+21+26])
                self.network_plot.add_edge(self.nodes[(3*i)+20+26],self.nodes[(3*i)+22+26])
                self.network_plot.add_edge(self.nodes[(3*i)+21+26],self.nodes[(3*i)+22+26])
                # between nurse and roommates
                self.network_plot.add_edge(self.nodes[(3*i)+20],self.nodes[i+82])
                self.network_plot.add_edge(self.nodes[(3*i)+21],self.nodes[i+82])
                self.network_plot.add_edge(self.nodes[(3*i)+22],self.nodes[i+82])
                self.network_plot.add_edge(self.nodes[(3*i)+20+26],self.nodes[i+82+9])
                self.network_plot.add_edge(self.nodes[(3*i)+21+26],self.nodes[i+82+9])
                self.network_plot.add_edge(self.nodes[(3*i)+22+26],self.nodes[i+82+9])
                
            # double room roommate connections
            self.network_plot.add_edge(self.nodes[44],self.nodes[45])
            self.network_plot.add_edge(self.nodes[44+26],self.nodes[45+26])
            # nurse connections
            self.network_plot.add_edge(self.nodes[44],self.nodes[82+8])
            self.network_plot.add_edge(self.nodes[45],self.nodes[82+8])
            self.network_plot.add_edge(self.nodes[44+26],self.nodes[99])
            self.network_plot.add_edge(self.nodes[45+26],self.nodes[99])

            for i in [72,73,74,78,79]:  # pink/yellow staff connections (floor 1)
                for j in [72,73,74,78,79]:
                    if(i!=j):
                        self.network_plot.add_edge(self.nodes[i],self.nodes[j])
                        self.network_plot.add_edge(self.nodes[i+12],self.nodes[j+12]) 
                        
            for i in [75,76,77,80,81]:  # pink/yellow staff connections (floor 2)
                for j in [75,76,77,80,81]:
                    if(i!=j):
                        self.network_plot.add_edge(self.nodes[i],self.nodes[j])
                        self.network_plot.add_edge(self.nodes[i+12],self.nodes[j+12]) 
            
            for i in range(82,86):  # blue staff connections(floor 1.1)
                for j in range(82,86):
                    if(i!=j):
                        self.network_plot.add_edge(self.nodes[i],self.nodes[j])
                        
            for i in range(87,90):  # blue staff connections(floor 1.2)
                for j in range(87,90):
                    if(i!=j):
                        self.network_plot.add_edge(self.nodes[i],self.nodes[j])
                        
            for i in range(91, 95):  # blue staff connections(floor 2.1)
                for j in range(91, 95):
                    if(i!=j):
                        self.network_plot.add_edge(self.nodes[i],self.nodes[j])

            for i in range(96, 99):  # blue staff connections(floor 2.2)
                for j in range(96, 99):
                    if(i!=j):
                        self.network_plot.add_edge(self.nodes[i],self.nodes[j])
                        
        elif version == "c":
            n = 102            # Number of nodes
            # self.nodes = empty(n, dtype=polya_node) 
            
            
#        else:
        for node in self.nodes:  # map neighbours to nodes
            node.neighbours = self.network_plot[node]
            
        self.Z = [[] for _ in range(n)]     # Matrix of Z(i,n) (ie. R or B) for last m draws
        self.draw_data = [[] for _ in range(n)]    # num balls added for each urn over
        for i in range(n):          # initialize Z 
            for j in range(memory):
                self.Z[i].append(-1)
        for i in range(n):          # initialize draw_data
            for j in range(memory):
                self.draw_data[i].append(-1) 
                
        self.update_deltas()
        
            # for i, ind in enumerate(self.network_plot):    # Generate nodes
            #     if random.random() <= 1:
            #         new_node = polya_node(init_red_balls, init_black_balls, ind)
            #     else:
            #         new_node = polya_node(init_black_balls, init_red_balls, ind)
            #     mapping[i] = new_node
            #     self.nodes[ind] = new_node
    
            # for i, node in enumerate(self.nodes):   # Add neighbours to nodes
            #     neighbour_indexes = [ind for ind in self.network_plot.neighbors(i)]
            #     self.nodes[i].add_neighbours([self.nodes[ind] for ind in neighbour_indexes])
    

    
    def add_node(self, risk, _id):
        new_node = polya_node(risk, _id)
        self.nodes.append(new_node)
        
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
