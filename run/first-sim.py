from utilities.utilities import time_steps, memory
from utilities.plots import draw_graph, plot_ave_infection_rate, plot_ave_red_proportion, total_infected_plot, average_total_infected_plot, total_deaths_plot
from model.model import network
import matplotlib.pyplot as plt

for k in range(1):
    red_prop_data = [[] for _ in range(time_steps + 1)] # red proportion for each urn over time
    super_red_prop_data = [[] for _ in range(time_steps + 1)] # red proportion for each superurn over time
    G_super = network("b")


    for i in G_super.nodes:
        # record initial infection rate data
        red_prop_data[0].append(i.red_proportion())
        super_red_prop_data[0].append(i.super_red_proportion())
        
        #print r/b balls in each urn initially
        #print("\n Red/black balls in " + str(i.id) + " urn: " + str(i.total_red) +"/"+ str(i.total_black))

    
    for j in range(time_steps):
        print("Urn " + str(G_super.nodes[0].id) + ". db: " + str(G_super.nodes[0].delta_b) + ", dr: " + str(G_super.nodes[0].delta_r) + "\n Red/black balls are " + str(G_super.nodes[0].total_red) +"/"+ str(G_super.nodes[0].total_black))
        
        if j % 5 == 0:
            draw_graph(G_super, j, k)
        
        G_super.supernode_run_step()
        for node in G_super.nodes:
            if node.alive == True:
                red_prop_data[j+1].append(node.red_proportion())
                super_red_prop_data[j+1].append(node.super_red_proportion())

        # time = []
        # average_red_prop = []
        
        # for j in range(time_steps):
            # average_red_prop.append(sum(red_prop_data[j])/len(red_prop_data[j]))
            # time.append(j)


    # x = range(time_steps)
    # corresponding y axis values
    # y = average_red_prop

    # plotting the points
    # plt.plot(x, y)

    # naming the x axis
    # plt.xlabel('Step')
    # naming the y axis
    # plt.ylabel('Average Proportion of Red Balls Over All Urns')

# plot data
# plot_ave_red_proportion(red_prop_data)
# plot_ave_infection_rate(super_red_prop_data)
total_infected_plot(G_super)
average_total_infected_plot(G_super)
total_deaths_plot(G_super)

print("Done")