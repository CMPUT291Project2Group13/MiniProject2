import copy
import readData
import fill_table
import time

def normalize_schema(attrDict,FdDict):
	# -normalizes schema to BCNF
	# -returns a list of lists (1 list for each BCNF schema)
	schema = choose_schema(attrDict)
	temp_attr_ls = copy.copy(attrDict[schema])  
	temp_fd_ls = copy.copy(FdDict[schema])  
	BCNF_tf = check_if_superkey(temp_attr_ls, temp_fd_ls) #eg [False, False, True, False] where False = not a superkey (is in order of LHS attributes)
	new_BCNF_schema = []
	temp_schema = [schema,temp_attr_ls,temp_fd_ls]
	Decomp = []   
	while 'False' in BCNF_tf:
		new_BCNF_schema, temp_schema = decompose_schemas(BCNF_tf,schema,temp_schema[1], temp_schema[2])
		Decomp.append(new_BCNF_schema)
		BCNF_tf = check_if_superkey(temp_schema[1], temp_schema[2]) 
	remove_trivial_fd(Decomp)	
	temp_schema = add_trivial_attr(temp_schema)
	Decomp.append(temp_schema)
	remove_dupes(Decomp)
	fill_table.write_to_output(Decomp)
	print('\n ***Normalization successfull***\n')
	time.sleep(1.5)
	return 


def choose_schema(attrDict):
	# -asks user to choose a schema from the database to be normalized
	# -returns schema name as string
	menu_header = ['\n','#'*65,'MENU'.center(63),'#'*65]
	for item in menu_header:
		print(item)
	schemas = list(attrDict.keys())
	for i in range(len(schemas)):
		print('%i- %s\n' %(i+1,schemas[i]))
	valid_input = False
	while valid_input == False:
		opt = input("Please enter a number to select the schema you wish to normalize to BCNF: ")
		valid_input = readData.validate_menu_input(opt,len(attrDict))
	schema_name = schemas[int(opt)-1]
	return schema_name


def check_if_superkey(superkey_closure, Fds):
	# -checks if it's a superkey (i.e. if all attributes are in closure)
	closure = []
	BCNF_tf = [] #list showing if attr are supkeys...stores True or False for each attr
	superkey = False
	for i in range(len(Fds[0])):
		pot_superkey = copy.copy(Fds[0][i]) #using copy to not overwrite the original list
			
		closure = get_attr_closure(pot_superkey, Fds)
		if len(superkey_closure) == len(closure):
			superkey = True
		else:
			superkey = False
		BCNF_tf.append(str(superkey)) 
	return BCNF_tf

def get_attr_closure(pot_superkey, Fds):
	# -computes the attribute closure for the potential superkey
	# -returns the closure as a list of attributes
	closure = pot_superkey
	len_closure_before = len(pot_superkey) #before = before loop stars
	len_closure_after = len_closure_before + 1
	while len_closure_before < len_closure_after: #no new items
		len_closure_before = len(closure)
		for i in range(len(Fds[0])):
			for j in range(len(Fds[0][i])):
				counter = 0
				for attr in Fds[0][i]:
					if attr in closure:
						counter = counter + 1 #counter = lenFds only if all attr of LHS attr list are in closure
		
				if counter == len(Fds[0][i]) and Fds[1][i] not in closure: # = all attr on LHS in closure...so we can add RHS to closure
					closure.append(Fds[1][i])
		len_closure_after = len(closure)
	return closure


def decompose_schemas(BCNF_tf,schema,temp_attr_ls, temp_fd_ls):
	# returns new_BCNF_schema and temp_schema
	# new_BCNF_schema is the schema containing the attributes that violated BCNF in the original schema
	# temp_schema is the schema with the remaining attributes
	idx = BCNF_tf.index('False')
	viol_LHS_attr = temp_fd_ls[0][idx] 
	new_LHS_attr = []
	new_RHS_attr = []
	step = 0
	for i in range(len(temp_fd_ls[0])):
		j = i - step
		if temp_fd_ls[0][j] == viol_LHS_attr:
			new_LHS_attr.append(temp_fd_ls[0].pop(j))			
			RHS_attr = temp_fd_ls[1].pop(j)
			new_RHS_attr.append(RHS_attr)
			if RHS_attr not in new_LHS_attr:
				idx = temp_attr_ls.index(RHS_attr)
				temp_attr_ls.pop(idx)
			step = step + 1		
	new_BCNF_attr_ls = copy.copy(viol_LHS_attr)
	for attr in new_RHS_attr:
		if attr not in new_BCNF_attr_ls:
			new_BCNF_attr_ls.append(attr)
	new_BCNF_schema_name = schema
	for attr in new_BCNF_attr_ls:
		new_BCNF_schema_name = new_BCNF_schema_name + '_' + attr
	new_BCNF_schema = [new_BCNF_schema_name,new_BCNF_attr_ls,[new_LHS_attr,new_RHS_attr]]
	for item in new_RHS_attr:	
		step = 0
		for i in range(len(temp_fd_ls[0])):
			j = i - step
			if item == temp_fd_ls[1][j]:
				temp_fd_ls[1].pop(j)
				temp_fd_ls[0].pop(j)
				step = step + 1
			elif item in temp_fd_ls[0][j]:
				temp_fd_ls[0].pop(j)
				temp_fd_ls[1].pop(j)
				step = step + 1
	temp_schema_name = schema
	for attr in temp_attr_ls:
		temp_schema_name = temp_schema_name + '_' + attr
	temp_schema =  [temp_schema_name,temp_attr_ls,[temp_fd_ls[0],temp_fd_ls[1]]]
	return new_BCNF_schema, temp_schema


def remove_trivial_fd(Decomp):     
	#removes trivial FDs such that Y: X inters. Y = empty set
	for schema in Decomp:
		for i in range(len(schema[2][1])):
			for j in range(len(schema[2][0])):
				if schema[2][1][i] in schema[2][0][j]:
					triv_attr = schema[2][1][i]
					idx = schema[2][0][j].index(triv_attr)
					schema[2][0][j].pop(idx)
	return 


def add_trivial_attr(temp_schema):
	# -add the trivial FDs (only needed for last schema in BCNF normalization process)
	# -returns the modified temp_schema
	if len(temp_schema[2][0]) == 0:
		for i in range(len(temp_schema[1])):
			attributes = copy.copy(temp_schema[1])
			temp_schema[2][0].append(attributes)
			temp_schema[2][1] = attributes
	return temp_schema
        
        
def remove_dupes(Decomp):
	#removes duplicate entries in the LHS attr list	
	for schema in Decomp:
		no_dupes_ls = []
		for item in schema[2][0]:
			if item not in no_dupes_ls:
				no_dupes_ls.append(item)
		schema[2][0] = copy.copy(no_dupes_ls)
	return
        
