import connectDB

def read_tables():
	# -reads data from tables in the database 
	# -creates 2 dictionaries (one for the list of attributes, one for the FDs)
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
		FdDict[item[0]] = [LHS,RHS]  
	FdDict = decompose_RHS(FdDict)
	return attrDict, FdDict


def decompose_RHS(FdDict):
	# -splits up attributes on RHS
	# -returns the updated dictionary
	for key in FdDict:
		step = 0
		for i in range(len(FdDict[key][1])):
			j = i + step  #to account for change of len(FdDict[key]) after each iteration
			if len(FdDict[key][1][j]) > 1:
				RhsAttr = FdDict[key][1].pop(j)   
				LhsAttr = FdDict[key][0].pop(j)
				NrOfAttr = len(RhsAttr)
				step = step + NrOfAttr - 1 
				for idx in range(len(RhsAttr)):
					FdDict[key][0].insert(j+idx,LhsAttr)
					FdDict[key][1].insert(j+idx,RhsAttr[idx])
			else:
				FdDict[key][1][j] = ''.join(FdDict[key][1][j])   
	return FdDict

def validate_menu_input(inp,max_nr):
	# -checks if input is a number and within allowed range
	# -returns boolean
	if inp.isdigit():
		inp = int(inp)
		if inp > 0 and inp <= max_nr:
			return True
	print('Invalid input')
	return False
