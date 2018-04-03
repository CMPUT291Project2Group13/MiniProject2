import readData
import normalize
import time
import copy


def get_closure(attrDict,FdDict):
	cont = True
	FDLHS = []
	FDRHS = []
	while cont == True:
		schema_name = choose_schema(attrDict)
		if schema_name == 'stop':
			cont = False
		else: 
			fd_ls = copy.deepcopy(FdDict[schema_name])
			FDLHS = FDLHS + fd_ls[0]
			FDRHS = FDRHS + fd_ls[1]
	FDs = [FDLHS,FDRHS]
	attr_ls = choose_attributes()
	closure = normalize.get_attr_closure(attr_ls,FDs)
	closure.sort()
	attr_ls.sort()
	attr_str = ','.join(attr_ls)
	closure_str = ','.join(closure)
	print(closure)
	print_str = 'The attribute closure of {' + attr_str + '} is {' + closure_str + '}'
	print(print_str)
	time.sleep(2.5)
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
		opt = input("Please enter a number to select the next schema or enter 'stop' to move on to the next step: ")
		if opt == 'stop':
			valid_input = True
			return opt
		if len(opt) == 0:
			valid_input == False
		else: 
			valid_input = readData.validate_menu_input(opt,len(attrDict))
	schema_name = schemas[int(opt)-1]
	return schema_name


def choose_attributes():
	valid_input = False
	while valid_input == False:
		attr = input('Please enter a set of attributes separated by commas (eg A,B,C): ')
		if len(attr) > 0:
			valid_input = True
			attr_ls = attr.split(',')
			return attr_ls
		else:
			print('invalid input')
	

			
