import joblib as jl
import os
import matplotlib.pyplot as plt
import numpy as np

def plotting1 (density, tau_coll, p_coll):
	barWidth = 0.25
	fig = plt.subplots(figsize =(12, 8))
	count = 0
	IT = density
	ECE = tau_coll
	CSE = p_coll
	 
	# Set position of bar on X axis
	br1 = np.arange(len(IT))
	br2 = [x + barWidth for x in br1]
	br3 = [x + barWidth for x in br2]
	 
	# Make the plot
	plt.bar(br1, IT, color ='r', width = barWidth,
	        edgecolor ='grey', label ='Subgraph edge density')
	plt.bar(br2, ECE, color ='g', width = barWidth,
	        edgecolor ='grey', label ='Tau-Correlation')
	plt.bar(br3, CSE, color ='b', width = barWidth,
	        edgecolor ='grey', label ='Statistical Significance')
	 
	# Adding Xticks
	plt.xlabel('Subgraphs', fontweight ='bold', fontsize = 15)
	plt.ylabel('Statistical Measures', fontweight ='bold', fontsize = 15)
	plt.xticks([r + barWidth for r in range(len(IT))],
	        ['subgraph-1', 'subgraph-2'])
 	
	leg = plt.legend()
	leg._legend_box.align = "left"
	plt.show()

def plotting2 (tau_subgraph, p_subgraph):
	max_x = 0
	min_x = 0
	counter = 1
	for taus in tau_subgraph:
		x = list(taus.keys())#range(1, len(tau_subgraph)+1)
		if max(x) > max_x:
			max_x = max(x)
		if min(x) < min_x:
			min_x = min(x)
		y = list(taus.values())
		#Create legend
		labels = "subgraph-"+str(counter) 	
			
		#Create axis labels
		plt.xlabel("Betweenness values")
		plt.ylabel("Tau-correlation")
		#Function to bar
		plt.plot(x, y, label = labels)
		plt.xlim(max_x, min_x-0.001)
		plt.title("Betweenness values vs tau correlation")
		leg = plt.legend()
		leg._legend_box.align = "left"
		# function to show the bar			
#		plt.savefig("./plot1_"+sys.argv[2]+".png", dpi=1000)
		counter += 1
	plt.show()	

def plotting3 (quartile1_coll, quartile2_coll):
	counter = 0
	for q1 in quartile1_coll:
		x = q1#range(1, len(tau_subgraph)+1)
		y = quartile2_coll[counter]
		#Create legend
		labels = "subgraph-"+str(counter+1) 	
			
		#Create axis labels
		plt.xlabel("Quartile1")
		plt.ylabel("Quartile2")
		#Function to bar
		plt.plot(x, y, label = labels)
		plt.title("Quartile-Quatrtile plot: "+ labels)
		leg = plt.legend()
		leg._legend_box.align = "left"
		# function to show the bar			
#		plt.savefig("./plot1_"+sys.argv[2]+".png", dpi=1000)
		counter += 1
	plt.show()
	counter = 0
	for q1 in quartile1_coll:
		qd = []
		count = 0
		for qs in q1:
			qd.append(abs(qs - quartile2_coll[counter][count]))
			count += 1
		x = range(1, len(qd)+1)
		y = qd
		#Create legend
		labels = "subgraph-"+str(counter+1) 	
			
		#Create axis labels
		plt.xlabel("Quartiles")
		plt.ylabel("Quartile Deviation")
		#Function to bar
		plt.plot(x, y, label = labels)
		plt.title("Quartile deviation plot: "+ labels)
		leg = plt.legend()
		leg._legend_box.align = "left"
		# function to show the bar			
#		plt.savefig("./plot1_"+sys.argv[2]+".png", dpi=1000)
		counter += 1
	plt.show()	

	

	
if __name__=="__main__":

		
	directory = "./files/results"
	with open(os.path.join(directory, "Tau.pkl"), 'rb') as fp:
		tau_coll = jl.load(fp)
	fp.close()
	with open(os.path.join(directory, "P_value.pkl"), 'rb') as fp:
		p_coll = jl.load(fp)
	fp.close()
	with open(os.path.join(directory, "Quartile1.pkl"), 'rb') as fp:
		quartile1_coll = jl.load(fp)
	fp.close()
	with open(os.path.join(directory, "Quartile2.pkl"), 'rb') as fp:
		quartile2_coll = jl.load(fp)
	fp.close()		
	with open(os.path.join(directory, "TauSubgraph.pkl"), 'rb') as fp:
		tau_subgraph = jl.load(fp)
	fp.close()
	with open(os.path.join(directory, "P_valueSubgraph.pkl"), 'rb') as fp:
		p_subgraph = jl.load(fp)
	fp.close()
	
	directory = "./files/Nodes/Graphs/subgraphs"
	density = []
	for filename1 in os.listdir(directory):	
		try:	
			with open(os.path.join("./files/results/", "Density"+filename1), 'rb') as fp:
				density.append(jl.load(fp))
			fp.close()		
		except:
			print ("Wrong file")
#	print (len(density), len(tau_coll), len(p_coll), len(tau_subgraph), len(p_subgraph), len(quartile1_coll), len(quartile1_coll))		
	#plotting1 (density, tau_coll, p_coll)
	plotting2 (tau_subgraph, p_subgraph)
	plotting3 (quartile1_coll, quartile2_coll)	
