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
        
        self.total_infected = []
        self.total_deaths = []


    # Function to generate network
    def generate_network(self, version):
        # mapping = {}
        if version == "a":
            n = 105              # Number of nodes
            self.construct_network_a()
            
        elif version == "b":
            n = 105              # Number of nodes
            self.construct_network_b()

        elif version == "c":
            n = 106          # Number of nodes
            self.construct_network_c()
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
            if node.alive == True:
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
        infected = 0
        deaths = 0
        for node in self.nodes:
            if node.alive == False:
                deaths += 1
            else:
                total_red = node.init_red
                total_black = node.init_black
                for n in range(memory):
                    if self.Z[node.id][n] == 0:
                        total_black += self.draw_data[node.id][n]
                    elif self.Z[node.id][n] == 1:
                        total_red += self.draw_data[node.id][n]
                infection_percent = total_red / (total_red+total_black)
                if infection_percent >= 0.6:
                    death = node.check_death()
                    if death == False:
                        infected += 1   
                    else:
                        deaths += 1
                node.total_red = total_red
                node.total_black = total_black
        self.total_infected.append(infected)
        self.total_deaths.append(deaths)
        
        
    #draws a ball from every superurn in the network
    def supernode_run_step(self):
        self.steps += 1
        if self.steps == 10:
            for node in self.nodes:
                node.remove_init_balls()
        for node in self.nodes:
            if node.alive == True:
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
        





