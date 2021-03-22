import random
from numpy import min, max
from math import floor
from utilities.utilities import init_split, spread_rate

# define the class that describes each urn
class polya_node:
    def __init__(self, profile, _id):    
    # def __init__(self, red, black, _id):
        
        # define the type of individual
        # self.profile = profile   # to be given as an input instead of red/black?
        self.risk = profile
        
        # wait until network has been created to set deltas
        self.delta_r = 0
        self.delta_b = 0
        
        if self.risk == "mid":
            self.init_red = 10
            self.init_black = 10
        elif self.risk == "hi":
            self.init_red = 11
            self.init_black = 9
        elif self.risk == "lo":
            self.init_red = 9
            self.init_black = 11
        elif self.risk == "mid-ext":
            self.init_red = 10
            self.init_black = 10
            self.delta_r = 10
            self.delta_b = 10
        elif self.risk == "lo-ext":
            self.init_red = 9
            self.init_black = 11
            self.delta_r = 4
            self.delta_b = 6
        # elif self.profile == "hi traffic worker":
        #     self.init_red = 2
        #     self.init_black = 2
            
        # elif self.profile == "lo traffic worker":
        #     self.init_red = 1
        #     self.init_black = 4
        
        self.total_red = self.init_red
        self.total_black = self.init_black
        
        self.neighbours = []    # list of neighbours
        self.degree = 0         # number of neighbours
        self.alive = True        # is the urn to be drawn from?
        self.id = _id
        self.recovered = False
        self.daysInfected = 0


    def set_delta_b(self):
        if "ext" not in self.risk:
            total_black = self.total_black
            for i in self.neighbours:
                total_black += i.total_black
            try:
                db = floor(total_black/ len(self.neighbours))
            except:
                print("Urn with ID #" + str(self.id) + " has no neighbours")
            if db == 0:
                db = 1
            self.delta_b = db
    
    def set_delta_r(self):
        if "ext" not in self.risk:
            total_red = self.total_red
            for i in self.neighbours:
                total_red += i.total_red
    
            try:
                dr = floor(1.3*(total_red / (len(self.neighbours))))
            except:
                print("Urn with ID #" + str(self.id) + " has no neighbours")
            if dr == 0:
                dr = 1
            self.delta_r = dr

    def remove_init_balls(self):
        self.total_black -= self.init_black
        self.total_red -= self.init_red
        
    def red_proportion(self):
        return self.total_red / (self.total_red + self.total_black)
    
    def super_red_proportion(self):
        num_super_red = 0  # number of red balls in superurn
        num_super_total = 0  # number of balls in superurn
        for i in self.neighbours:
            num_super_red += i.total_red
            num_super_total += i.total_red + i.total_black
        return num_super_red / num_super_total

    def draw_ball(node):
        red_percent = node.red_proportion()
        roll = random.random()
        if roll > red_percent:
            node.total_black += 1
            drawn_ball = "black"
        else:
            node.total_red += 1
            drawn_ball = "red"
        return drawn_ball

    # Add neighbour to node
    def add_neighbour(self, neighbour):
        self.neighbours.append(neighbour)
        self.degree = len(self.neighbours)

    def add_neighbours(self, neighbours):
        self.neighbours = neighbours
        self.degree = len(self.neighbours)
    
    def set_patient_zero(self):
        self.init_red = 30
        self.init_black = 3
        self.total_red = self.init_red
        self.total_black = self.init_black
    
    def check_death(self):
        roll = random.random()
        if roll < 0.05:
            self.alive = False
            self.neighbours = []
            return True
        else:
            return False

    def reset_node(self):
        self.total_black = self.init_black
        self.total_black = self.init_red
        self.recovered = True
        
        
        
        
