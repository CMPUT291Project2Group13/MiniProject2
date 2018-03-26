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


def remove_trivial_fd(FdDict):  
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
	# -checks if it's a superkey (if all attributes are in closure)
	closure = []
	BCNF = []
	superkey = False
	for i in range(len(Fds[0])):
		pot_superkey = copy.copy(Fds[0][i]) #using copy to not overwrite the list
		closure = get_attr_closure(pot_superkey, Fds)
		if len(superkey_closure) == len(closure):
			superkey = True
		else:
			superkey = False
		BCNF.append(superkey)   
		
		
		###returning a list like this [False, False, False, False, True, False, False, False, False]
		
	
	
	
	
	
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
				if counter == len(Fds[0][i]) and Fds[1][i] not in closure:
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
	
	
	####put this in a loop..
	check_if_superkey(attrDict[schema], FdDict[schema])
	
	
	

if __name__ == "__main__":
	main()

	