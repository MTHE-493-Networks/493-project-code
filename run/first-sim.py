from utilities.utilities import time_steps, number_of_nodes
from model.model import network
from utilities.plots import draw_graph, plot_ave_red_proportion, plot_ave_infection_rate

red_prop_data = [[] for _ in range(time_steps)] # red proportion for each urn over time
super_red_prop_data = [[] for _ in range(time_steps)] # red proportion for each superurn over time
draw_data = [[] for _ in range(time_steps)]  # Z(i,n)

G_super = network(number_of_nodes)
# record initial data
for i in G_super.nodes:
    red_prop_data[0].append(i.red_proportion()) #n=0 initial red proportions
    super_red_prop_data[0].append(i.super_red_proportion)
    
# run model
for j in range(time_steps):
  G_super.supernode_run_step()
  # draw_graph(G_super, j)
  # record this step of data
  for i in G_super.nodes:
    red_prop_data[j].append(i.red_proportion())
    super_red_prop_data[j].append(i.super_red_proportion)
    # print("\n Red/black balls in " + str(i.id) + " urn: " + str(i.total_red) +"/"+ str(i.total_black))

# plot data
plot_ave_red_proportion(red_prop_data)
plot_ave_infection_rate(super_red_prop_data)