import connectDB

class EquivalenceOfFD:


	def _init_(self):
		self.EquivalenceOfFD()
		return

	def main(self):
		firstSet = []
		secondSet = []
		schemasSelectedOne = []	
		schemasSelectedTwo = []	
		menuHeader = ['\n','#'*65,'MENU'.center(63),'#'*65]
		menuList = ['1- enter schema for F1 set\n','2- enter schema for F2 set\n', '3- confirm\n', '4- Exit\n']


		while True:
			for item in menuHeader:
				print(item)
			for item in menuList:
				print(item)	
			option = input('Please enter a number to select one of the options listed above:' )

			if option == '1':
				returnDataList, newSchemas = self.option(schemasSelectedOne)
				print(returnDataList)
				schemasSelectedOne = newSchemas
				if returnDataList != None:
					if not firstSet:
						print("firstSet empty")
						firstSet = returnDataList
					else:		
						firstSet.extend(returnDataList)
					print("first set")
					print(firstSet)

			elif option == '2':
				returnDataList, newSchemas = self.option(schemasSelectedTwo)
				print(returnDataList)
				schemasSelectedOne = newSchemas
				if returnDataList != None:
					if not firstSet:
						print("secondSet empty")
						secondSet = returnDataList
					else:		
						secondSet.extend(returnDataList)
					print("second set")
					print(secondSet)

			elif option == '3':
				firstSet.sort()
				print(firstSet)
				secondSet.sort()
				print(secondSet)
				if not firstSet:
					print("first set is empty")
					return
				if not secondSet:
					print("second set is empty")
					return

				if set(secondSet) == set(firstSet):
					print("Two sets are equivalent")
					return
				else:
					print("Two sets are not equivalent")
					return
			elif option == '4':
				break
			else:
				print("invalid input")
				return

	def option(self, schemasSelected):
		print("please choose from the following schemas")
		connectDB.c.execute('''SELECT name 
								FROM InputRelationSchemas ''')
		data =  connectDB.c.fetchall()
		print(data)

		schemas = input("please choose the schemas(splite by comma): ")
		if schemas in schemasSelected:
			print("The schema is already in selection")
			return None, schemasSelected
		schemasSelected.append(schemas)
		schemaList = schemas.split(",")
		for item in schemaList:
			connectDB.c.execute('''SELECT I.FDs 
									FROM InputRelationSchemas  I
									WHERE I.name = :item''',{"item":item})
			data =  connectDB.c.fetchall()
			if not data:
				print ("invalid input")
				schemasSelected.remove(schemas)
				return None, schemasSelected

			dataList = []
			for i in data[0]:
				dataList.append(i)
			print(dataList)
			newString = "".join(str(x) for x in dataList)
			newList = newString.split()
			print(newList)

		return newList, schemasSelected
