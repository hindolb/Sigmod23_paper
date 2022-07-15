import joblib as jl
import networkx as nx
import re
import networkx.algorithms.components as comp
from networkx.algorithms import simple_paths as sp

if __name__ == "__main__":
    with open("./TestingTasks.pkl", 'rb') as fp:
        test_set = jl.load(fp)
    fp.close()
    with open("./files/results/new2.pkl", 'rb') as fp:
        files3 = jl.load(fp)
    fp.close()
    with open("./files/results/control2.pkl", 'rb') as fp:
       thresholds = jl.load(fp)
    fp.close()

    tp = 0
    summ = 0
    count = 0
    for tasks in test_set.keys():
      files1 = test_set[tasks]
      file1_dict = {}
      for it1 in files1:
        file1_dict[it1] = 0      
      if len(files1) == 0:
        continue
      intersection1 = set(files1).intersection(set(files3))
      not_used = set(files1).difference(intersection1)
      for files in not_used:
        file1_dict[files] =  file1_dict[files] + 1
      tp += len(intersection1)/len(files1)
      count1 = 0 
      for files in file1_dict.keys():
        summ += file1_dict[files]
        count1 += 1
      summ = summ/count1
      count+= 1
    print (tp/count)
    print (summ/count)
    

    max_tp = -1 
    max_summ = -1
    for threshold in thresholds.keys():
      files2 = thresholds[threshold]
      tp = 0
      count = 0
      file2_dict = {}
      for it1 in files2:
        file2_dict[it1] = 0
      for tasks in test_set.keys():
        files1 = test_set[tasks]
        if len(files1) == 0:
          continue        
        intersection1 = set(files1).intersection(set(files2))
        not_used = set(files2).difference(intersection1)
        for files in not_used:
          file2_dict[files] =  file2_dict[files] + 1
          tp += len(intersection1)/len(files1)
          count += 1
          tp += 0          
        count1 = 0 
        summ = 0
        for file in file2_dict.keys():
            if count == 0:
                continue
            else:
              summ += file2_dict[files]/count
              count1 += 1
        if count == 0:
            continue
        else:
            if tp/count > max_tp:
              max_tp = tp/count
        if count1 > 0:
            continue
        else:
            if summ/count1 > max_summ:
              max_summ = summ/count1

    print (max_tp)  
    print (max_summ)

