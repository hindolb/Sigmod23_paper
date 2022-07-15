import joblib as jl
import networkx as nx
import re
import os

def plotting(tp_list1, tn_list1, fp_list1, fn_list1, ac_list1, f1_list1, sp_list1, se_list1, fo_list1, threshold_no, count11_list, tp_avg2, tn_avg2, fp_avg2, fn_avg2, ac_avg2, f1_avg2, sp_avg2, se_avg2, fo_avg2):

	barWidth = 0.25
	I1 = tp_list1
	I2 = tn_list1
	I3 = fp_list1
	I4 = fn_list1
	I5 = ac_list1
	I6 = f1_list1
	I7 = sp_list1
	I8 = se_list1
	I9 = fo_list1 
	I10 = tp_avg2
	I11 = tn_avg2
	I12 = fp_avg2
	I13 = fn_avg2
	I14 = ac_avg2
	I15 = f1_avg2
	I16 = sp_avg2
	I17 = se_avg2
	I18 = fo_avg2	
	fig = plt.subplots(figsize =(12, 8))
	count = 0
	ECE = tau_coll
	CSE = p_coll
	 
	# Set position of bar on X axis
	br1 = np.arange(len(I1))
	br2 = [x + barWidth for x in br1]
	br3 = [x + barWidth for x in br2]
	br4 = [x + barWidth for x in br3]
	br5 = [x + barWidth for x in br4]
	br6 = [x + barWidth for x in br5]
	br7 = [x + barWidth for x in br6]
	br8 = [x + barWidth for x in br7]
	br9 = [x + barWidth for x in br8]
	br10 = [x + barWidth for x in br9]
	br11 = [x + barWidth for x in br10]
	br12 = [x + barWidth for x in br11]
	br13 = [x + barWidth for x in br12]
	br14 = [x + barWidth for x in br13]
	br15 = [x + barWidth for x in br14]
	br16 = [x + barWidth for x in br15]
	br17 = [x + barWidth for x in br16]
	br18 = [x + barWidth for x in br17]
	
		 
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
 	
	plt.legend()
	plt.show()

if __name__ == "__main__":

    with open("./TestingTasks.pkl", 'rb') as fp:
        test_tasks = jl.load(fp)
    fp.close()  

    with open("./FileSize.pkl", 'rb') as fp:
        file_size = jl.load(fp)
    fp.close()  

    num_files = len(list(file_size.keys()))


    with open("./files/mysubgraphs.pkl", 'rb') as fp:
        file_sets = jl.load(fp)
    fp.close()

    tp = 0
    tn=  0
    fp = 0
    fn = 0
    count = 0
    for tasks in test_tasks:
        files = test_tasks[tasks]
        tp += len(set(files).intersection(set(file_sets)))
        num_notsel = set(list(file_size.keys())).difference(set(files))
        tn += len(num_notsel.difference(set(file_sets)))
        fp += len(set(file_sets).difference(set(files)) )
        fn += len(set(files).difference(set(file_sets)))
        count +=1
    tp_avg2 = tp/count
    tn_avg2 = tn/count
    fp_avg2 = fp/count
    fn_avg2 = fn/count        
    ac_avg2 = (tp_avg2+tn_avg2)/(tp_avg2+tn_avg2+fp_avg2+fn_avg2)
    f1_avg2 = (2*tp_avg2)/((2*tp_avg2)+fp_avg2+fn_avg2)
    sp_avg2 = tn_avg2/(tn_avg2+fp_avg2)
    se_avg2 = tp_avg2/(tp_avg2+fn_avg2)
    fo_avg2 = fp_avg2/(fp_avg2+tn_avg2)
    #plotting for each threhold
    #TP, TN, FP, FN, Accuracy, F1, ROC- for all threshold and subgraph
    #for threhold = threhold_no, subgraph = count1

    for filename1 in os.listdir("./files"):
        count11_list = []
        if filename1[-3:] == 'thl':
            threhold_no = filename1[:-4]
            with open(os.path.join("./files", filename1), 'rb') as fp:
                threshold_sets = jl.load(fp)
        fp.close()
        tp_list1 = []
        tn_list1 = []
        fp_list1 = []
        fn_list1 = []
        ac_list1 = []
        f1_list1 = []
        sp_list1 = []
        se_list1 = []
        fo_list1 = []
		
        for threshold in threshold_sets.keys():
            files = threshold_sets[threshold]
            count1 = 1
            for file_sets in files:
                tp = 0
                tn = 0
                fp = 0
                fn = 0
                count = 0
                for tasks in test_tasks.keys():
                    files = test_tasks[tasks]
                    tp += len(set(files).intersection(set(file_sets)))                    
                    num_notsel = set(list(file_size.keys())).difference(set(files))
                    tn += len(num_notsel.difference(set(file_sets)))
                    fp += len(set(file_sets).difference(set(files)) )
                    fn += len(set(files).difference(set(file_sets)))
                    count +=1
                print (len(set(file_sets)))
                tp_avg = tp/count
                tn_avg = tn/count
                fp_avg = fp/count
                fn_avg = fn/count        
                tp_list1.append(tp_avg)
                tn_list1.append(tn_avg)
                fp_list1.append(fp_avg)
                fn_list1.append(fn_avg)
                ac_list1.append((tp_avg+tn_avg)/(tp_avg+tn_avg+fp_avg+fn_avg))
                f1_list1.append((2*tp_avg)/((2*tp_avg)+fp_avg+fn_avg))
                sp_list1.append(tn_avg/(tn_avg+fp_avg))
                se_list1.append(tp_avg/(tp_avg+fn_avg))
                fo_list1.append(fp_avg/(fp_avg+tn_avg))            
                count11_list.append(count1)
                count1 += 1
    
        #plotting(tp_list1, tn_list1, fp_list1, fn_list1, ac_list1, f1_list1, sp_list1, se_list1, fo_list1, threshold_no, count11_list, tp_avg2, tn_avg2, fp_avg2, fn_avg2, ac_avg2, f1_avg2, sp_avg2, se_avg2, fo_avg2)
        print (len(tp_list1), len(count11_list),tp_avg2, tp_list1)
        #TP, TN, FP, FN, Accuracy, F1, ROC- for all threshold and subgraph
        #for threhold = threhold_no, subgraph = count1