# Network Constructions a, b, and c
    
    def construct_network_a(self):
        for i in range(0, 32):  # Wing A beds
            self.add_node("mid", i)
        for i in range(32, 64):  # Wing B beds
            self.add_node("mid", i)
        for i in range(64,80):  # Room staff: 64-71 wing A, 72-79 wing B
            if (i%2 == 0):      # Even numbers regular, odd nursing students
                self.add_node("mid-ext", i)
            else:
                self.add_node("lo-ext", i)
        for i in range(80, 84):  # Dining staff
            self.add_node("lo-ext", i)
        self.nodes[64].set_patient_zero()
        # edges
        # all main workers-patron connections
        for j in range(0, 16):
            for i in range(4*j, 4*j + 4):
                self.network_plot.add_edge(self.nodes[i],self.nodes[64+j])
        # dining staff
        for i in range(0, 64):
            for j in range(80, 84):
                self.network_plot.add_edge(self.nodes[i],self.nodes[j])
        # semi-private connections
        self.network_plot.add_edge(self.nodes[36],self.nodes[37])
        self.network_plot.add_edge(self.nodes[42],self.nodes[43])
        self.network_plot.add_edge(self.nodes[46],self.nodes[47])
        self.network_plot.add_edge(self.nodes[50],self.nodes[51])
        self.network_plot.add_edge(self.nodes[54],self.nodes[55])     
        self.network_plot.add_edge(self.nodes[58],self.nodes[59])
        self.network_plot.add_edge(self.nodes[4],self.nodes[5])
        self.network_plot.add_edge(self.nodes[10],self.nodes[11])
        self.network_plot.add_edge(self.nodes[14],self.nodes[15])
        self.network_plot.add_edge(self.nodes[18],self.nodes[19])
        self.network_plot.add_edge(self.nodes[26],self.nodes[27])
        self.network_plot.add_edge(self.nodes[22],self.nodes[23])
        # connections between workers and wings
        for i in range(64, 79):
            self.network_plot.add_edge(self.nodes[i],self.nodes[i+1])
        # close the loops
        self.network_plot.add_edge(self.nodes[64],self.nodes[71])
        self.network_plot.add_edge(self.nodes[72],self.nodes[79])
        

        

    def construct_network_b(self):
        # Number of nodes
        # self.nodes = empty(n, dtype=polya_node)
        # curr = 0  # tracker of current node index
        
        for i in range(0,12):  # pink beds 0-11
            self.add_node("mid", i)
        for i in range(12,20):  # yellow beds 12-19
            self.add_node("hi", i)
        for i in range(20,72):  # blue beds 20-71
            self.add_node("mid", i)
        for i in range(72,100):  # staff 72-99 {pink(6) 72-77, yellow(4) 78-81, blue(18) 82-99}
            self.add_node("mid-ext", i)
        for i in range(100,105): # dining staff 100-104
            self.add_node("lo-ext", i)
        self.nodes[72].set_patient_zero() 
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
        
        #connections between groups of nurses/floors  
        self.network_plot.add_edge(self.nodes[74],self.nodes[82])  # pink/yellow to blue (floor 1)
        self.network_plot.add_edge(self.nodes[77],self.nodes[91])  # pink/yellow to blue (floor 2)
        self.network_plot.add_edge(self.nodes[86],self.nodes[87])  # b/t 2 groups of blue nurses
        self.network_plot.add_edge(self.nodes[95],self.nodes[96])  
        self.network_plot.add_edge(self.nodes[72],self.nodes[75]) # pink f1 to f2
        self.network_plot.add_edge(self.nodes[85],self.nodes[94]) # blue1 f1 to f2
        self.network_plot.add_edge(self.nodes[90],self.nodes[99]) # blue2 f1 to f2
        
        # connections between dining room staff
        for i in range(100,104):
            for j in range(i+1,105):
                self.network_plot.add_edge(self.nodes[i],self.nodes[j])

        # connections between dining room staff and residents
        for i in range(0,100):
            for j in range(100,105):
                self.network_plot.add_edge(self.nodes[i],self.nodes[j])
    #end construct_network_b()
    
    
    def construct_network_c(self):
        # nodes
        for i in range(0,4):  #0-3: unit C hi risk
            self.add_node("hi", i)
        for i in range(4,21):  #4-20: unit C normal
            self.add_node("mid", i)
        for i in range(21,25):  #21-24: unit B hi risk
            self.add_node("hi", i)
        for i in range(25,42):  #25-41: unit B normal
            self.add_node("mid", i)
        for i in range(42,82):  #42-81: unit A
            self.add_node("mid", i)
        for i in range(82,90):  #82-89: student/PSW
            self.add_node("lo-ext", i) #82-83 C, 84-85 B, 86-89 A
        for i in range(90,106): #90-105: workers
            self.add_node("mid-ext", i) #90-92 C, 93-95 B, 96-97 top din, 98-103 A, 104-105 bot din
        self.network_plot.add_nodes_from(self.nodes)
        self.nodes[90].set_patient_zero()
        # edges        
        # Unit C residents-workers
        for i in range(0,4): # 4 hi risk
            self.network_plot.add_edge(self.nodes[i],self.nodes[90])
        for i in range(4,13): # 4 middle rooms
            self.network_plot.add_edge(self.nodes[i],self.nodes[91])
        for i in range(13,21): # 3 southern rooms
            self.network_plot.add_edge(self.nodes[i],self.nodes[92])
        for i in range(0, 9): #PSW 1
            self.network_plot.add_edge(self.nodes[i],self.nodes[82])
        for i in range(9, 21): #PSW 2
            self.network_plot.add_edge(self.nodes[i],self.nodes[83])        
        # unit C roommates
        for i in range(5,8):
            for j in range(i+1,9):
                self.network_plot.add_edge(self.nodes[i],self.nodes[j])
        self.network_plot.add_edge(self.nodes[9],self.nodes[10])
        self.network_plot.add_edge(self.nodes[12],self.nodes[12])
        self.network_plot.add_edge(self.nodes[13],self.nodes[14])
        for i in range(15,17):
            for j in range(i+1,18):
                self.network_plot.add_edge(self.nodes[i],self.nodes[j])
        for i in range(18,20):
            for j in range(i+1,21):
                self.network_plot.add_edge(self.nodes[i],self.nodes[j])               
        # unit b residents-workers
        for i in range(21,25): # 4 hi risk
            self.network_plot.add_edge(self.nodes[i],self.nodes[93])
        for i in range(25,32): # 4 middle rooms
            self.network_plot.add_edge(self.nodes[i],self.nodes[94])
        for i in range(32,42): # 3 southern rooms
            self.network_plot.add_edge(self.nodes[i],self.nodes[95])
        for i in range(21, 28): #PSW 1
            self.network_plot.add_edge(self.nodes[i],self.nodes[84])
        for i in range(28, 42): #PSW 2
            self.network_plot.add_edge(self.nodes[i],self.nodes[85])         
        #unit b roommates
        self.network_plot.add_edge(self.nodes[26],self.nodes[27])
        self.network_plot.add_edge(self.nodes[28],self.nodes[29])
        self.network_plot.add_edge(self.nodes[30],self.nodes[31])
        self.network_plot.add_edge(self.nodes[32],self.nodes[33])        
        for i in range(34,37):
            for j in range(i+1,38):
                self.network_plot.add_edge(self.nodes[i],self.nodes[j])
        for i in range(39,42):
            for j in range(i+1,43):
                self.network_plot.add_edge(self.nodes[i],self.nodes[j])
        # unit a roommates
        self.network_plot.add_edge(self.nodes[44],self.nodes[45])
        self.network_plot.add_edge(self.nodes[51],self.nodes[50])
        for i in range(52,55):
            for j in range(i+1,56):
                self.network_plot.add_edge(self.nodes[i],self.nodes[j])
        for i in range(56,59):
            for j in range(i+1,60):
                self.network_plot.add_edge(self.nodes[i],self.nodes[j])
        for i in range(60,63):
            for j in range(i+1,64):
                self.network_plot.add_edge(self.nodes[i],self.nodes[j])
        self.network_plot.add_edge(self.nodes[64],self.nodes[65])
        for i in range(66,69):
            for j in range(i+1,70):
                self.network_plot.add_edge(self.nodes[i],self.nodes[j])
        for i in range(70,73):
            for j in range(i+1,74):
                self.network_plot.add_edge(self.nodes[i],self.nodes[j])
        for i in range(74,77):
            for j in range(i+1,78):
                self.network_plot.add_edge(self.nodes[i],self.nodes[j])
        for i in range(78,81):
            for j in range(i+1,82):
                self.network_plot.add_edge(self.nodes[i],self.nodes[j])
        # unit a residents-workers/PSW 42-81: unit A residents
        for i in range(42,46):
            self.network_plot.add_edge(self.nodes[i],self.nodes[98]) #worker
            self.network_plot.add_edge(self.nodes[i],self.nodes[86]) #PSW
        for i in range(46, 50):
            self.network_plot.add_edge(self.nodes[i],self.nodes[99])
            self.network_plot.add_edge(self.nodes[i],self.nodes[86])
        for i in range(50,64):
            self.network_plot.add_edge(self.nodes[i],self.nodes[100])
            self.network_plot.add_edge(self.nodes[i],self.nodes[87])
            self.network_plot.add_edge(self.nodes[i],self.nodes[101])
        for i in range(64,74):
            self.network_plot.add_edge(self.nodes[i],self.nodes[102])
            self.network_plot.add_edge(self.nodes[i],self.nodes[88])
        for i in range(74,82):
            self.network_plot.add_edge(self.nodes[i],self.nodes[103])
            self.network_plot.add_edge(self.nodes[i],self.nodes[89])
        # between workers, PSW
        # PSW: 82-83 C, 84-85 B, 86-89 A
        # workers: 90-92 C, 93-95 B, 96-97 top din, 98-103 A, 104-105 bot din
        self.network_plot.add_edge(self.nodes[90],self.nodes[82])
        self.network_plot.add_edge(self.nodes[91],self.nodes[82])
        self.network_plot.add_edge(self.nodes[91],self.nodes[83])
        self.network_plot.add_edge(self.nodes[92],self.nodes[83])
        self.network_plot.add_edge(self.nodes[93],self.nodes[84])
        self.network_plot.add_edge(self.nodes[94],self.nodes[84])
        self.network_plot.add_edge(self.nodes[94],self.nodes[85])
        self.network_plot.add_edge(self.nodes[95],self.nodes[85])
        self.network_plot.add_edge(self.nodes[96],self.nodes[97])
        self.network_plot.add_edge(self.nodes[98],self.nodes[86])
        self.network_plot.add_edge(self.nodes[99],self.nodes[86])
        self.network_plot.add_edge(self.nodes[99],self.nodes[87])
        self.network_plot.add_edge(self.nodes[100],self.nodes[87])
        self.network_plot.add_edge(self.nodes[100],self.nodes[101])
        self.network_plot.add_edge(self.nodes[102],self.nodes[88])
        self.network_plot.add_edge(self.nodes[103],self.nodes[88])
        self.network_plot.add_edge(self.nodes[103],self.nodes[89])
        # between dining staff and all residents
        for i in range(0,42):
            self.network_plot.add_edge(self.nodes[i],self.nodes[96])
            self.network_plot.add_edge(self.nodes[i],self.nodes[97])
        for i in range(42,82):
            self.network_plot.add_edge(self.nodes[i],self.nodes[104])
            self.network_plot.add_edge(self.nodes[i],self.nodes[105])
    #end construct_network_c