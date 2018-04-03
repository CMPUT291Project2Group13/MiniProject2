import sqlite3
import connectDB
import copy 
import sys
import time
import readData
import normalize
import fill_table
import EquivalenceOfFD

####delete the delete command in write_to_output before submitting!!
####################################################################

def main_menu():
	# -displays options and asks user to choose one
	# -returns the option the user has chosen as a str
	menu_header = ['\n','#'*65,'MENU'.center(63),'#'*65]
	menu_ls = ['1- Normalize schema\n','2- Compute attribute closure\n', '3- Check equivalence of 2 sets of functional dependencies\n', '4- Exit\n']
	for item in menu_header:
		print(item)
	for item in menu_ls:
		print(item)
	valid_input = False
	while valid_input == False:
		opt = input('Please enter a number to select one of the options listed above: ')
		valid_input = readData.validate_menu_input(opt,len(menu_ls))
	return opt


def exit_program():
	# -disconnects from database and exits the program
	print('\nDisconnecting...')
	time.sleep(1.5)	
	connectDB.disconnect()
	sys.exit()
	
	
def main():
	path = './mini-project2-Example.sqliteDB'# './' + input('Please enter the name of the database file you would like to connect to: ')
	connectDB.connect(path) 
	attrDict, FdDict = readData.read_tables()
	
	exit = False
	while exit == False: 
		opt = main_menu()
		if opt == '1':			
			normalize.normalize_schema(attrDict,FdDict)		
		#elif opt == '2':
			#get attribute closure
		elif opt == '3':
			newList = copy.copy(FdDict["Person"])
			E = EquivalenceOfFD.EquivalenceOfFD()
			E.main(FdDict)
		elif opt == '4':
			exit_program()

if __name__ == "__main__":
	main()
