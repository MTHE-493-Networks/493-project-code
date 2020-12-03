import random
from numpy import min, max
from math import floor
from utilities.utilities import init_split, spread_rate

# define the class that describes each urn
class polya_node:
    def __init__(self, red, black, _id):
        self.init_red = red
        self.init_black = black
        
        # self.delta_r = self.set_delta_r()
        # self.delta_b = self.set_delta_b()
        
        self.total_red = red
        self.total_black = black
        
        self.neighbours = []  # list of neighbours
        self.degree = 0  # number of neighbours
        
        self.id = _id


    # def set_delta_b(self):
    #     total_black = self.total_black
    #     for i in self.neighbours:
    #         total_black += i.total_black
    #     db = floor((total_black/init_split) / (len(self.neighbours)+1))
    #     if db == 0:
    #         db = 1
    #     self.delta_b = db
    #
    # def set_delta_r(self):
    #     total_red = self.total_red
    #     for i in self.neighbours:
    #         total_red += i.total_red
    #
    #     dr = floor(((total_red + spread_rate)/init_split) / (len(self.neighbours)+1))
    #
    #     if dr == 0:
    #         dr = 1
    #     self.delta_r = dr

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
