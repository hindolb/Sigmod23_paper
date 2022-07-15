import joblib as jl
import networkx as nx
import os
import re
import networkx.algorithms.components as comp
from networkx.algorithms import simple_paths as sp

if __name__ == "__main__":
    #Loading the graph
	with open("./files/Nodes/Graphs/TrainingFiles.pkl", 'rb') as fp:
		graph = jl.load(fp)
	fp.close()
	with open("./files/Nodes/Weights/TrainingFiles.pkl", 'rb') as fp:
		weight = jl.load(fp)
	fp.close()
	directory = "./files/results"
	
	print ("Merging and sorting the betweenness values")
	
	overall_betweenness = {}
	for filename1 in os.listdir(directory):	
		if filename1[17:22] == "Tuple":		
			with open(os.path.join(directory, filename1), 'rb') as fp:
				betweenness = jl.load(fp)
			fp.close()
			for it1 in betweenness.keys():
				values = betweenness[it1]
				if it1 in overall_betweenness.keys():
					values1 = overall_betweenness[it1]
					for it3 in values:
						values1.append(it3)
					overall_betweenness[it1] = values1	 
				else:
					overall_betweenness[it1] = values
	edges_coll = overall_betweenness[max(list(overall_betweenness.keys()))]
	del overall_betweenness[max(list(overall_betweenness.keys()))]
	edges_coll += overall_betweenness[max(list(overall_betweenness.keys()))]
	
	del betweenness
	del overall_betweenness
	nodes = []
	cumm_weight = 0
	for edge in edges_coll:
		cumm_weight += weight[edge]
	threshold = cumm_weight/len(edges_coll)
	print (threshold)
	new_graph = nx.Graph()
	for edge in graph.edges:
		if list(graph.get_edge_data(*edge).values())[0] < int(threshold):
			continue
		else:
			new_graph.add_edge(*edge)
			
		#partition the new graph
		counter = 1
	S = [new_graph.subgraph(c).copy() for c in nx.connected_components(new_graph)]
	for subgraphs in S:		
		#check for each partition:
		print ("Computing for subgraph: ", counter)
#		count = 0
#		print(len(list(graph.nodes)))
		sel_files = list(subgraphs.nodes)	

		with open("./TestingTasks.pkl", 'rb') as fp:
			test_files_coll = jl.load(fp)
		fp.close()
		file1_dict = {}
		for it1 in test_files_coll.values():
			for it2 in it1:
				file1_dict[it2] = 0  				
		tp = 0
		summer = 0
		count = 0
		for test_files in test_files_coll.values():
			intersection1 = list(set(test_files).intersection(set(sel_files)))
			not_used = set(test_files).difference(intersection1)
			for files in not_used:
				file1_dict[files] += 1
			tp += len(intersection1)/len(list(set(test_files)))
			count1 = 1
			for files in file1_dict.keys():
				summ = 0
				if file1_dict[files] == 1:
					summ += file1_dict[files]
				count1 += 1
			summer += summ/count1
			count+= 1
			for files in file1_dict.keys():
				file1_dict[files] = 0						
		print (len(test_files_coll), len(file1_dict))	
		print (" Hit Ratio: ", tp/count, " File not usage: ", summer/count, " Number of files used: ", len(sel_files))	
		counter += 1
