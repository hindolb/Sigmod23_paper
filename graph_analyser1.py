import joblib as jl
import os
from multiprocessing import Pool
import time
import itertools
import networkx as nx
import sys
import re

def non_parallel(g):
	start = time.time()  
	d1 = nx.edge_betweenness_centrality(g)
	end = time.time()
	d2 = {}
	print ("Time to find betweenness centrality of all nodes (non-parallel): ", end-start)
	start = time.time()
	for it1 in d1.keys():
		val = d1[it1]
		if val in d2.keys():
			temp = d2[val]
			temp.append(str(it1[0]) +"///..." +str(it1[1]))
			d2[val] = temp
		else:
			d2[val] = [str(it1[0]) +"///..." +str(it1[1])]
	return d2

def chunks(l, n):
    """Divide a list of nodes `l` in `n` chunks"""
    l_c = iter(l)
    while 1:
        x = tuple(itertools.islice(l_c, n))
        if not x:
            return
        yield x


def betweenness_centrality_parallel(G, processes=None):
    """Parallel betweenness centrality  function"""
    p = Pool(processes=processes)
    node_divisor = len(p._pool) * 4
    node_chunks = list(chunks(G.nodes(), int(G.order() / node_divisor)))
    num_chunks = len(node_chunks)
    bt_sc = p.starmap(
        nx.betweenness_centrality_subset,
        zip(
            [G] * num_chunks,
            node_chunks,
            [list(G)] * num_chunks,
            [True] * num_chunks,
            [None] * num_chunks,
        ),
    )

    # Reduce the partial solutions
    bt_c = bt_sc[0]
    for bt in bt_sc[1:]:
        for n in bt:
            bt_c[n] += bt[n]
    return bt_c
	

if __name__=="__main__":
	
	directory = "./files/Nodes/Graphs/subgraphs"
	count = 1
	for filename1 in os.listdir(directory):
		if filename1 == ".ipynb_checkpoints":
			continue
		print ("Loading subgraph: ", filename1)
		filename = os.path.join(directory, filename1)			
		new_file = open(filename, "rb")
		G = jl.load(new_file)
		new_file.close()	
		
		tuples = non_parallel(G)
		
		print ("Saving for subgraph: ", filename1)
		filename = os.path.join(directory, "Tuple_"+str(count)+".tup")								
		new_file = open(filename, "wb")
		jl.dump(tuples, new_file)
		new_file.close()	
		
		count += 1
		
		
