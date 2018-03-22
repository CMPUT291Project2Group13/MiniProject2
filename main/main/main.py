import sqlite3
import connectDB



def readData():
	connectDB.c.execute('''SELECT Name,Attributes FROM InputRelationSchemas''')
	attributes = connectDB.c.fetchall()
	attrDict = {}
	for item in attributes:
		attrDict[item[0]] = item[1]
	print(attrDict)

	connectDB.c.execute('''SELECT Name,FDs FROM InputRelationSchemas''')
	FDs = connectDB.c.fetchall()
	FdDict = {}
	for item in FDs:
		FdDict[item[0]] = item[1]
	print(FdDict)

def main():
	path = './mini-project2-Example.sqliteDB'# './' + input('Please enter the name of the database file you would like to connect to: ')
	connectDB.connect(path) 
	
	readData()



if __name__ == "__main__":
	main()

