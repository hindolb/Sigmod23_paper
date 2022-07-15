import joblib as jl
import os
import re
from matplotlib import pyplot as plt

def test_module(betweenness, weights, count, filename1):
	sum_of_weights = []
	for it1 in betweenness.keys():
		edges = betweenness[it1]
		temp1 = 0	
		for it2 in edges:
			temp1 += weights[it2]
		sum_of_weights.append(temp1/len(edges))					
		
	print ("Saving Sum of edge weights")
	filename1 = filename1 + ".sow"
	filename = os.path.join("./results", filename1)			
	new_file = open(filename, "wb")
	jl.dump(sum_of_weights, new_file)
	new_file.close()	

	print ("Saving betweenness centrality values")
	filename1 = filename1 + ".bwc"
	filename = os.path.join("./results", filename1)			
	new_file = open(filename, "wb")
	jl.dump(betweenness, new_file)
	new_file.close()	


if __name__=="__main__":
	
	directory1 = "./files/Nodes/Graphs/subgraphs"
	filename1 = "./files/Nodes/Weights/Weight.pkl"	
	print ("Loading Weights: ", filename1)
	new_file = open(filename1, "rb")
	weights = jl.load(new_file)
	new_file.close()
	
	for filename1 in os.listdir(directory1):
		
		if filename1[0:5] != "Tuple":
			continue
		print ("Loading betweenness-centrality: ", filename1)
		filename = os.path.join(directory1, filename1)			
		new_file = open(filename, "rb")
		betweenness1 = jl.load(new_file)
		new_file.close()	
		print ("Sorting the betweenness dictionary")
		list1 = list(betweenness1.keys())
		list1.sort(reverse = True)
		list2 = list(betweenness1.values())
		temp = {}
		temp2 = {}
		count = 1
		for it1 in list1:
			temp2[count] = it1
			temp[count] = list2[count-1]
			count += 1
			#temp[it1] = items[it1]
		del betweenness1
		del list1
		betweenness = temp
		mapping = temp2
		del temp
		del temp2
#		print (len(betweenness[1]))
#		continue

		print ("Saving the mapping")
		filename2 = filename1 + ".map"
		filename = os.path.join("./results", filename2)			
		new_file = open(filename, "wb")
		jl.dump(mapping, new_file)
		new_file.close()	
		test_module(betweenness, weights, it1+1, filename1)		
		
	


						
