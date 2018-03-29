import sqlite3
import connectDB
import copy 


def readData():
	attrDict = {}
	FdDict = {}
	
	#create attributes dictionary with relation name as key
	connectDB.c.execute('''SELECT Name,Attributes FROM InputRelationSchemas''')
	name_attr = connectDB.c.fetchall()
	for item in name_attr:   #item looks like this ('R1', 'A,B,C,D,E,F,G,H,K')
		attributes = item[1].split(',')
		attrDict[item[0]] = attributes


	#create FD dictionary with relation name as key and value is [LHS list,RHS list]
	connectDB.c.execute('''SELECT Name,FDs FROM InputRelationSchemas''')
	name_FDs = connectDB.c.fetchall()
	for item in name_FDs:   #item looks like this ('R1', '{A,B,H}=>{C,K}; {A}=>{D}')
		FDs = item[1].replace('{','')
		FDs = FDs.replace('}','')
		FDs = FDs.split(';')
		LHS = []
		RHS = []		
		for attr in FDs:
			FD = attr.split('=>')
			FDlhs = FD[0].split(',')
			for i in range(len(FDlhs)):
				FDlhs[i] = FDlhs[i].strip()
			FDrhs = FD[1].split(',')
			for i in range(len(FDrhs)):
				FDrhs[i] = FDrhs[i].strip()			
			LHS.append(FDlhs)
			RHS.append(FDrhs)
		FdDict[item[0]] = [LHS,RHS]  #looks like this {'ForAttrClosureF2': [[['C'], [' F'], [' E']], [['E'], ['A'], ['F']]], 'R1':.....
		
	FdDict = decompose_RHS(FdDict)
	
	return attrDict, FdDict


def decompose_RHS(FdDict):
	# -splits up attributes on RHS
	for key in FdDict:
		step = 0
		for i in range(len(FdDict[key][1])):
			j = i + step
			if len(FdDict[key][1][j]) > 1:
				RhsAttr = FdDict[key][1].pop(j)   #['C', 'K']
				LhsAttr = FdDict[key][0].pop(j)
				NrOfAttr = len(RhsAttr)
				step = step + NrOfAttr - 1 #if have 2 attr will add 1 to j
				for idx in range(len(RhsAttr)):
					FdDict[key][0].insert(j+idx,LhsAttr)
					FdDict[key][1].insert(j+idx,RhsAttr[idx])
			else:
				FdDict[key][1][j] = ''.join(FdDict[key][1][j])   #converts ls to str
				
	FdDict = remove_trivial_fd(FdDict)
	
	return FdDict


def remove_trivial_fd(FdDict):      ########ok to remove trivial ones????
	#such that Y: X inters. Y = empty set
	for key in FdDict:
		step = 0
		for i in range(len(FdDict[key][0])):
			i = i - step
			if FdDict[key][1][i] in FdDict[key][0][i]:
				FdDict[key][1].pop(i)
				FdDict[key][0].pop(i)
				step = step + 1
		
	return FdDict


def check_if_superkey(superkey_closure, Fds):
	# -checks if it's a superkey (i.e. if all attributes are in closure)
	closure = []
	BCNF_tf = [] #list showing if attr are in BCNF (=superkey/trivial)...stores True or False for each attr
	superkey = False
	for i in range(len(Fds[0])):
		pot_superkey = copy.copy(Fds[0][i]) #using copy to not overwrite the original list
		##print('potential superkey: ') 
		##print(pot_superkey) 		
		closure = get_attr_closure(pot_superkey, Fds)
		if len(superkey_closure) == len(closure):
			superkey = True
		else:
			superkey = False
		BCNF_tf.append(str(superkey)) 
		

		##print('closure: ') 
		##print(closure) 

		
		###returning a list like this [False, False, False, False, True, False, False, False, False]
		
	return BCNF_tf
	
def decompose_schema(BCNF_tf,temp_attr_ls,temp_fd_ls):
	#temp_attr_ls contains all attr minus the ones we already removed and put in separate table
	print(BCNF_tf)
	print(temp_attr_ls)
	print(temp_fd_ls)
	idx = BCNF_tf.index('False')   #gives index of 1st occurence
	attr_LHS = temp_attr_ls[idx] #=attr that violates BCNF...str
	Fd_LHS_ls = []
	Fd_RHS_ls = []
	step = 0
	for j in range(len(temp_fd_ls[0])):
		i = j = step
		if temp_fd_ls[0][i] == [attr_LHS]:
			remove = temp_fd_ls[0].pop(i)
			Fd_LHS_ls.append(remove)  #removes attr that violates BCFN from LHS
			remove = temp_fd_ls[1].pop(i)
			Fd_RHS_ls.append(remove)
			step = step + 1
	
	
	
	return temp_attr_ls, temp_fd_ls
	
	
	
def get_attr_closure(pot_superkey, Fds):
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
				if counter == len(Fds[0][i]) and Fds[1][i] not in closure: #=all attr on LHS in closure...so we can add RHS to closure
					closure.append(Fds[1][i])
			
		len_closure_after = len(closure)
		
	return closure


def choose_schema(attrDict):
	menu_header = ['\n','#'*65,'MENU'.center(63),'#'*65]
	for item in menu_header:
		print(item)
	schemas = list(attrDict.keys())
	for i in range(len(schemas)):
		print('%i- %s\n' %(i+1,schemas[i]))
	valid_input = False
	while valid_input == False:
		opt = input('Please enter a number to select one of the options listed above: ')
		valid_input = validate_menu_input(opt,len(attrDict))		
	schema_name = schemas[int(opt)-1]
	
	return schema_name


def validate_menu_input(inp,max_nr):
	if inp.isdigit():
		inp = int(inp)
		if inp > 0 and inp <= max_nr:
			return True
	print('Invalid input')
	return False


def main():
	path = './mini-project2-Example.sqliteDB'# './' + input('Please enter the name of the database file you would like to connect to: ')
	connectDB.connect(path) 
	attrDict, FdDict = readData()
	schema = choose_schema(attrDict) 
	
	
	BCNF_tf = ['False']
	temp_attr_ls = copy.copy(attrDict[schema])  #will update with each iteration...delete attr that we have removed from schema
	temp_fd_ls = copy.copy(FdDict[schema])  #will update with each iteration...delete fds that we have removed from schema
	
	while 'False' in BCNF_tf:
		BCNF_tf = check_if_superkey(temp_attr_ls, temp_fd_ls) #returning [False, False, True, False]
		temp_attr_ls,temp_fd_ls = decompose_schema(BCNF_tf,temp_attr_ls,temp_fd_ls)
		break ###
	
	

if __name__ == "__main__":
	main()

	
	
