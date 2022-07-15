import joblib as jl
import os

if __name__=="__main__":

	print ("Loading the merged and sorted betweenness")
	filename = "./files/results/SortedBetweenness.pkl"
	with open (filename, "rb") as fp:
		final_betweenness = jl.load(fp)
	fp.close()

	print ("Loading the weights of the edges")
	filename = "./files/Nodes/Weights/Sorted_Weights.pkl"
	with open (filename, "rb") as fp:
		weights_sorted = jl.load(fp)
	fp.close()


	print ("Starting computation")
	list_of_edges = []
	for betweenness in final_betweenness.keys():		
		edge_pairs_coll = final_betweenness[betweenness]		
		break
	del final_betweenness

	print ("Loading the subgraphs")
	count = 1
	edge_coll = {}
	node_coll = {}
	for filename in os.listdir("./files/Nodes/Graphs/subgraphs"):
		if filename[-3:] == "pkl":
			filename1 = os.path.join("./files/Nodes/Graphs/subgraphs", filename)
			with open (filename1, "rb") as fp:
				edge_coll[count] = list((jl.load(fp)).edges)
				node_coll[count] = list((jl.load(fp)).nodes)
			fp.close()
			count += 1	

	edge_partition = {}
	print ("Seperating edges by subgraph")
	for num_subgraphs in edge_coll:
		subgraphs = edge_coll[num_subgraphs]
		for edges in edge_pairs_coll:
			if edges in subgraphs:
				edge_partition[num_subgraphs] = edges
	del edge_coll

	print ("Finding a walk in each subgraph")
	for subgraph_no in edge_partition:
		edge_list = edge_partition[subgraph_no]
		nodes = []
		all_nodes = node_coll[count]
		g = nx.Graph()
		for edge in edge_list:
			temp = edge.split("///...") 
			g.add_edge(edge)			
			node1 = temp[0]
			node2 = temp[1]
			edge_list = []
			for 
		
		for 