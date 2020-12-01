import random

# define the class that describes each urn
class polya_node:
    def __init__(self, red, black, _id):
        self.init_red = red
        self.init_black = black

        self.total_red = red
        self.total_black = black

        self.neighbours = []  # list of neighbours
        self.degree = 0  # number of neighbours

        self.id = _id

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
