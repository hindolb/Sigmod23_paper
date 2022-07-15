import requests 
import xml.etree.ElementTree as ET 
import os
import joblib as jl
import numpy as np
from scipy import linalg 
from scipy.spatial import distance
from scipy.sparse import lil_matrix


def matrixOperation(train_tasks):
	files = []
	tasks = []
	num_files = []
	num_tasks = []
	file_id_mapping = {}
	id_file_mapping = {}
	task_id_mapping = {}
	id_task_mapping = {}	
	temp = []
	count1 = 0
	count2 = 0
	print ("Creating task ID and file ID")
	for tasks in train_tasks.keys():
		task_id_mapping[tasks] = count1
		id_task_mapping[count1] = tasks
		count1 += 1
		for file1 in train_tasks[tasks]:
			if file1 not in file_id_mapping.keys():
				file_id_mapping[file1] = count2
				id_file_mapping[count2] = file1
				count2 += 1
	num_files = count2
	del temp
	num_tasks = count1
	print ("Initttializing matrix")
	file_task_matrix = lil_matrix((num_tasks,num_files), dtype=np.int8).toarray()
	print ("Dimension: ", file_task_matrix.shape)
	count1 = 0
	print ("Creating matrix and file ID")
	for tasks in train_tasks.keys():
		for file1 in train_tasks[tasks]:
			task_id = task_id_mapping[tasks]
			file_id = file_id_mapping[file1]
			temp =file_task_matrix[task_id][file_id]
			temp += 1
			file_task_matrix[task_id][file_id] = temp 
	file_task_matrix = np.transpose(file_task_matrix)	 		
	print ("Done creatiiing matrix, Saving Data")
	with open("File_Task_Matrix.pkl", 'wb') as fp:
		jl.dump(file_task_matrix, fp)
	fp.close()
	del file_task_matrix
	with open("Id_File_Mapping.pkl", 'wb') as fp:
		jl.dump(id_file_mapping, fp)
	fp.close()
	with open("Id_Task_Mapping.pkl", 'wb') as fp:
		jl.dump(id_task_mapping, fp)
	fp.close()
	del id_file_mapping
	del id_task_mapping	
	with open("File_Id_Mapping.pkl", 'wb') as fp:
		jl.dump(file_id_mapping, fp)
	fp.close()
	with open("Task_Id_Mapping.pkl", 'wb') as fp:
		jl.dump(task_id_mapping, fp)
	fp.close()
	print ("Done saving data")
	
			
def test_train_split(data, task_runtime):
	print ("Starting train-test split")
	train_task = {}
	test_task = {}
	count = 0
	data_file = {}
	file_runtime = {}
	marker = 0
	for task1 in data.keys():
		for task2 in data:		
			if len(set(data[task1]).intersection(set(data[task2]))) != 0:
				if count >= (0.2*len(data.values())):
					marker = 1		
					break
				else:
					test_task[task1] = data[task1]
					train_task[task2] = data[task2]
					count += 2				
					break
		if marker == 1:
			break
	for task1 in data.keys():
		if task1 not in test_task.keys(): 
			if task1 not in train_task.keys():
				train_task[task1] = data[task1]
	print ("Finished splitting data")		
	for tasks in train_task.keys():
		file_colls = train_task[tasks]
		runtime = task_runtime[tasks]
		for files in file_colls:
			try:
				temp = data_file[files]
				temp.append(tasks)
				data_file[files] = temp
				temp = file_runtime[files]
				file_runtime[files] = temp + runtime
			except:
				temp = [tasks]
				data_file[files] = temp
				file_runtime[files] = 0
	return train_task, test_task, data_file, file_runtime


def parseXML(xmlfile, data, file_size, task_runtime): 
	
	print ("Extracting from XML")
	try:
		# create element tree object 
		tree = ET.parse(xmlfile) 
  	
		# get root element 
		root = tree.getroot() 
	
		for child in root:
			try:
				#Check if task execution time and file size are in int/float
				task_id = xmlfile+"_"+child.attrib['id']
				task_runtime[task_id] = float(child.attrib['runtime'])
				data[task_id] = list()
				for grn_child in child:
					if grn_child.attrib['link'] == "input":	
						data[task_id].append(grn_child.attrib['file'])
						file_size[grn_child.attrib['file']] = grn_child.attrib['size']
			except:
				continue
	except:
		print ("This XML file could not be processed")	
	print ("Finished XML   extraction")
def main(): 

	# directory to store the file dependencises of each task
	# key: task_id, value = file_id 
	data = {}
	file_size = {}
	task_runtime = {}

	# iterarating over all files in the directory
	dirs = "./dataset"
	for files in os.listdir(os.path.join("./",dirs)):
		if files[-3:] == "dax":
			# parse xml file 
			parseXML(os.path.join(os.path.join("./",dirs),files), data, file_size, task_runtime) 

	train_tasks, test_tasks, data_file, file_runtime = test_train_split(data, task_runtime)
	print("Number of training tasks: ", len(train_tasks))
	print("Number of testing tasks: ", len(test_tasks))

	# saving extracted data

	print("Saving extracted data")
	new_file = open("TrainingTasks.pkl", "wb")
	jl.dump(train_tasks,new_file)
	new_file.close()
	new_file = open("TestingTasks.pkl", "wb")
	jl.dump(test_tasks,new_file)
	new_file.close()
	new_file = open("TrainingFiles.pkl", "wb")
	jl.dump(data_file,new_file)
	new_file.close()
	new_file = open("TrainingFileRuntime.pkl", "wb")
	jl.dump(file_runtime,new_file)
	new_file.close()	
	new_file = open("FileSize.pkl", "wb")
	jl.dump(file_size,new_file)
	new_file.close()		
	print("Finished saving extracted data") 
	
	del test_tasks
	del file_size


	new_file = open("TrainingTasks.pkl", "rb")
	train_tasks = jl.load(new_file)
	new_file.close()		
	matrixOperation(train_tasks)
      
if __name__ == "__main__": 
  
	# calling main function 
	main() 

'''
	tree structure:
	<adag>
		<job>
			<uses/>
		</job>
	</adag>	
'''
