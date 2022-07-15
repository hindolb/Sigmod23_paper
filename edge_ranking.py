import joblib as jl
import os

if __name__ == "__main__":

	print ("Loading weights of the edges of the graph")
	filename = "./files/Nodes/Weights/TrainingFiles.pkl"
	new_file = open(filename, "rb")
	weight = jl.load(new_file)
	new_file.close()


	directory = "./files/Nodes/Graphs/subgraphs"
	final_betweenness = {}
	print ("Merging betweenness values of edges across subgraphs")
	count = 1	
	for filename1 in os.listdir(directory):
		if filename1[0:5] != "Tuple":
			continue
		print ("Loading betweenness-centrality: ", filename1)
		filename = os.path.join(directory, filename1)			
		new_file = open(filename, "rb")
		betweenness = jl.load(new_file)
		new_file.close()	
		
		sorted_betweenness = {}				
		for values in betweenness.keys():
			edge_list1 = betweenness[values]
			try:
				edge_list2 = final_betweenness[values]
				for edges in edge_list2:
					edge_list1.append(edges)
				final_betweenness[values] = list(set(edge_list1))
			except:
				final_betweenness[values] = edge_list1
				
		print ("Sorting individual dictionary of subgraphs")
		for values in betweenness.keys():
			list_of_edges = betweenness[values]		
			edge_weights = {}
			for edge_pairs in list_of_edges:
				edge_weights[edge_pairs] = weight[edge_pairs]
			sorted_by_weight = {k: v for k, v in sorted(edge_weights.items(), key=lambda item: item[1], reverse = True)}
			temp = []
			for it1 in sorted_by_weight.keys():
				temp.append(it1)
			sorted_betweenness[values] = temp
		del temp
		del edge_weights
		del sorted_by_weight
		del list_of_edges
		print ("Sorting the keys")
		final_betweenness1 = {}
		for value in sorted (sorted_betweenness.keys(), reverse = True):
			final_betweenness1[value] = sorted_betweenness[value]
		del sorted_betweenness
		print ("Saving the sorted betweenness for the subgraph")
		filename = os.path.join("./files/results/SortedBetweennessTuple_"+str(count)+".pkl")			
		with open (filename, "wb") as fp:
			jl.dump(final_betweenness1, fp)
		fp.close()
		del final_betweenness1
		count += 1
		
				
