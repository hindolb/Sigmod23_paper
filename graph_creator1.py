import networkx as nx
import joblib as jl
#from memory_profiler import profile
import os
import re

#@profile
def graphCreator(files_list1, filename1):

	directory_graph = "./files/Nodes/Graphs"
	directory_weight = "./files/Nodes/Weights"	
	graph_file = filename = os.path.join(directory_graph, "Graph.pkl")							
	graph_file = re.sub(r'(ExtractedWorkflowData)','Graph', filename)
	weight_file = filename = os.path.join(directory_weight, "Weight.pkl")							
	weight_file = re.sub(r'(ExtractedWorkflowData)','Weight', filename)
	g= nx.Graph()
	print ("Creating edges of the graph")
	for it1 in files_list1.keys():
		for it2 in files_list1.keys():
			task1 = files_list1[it1]
			task2 = files_list1[it2]
			common = len(list(set(task1).intersection(set(task2))))
			if common != 0:
				g.add_edge(it1, it2, weight = common)					
	print ("Successfully created a graph")	
	print("Saving the created graph")
	new_file = open(graph_file, "wb")
	jl.dump(g, new_file)
	new_file.close()
	del g
	
	weight = {}
	for it1 in files_list1.keys():
		for it2 in files_list1.keys():
			task1 = files_list1[it1]
			task2 = files_list1[it2]
			common = len(list(set(task1).intersection(set(task2))))
			if common != 0:
				weight[it1+"///..."+it2] = common
	print ("Successfully computed the weights")	
	print("Saving the computed weights")
	new_file = open(weight_file, "wb")
	jl.dump(weight, new_file)
	new_file.close()	

if __name__=="__main__":
	
	filename = "./TrainingFiles.pkl"
	print ("Loading graph")
	new_file = open(filename, "rb")
	file_list1 = jl.load(new_file)
	new_file.close()

	graphCreator(file_list1, filename)
	
