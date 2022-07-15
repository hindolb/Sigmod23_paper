import networkx as nx
import joblib as jl
import networkx.algorithms.components as comp
import os
import re

def find_subgraphs(filename, G): 
	S = [G.subgraph(c).copy() for c in nx.connected_components(G)]
	count = 0
	directory = "./files/Nodes/Graphs/subgraphs"
	for it1 in S:
		if len(it1.nodes) > 1:
			count += 1
			filename1 = re.sub(r'(./files/Nodes/Graphs/)',"./files/Nodes/Graphs/subgraphs/", filename)			
			filename1 = re.sub(r'(.pkl)','_'+str(count)+'.pkl', filename1)
#			filename = os.path.join(directory, filename)					
			print (filename1)
			print ("Saving the graph")			
			new_file = open(filename1, "wb")
			jl.dump(it1, new_file)
			new_file.close()
			del filename1
			


if __name__=="__main__":
	
	directory = "./files/Nodes/Graphs"
	for filename1 in os.listdir(directory):
		if filename1[-3:] != "pkl":
			continue					
		print ("Loading graph of node: ", filename1)
		filename = os.path.join(directory, filename1)					
		new_file = open(filename, "rb")
		g = jl.load(new_file)
		new_file.close()
#	print ("Loading weight of node: ", counter)
#	new_file = open("./files/Nodes/Weights/Weight_" +str(counter) +"_.pkl", "rb")
#	weight = jl.load(new_file)
#	new_file.close()

#	g= nx.Graph()
#	for it1 in weight.keys():
#		files = it1.split("_")
#		g.add_edge(files[0], files[1])

		print(nx.number_connected_components(g))
#	maxx = max(nx.connected_component_subgraphs(g), key=len)
#	print (maxx.nodes)
#	print (len(weight))
		find_subgraphs(filename, g)
