import joblib as jl
import os
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import pearsonr
from numpy import cov
import sys
import numpy as np
import networkx as nx

#Note: sys.argv in use: Enter number of betweenness values in the subgraph to compute the statistics
#TODO: intra betweenness weights random

if __name__=="__main__":
	print ("Loading sorted weights of the edges of the graph")
	filename = "./files/Nodes/Weights/SortedWeights.pkl"
	new_file = open(filename, "rb")
	sorted_weights = jl.load(new_file)
	new_file.close()
	rank = {}
	count = 1
	for edges in sorted_weights.keys():
		rank[edges] = count
		count += 1
	del sorted_weights
		
	directory = "./files/results"
	tau_coll = []
	p_coll = []
	quartile1_coll = []
	quartile2_coll = []
	tau_subgraph = []
	p_subgraph = []
	anomaly = []
	for filename1 in os.listdir(directory):	
		quartile1 = []
		quartile2 = []
		tau_betweenness = {}
		p_betweenness = {}
		anomaly_betweenness = []			
		count = 1	
		if filename1[17:22] == "Tuple":		
			with open(os.path.join(directory, filename1), 'rb') as fp:
				betweenness = jl.load(fp)
			fp.close()			
			rank1 = {}
			rank2 = {}
			print ("Finding rank of the subgraph")
			count1 = 0
			count2 = 1

			min_rank = -1
			first = betweenness[list(betweenness.keys())[0]]
			temp = 0
			for it1 in first:
				if rank[it1] < min_rank:
					temp += 1
				else:
					min_rank = temp
			anomaly_betweenness.append(min_rank)
			for values in betweenness.keys():
				edge_coll = betweenness[values]
				rank3 = {}
				rank4 = {}
				for edge in edge_coll:
					rank2[edge] = count
					rank1[edge] = rank[edge]
					rank3[edge] = count2
					rank4[edge] = rank[edge]
					count += 1		
					count2 += 1
				if count1 < int(sys.argv[1]):	
					tau, p_value = stats.kendalltau(list(rank1.values()), list(rank2.values()))
#					print (list(rank3.values()), list(rank4.values()), tau)					
					tau_betweenness[values] = tau
					p_betweenness[values] = p_value
				count1 += 1
				del rank3, rank4
			tau_subgraph.append(tau_betweenness)
			p_subgraph.append(p_betweenness)
			anomaly.append(anomaly_betweenness)			
			del tau_betweenness, p_betweenness
			
			print ("Find kendall tau")
			tau, p_value = stats.kendalltau(list(rank1.values()), list(rank2.values()))
			tau_coll.append(tau)
			p_coll.append(p_value)
			print ("finding quartiles")
			quartile1.append(np.quantile(list(rank1.values()), .125))
			quartile1.append(np.quantile(list(rank1.values()), .25))
			quartile1.append(np.quantile(list(rank1.values()), .275))
			quartile1.append(np.quantile(list(rank1.values()), .50))
			quartile1.append(np.quantile(list(rank1.values()), .625))
			quartile1.append(np.quantile(list(rank1.values()), .75))
			quartile1.append(np.quantile(list(rank1.values()), .875))
			quartile1.append(np.quantile(list(rank1.values()), 1))
			quartile2.append(np.quantile(list(rank2.values()), .125))
			quartile2.append(np.quantile(list(rank2.values()), .25))
			quartile2.append(np.quantile(list(rank2.values()), .275))
			quartile2.append(np.quantile(list(rank2.values()), .50))
			quartile2.append(np.quantile(list(rank2.values()), .625))
			quartile2.append(np.quantile(list(rank2.values()), .75))
			quartile2.append(np.quantile(list(rank2.values()), .875))
			quartile2.append(np.quantile(list(rank2.values()), 1))
			quartile1_coll.append(quartile1)
			quartile2_coll.append(quartile2)
			
#	print (tau_coll)		
#	print (p_coll)
#	print (tau_subgraph)
#	print (p_subgraph)

	print ("Saving statistics")
	with open(os.path.join(directory, "Tau.pkl"), 'wb') as fp:
		jl.dump(tau_coll, fp)
	fp.close()
	with open(os.path.join(directory, "P_value.pkl"), 'wb') as fp:
		jl.dump(p_coll, fp)
	fp.close()
	with open(os.path.join(directory, "Quartile1.pkl"), 'wb') as fp:
		jl.dump(quartile1_coll, fp)
	fp.close()
	with open(os.path.join(directory, "Quartile2.pkl"), 'wb') as fp:
		jl.dump(quartile2_coll, fp)
	fp.close()		
	with open(os.path.join(directory, "TauSubgraph.pkl"), 'wb') as fp:
		jl.dump(tau_subgraph, fp)
	fp.close()
	with open(os.path.join(directory, "P_valueSubgraph.pkl"), 'wb') as fp:
		jl.dump(p_subgraph, fp)
	fp.close()

	with open(os.path.join(directory, "AnomalySubgraph.pkl"), 'wb') as fp:
		jl.dump(anomaly, fp)
	fp.close()
	
	print ("End of betweenewss centrality statistics computation and persistence")
	directory = "./files/Nodes/Graphs/subgraphs"
	for filename1 in os.listdir(directory):	
		try:
			with open(os.path.join(directory, filename1), 'rb') as fp:
				g = jl.load(fp)
			fp.close()	
			with open(os.path.join("./files/results/", "Density"+filename1), 'wb') as fp:
				jl.dump(nx.density(g), fp)
			fp.close()									
		except:
			print ("Not graph file. Ignoring!!")
