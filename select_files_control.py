import joblib as jl
import networkx as nx
import re
import networkx.algorithms.components as comp


if __name__ == "__main__":
	#print ("Loading the graph")
	with open("files/Nodes/Weights/TrainingFiles.pkl", 'rb') as fp:
		weights = jl.load(fp)
	fp.close()
	
	all_weights = list(set(list(weights.values())))
	
	files = []
	for it1 in weights.keys():
		temp = it1.split("///...")
		files.append(temp[0])
		files.append(temp[1])
	num_files = len(list(set(files)))
	del files
	 
	for threshold in all_weights:
		print ("Computing for Threhold: ", threshold)
		print ("Loading the graph")
		with open("files/Nodes/Graphs/TrainingFiles.pkl", 'rb') as fp:
			graph = jl.load(fp)
		fp.close()	
		
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
#			count = 0
#			print(len(list(graph.nodes)))
			sel_files = list(subgraphs.nodes)
			with open("./TestingTasks.pkl", 'rb') as fp:
				test_files_coll = jl.load(fp)
			fp.close()
			file1_dict = {}
			for it1 in test_files_coll.values():
				for it2 in it1:
					file1_dict[it2] = 0  				
			tp = 0
			summ = 0
			count = 0
			for test_files in test_files_coll.values():
				intersection1 = list(set(test_files).intersection(set(sel_files)))
				not_used = set(test_files).difference(set(intersection1))
				for files in not_used:
					file1_dict[files] += 1
				tp += len(intersection1)/len(list(set(test_files)))
				count1 = 1
				for files in file1_dict.keys():
					if file1_dict[files] == 1:
						summ += file1_dict[files]
					count1 += 1
				summ = summ/count1
				count+= 1
			print ("Number of files: ", len(sel_files), "Out of: ", num_files) 
			print (" Hit Ratio: ", tp/count, " File not usage: ", summ/count)
			counter += 1
		print ("\n\n")	
