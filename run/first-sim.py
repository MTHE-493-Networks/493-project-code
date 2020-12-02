from utilities.utilities import time_steps, number_of_nodes, draw_graph
from model.model import network
import matplotlib.pyplot as plt

red_prop_data = [[] for _ in range(time_steps)] # empty matrix to contain red proportion for each node over time
average_red_prop = []  # to contain average proportion of red balls over time
G_super = network(number_of_nodes)

for i in G_super.nodes:
    red_prop_data[0].append(i.red_proportion())
    print("\n Red/black balls in " + str(i.id) + " urn: " + str(i.total_red) +"/"+ str(i.total_black))

for j in range(time_steps):
  G_super.supernode_run_step()
  if j % 10 == 0:
      draw_graph(G_super, j)
  for i in G_super.nodes:
    red_prop_data[j].append(i.red_proportion())

time = []
for j in range(time_steps):
  average_red_prop.append(sum(red_prop_data[j])/len(red_prop_data[j]))
  time.append(j)

for i in G_super.nodes:
    print("\n Red/black balls in " + str(i.id) + " urn: " + str(i.total_red) +"/"+ str(i.total_black))

x = time
# corresponding y axis values
y = average_red_prop

# plotting the points
plt.plot(x, y)

# naming the x axis
plt.xlabel('Step')
# naming the y axis
plt.ylabel('Average Proportion of Red Balls Over All Urns')

# function to show the plot
plt.show()

