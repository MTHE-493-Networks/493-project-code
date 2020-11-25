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
