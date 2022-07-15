import joblib as jl
import os
import re
from matplotlib import pyplot as plt
import networkx as nx

def plotting(result1, count):
	

	# X-axis values
	x = list()
	for it in result1.keys():  	
		x.append(it)
#	print (len(x))
	# Y-axis values
	y = result1.values()
#	print (len(y))	
#	Create legend
	for it2 in result1.keys():  
		labels = "node-"+str(it2) 	
	
	#Create axis labels
	plt.xlabel("Betweenness")
	plt.ylabel("Sum of Weights")
	# Function to bar
	plt.bar(x,y, label = labels)
	plt.title("Betweenness values vs sum of weights")
	plt.legend()
	# function to show the bar			
	plt.savefig('plot_'+str(count)+'.png', dpi=300)


if __name__=="__main__":
	
#	avg_clustering = {}
#	num_nodes = {}
#	num_edges = {}
#	omega = {}
#	node_edge_ratio = {}


	directory1 = "./results"	
	count1 = 0
	for filename1 in os.listdir(directory1):		
		if filename1[0:5] == "Omega":
			count1 += 1
	print (count1)
	
	directory1 = "./files/Nodes/Graphs/subgraphs"	
	count = 0
	for filename1 in os.listdir(directory1):		
		if filename1[0:5] != "Graph":
			continue
		if count < count1:
			count += 1
			print ("Skipping: ", filename1)
			continue			
		print ("Loading graph: ", filename1)
		filename = os.path.join(directory1, filename1)			
		new_file = open(filename, "rb")
		G = jl.load(new_file)
		new_file.close()
		
#		num_nodes[count] = len(G.nodes())
#		num_edges[count] = len(G.edges())
		avg_clustering = nx.average_clustering(G)
		node_edge_ratio = len(G.nodes())/len(G.edges())

		print("Saving average clustering value of the subgraph")
		filename = "./results/AvgClustering_"+str(count)+".pkl"
		new_file = open(filename, "wb")
		jl.dump(avg_clustering, new_file)
		new_file.close()
		print("Saving the node edge ratio of the subgraph")
		filename = "./results/NodeEdgeRatio_"+str(count)+".pkl"
		new_file = open(filename, "wb")
		jl.dump(node_edge_ratio, new_file)
		new_file.close()		

		count += 1
		
	directory1 = "./files/Nodes/Graphs"
	filename = os.path.join(directory1, "Graph.pkl")				
	print ("Loading main graph: ", filename)
	new_file = open(filename, "rb")
	G = jl.load(new_file)
	new_file.close()
	
	node_edge_ratio = len(G.nodes())/len(G.edges())			
	print("Saving the node edge ratio of the main graph")
	filename = "./results/NodeEdgeRatioMain.pkl"
	new_file = open(filename, "wb")
	jl.dump(node_edge_ratio, new_file)
	new_file.close()
		
#	print (node_edge_ratio)
#	print (avg_clustering)
#	print (omega)
#	plotting (avg_clustering, 3)
#	plotting (node_edge_ratio, 4)	
#	plotting (num_nodes, 5)
#	plotting (num_edges, 6)	
	
