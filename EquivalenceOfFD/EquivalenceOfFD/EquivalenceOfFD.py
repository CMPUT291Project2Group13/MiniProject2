import connectDB
import normalize
import copy

class EquivalenceOfFD:


	def _init_(self):
		self.main()
		return

	def main(self, FdDict):
		firstSet = []
		secondSet = []
		leftSet = []
		rightSet = []
		schemasSelectedOne = []	
		schemasSelectedTwo = []	
		superKeyOne = []
		superKeyTwo = []
		firstSetSchemas = []
		secondSetSchemas = []
		menuHeader = ['\n','#'*65,'MENU'.center(63),'#'*65]
		menuList = ['1- enter schema for F1 set\n','2- enter schema for F2 set\n', '3- confirm\n', '4- Exit\n']


		while True:
			for item in menuHeader:
				print(item)
			for item in menuList:
				print(item)	
			option = input('Please enter a number to select one of the options listed above:' )

			if option == '1':
				returnDataList, newSchemas, choice = self.option(schemasSelectedOne)
				if returnDataList == None:
					return
				else:
					firstSetSchemas.append(choice)
					schemasSelectedOne = newSchemas
					if not firstSet:
						firstSet = returnDataList
					else:		
						firstSet.extend(returnDataList)
					print("First set: " + str(firstSet))

			elif option == '2':
				returnDataList, newSchemas, choice = self.option(schemasSelectedTwo)
				if returnDataList == None:
					return
				else:
					secondSetSchemas.append(choice)
					schemasSelectedOne = newSchemas
					if not firstSet:
						secondSet = returnDataList
					else:		
						secondSet.extend(returnDataList)
					print("Second set: " + str(secondSet))

			elif option == '3':
				firstSet.sort()
				secondSet.sort()
				setOneList = []
				setTwoList = []
				newSet1, key1 = self.determination(firstSet)
				newSet2, key2 = self.determination(secondSet)
				list(set(firstSetSchemas))
				list(set(secondSetSchemas))

				for item in firstSetSchemas:
					setOneList.append(copy.copy(FdDict[item]))
				for item in secondSetSchemas:
					setTwoList.append(copy.copy(FdDict[item]))
				index = 0
				for newList in setOneList:
					subIndex = 0
					for item in newList[0]:
						closure = normalize.get_attr_closure(item, setTwoList[index])
						if newList[1][subIndex] not in closure:
							print("Sets are not equivalent")
							return
						subIndex = subIndex + 1
					index = index + 1

				index = 0
				for newList in setTwoList:
					subIndex = 0
					for item in newList[0]:
						closure = normalize.get_attr_closure(item, setOneList[index])
						if newList[1][subIndex] not in closure:
							print("Sets are not equivalent")
							return
						subIndex = subIndex + 1
					index = index + 1
				print("Sets are equivalent")	

			elif option == '4':
				break
			else:
				print("invalid input")
				return

	def option(self, schemasSelected):
		print("please choose from the following schemas")
		connectDB.c.execute('''SELECT name 
								FROM InputRelationSchemas ''')
		names =  connectDB.c.fetchall()

		print(names)

		schemas = input("please choose the schemas: ")


		if schemas in schemasSelected:
			print("The schema is already in selection")
			return None, schemasSelected, None
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
				return None, schemasSelected, None

			dataList = []
			for i in data[0]:
				dataList.append(i)
			newString = "".join(str(x) for x in dataList)
			newList = newString.split()

		connectDB.c.execute('''SELECT I.attributes 
								FROM InputRelationSchemas I
								WHERE I.name = :name''',{"name":schemas})
		attributes =  connectDB.c.fetchall()

		return newList, schemasSelected, schemas

	def determination(self, set):
		result = []
		lhsList = []
		check = []

		for item in set:
			wrapper = []
			lhs = []
			rhs = []
			item = item.replace("{","")
			item = item.replace("}","")
			item = item.replace(";","")
			twoSideList = item.split("=>")
			lhs = twoSideList[0].split(",")
			rhs = twoSideList[1].split(",")
			wrapper = [lhs, rhs]
			result.append(wrapper)
			lhsStr = str(twoSideList[0])
#			lhsStr = lhsStr.replace(",", "")  #if dont need comma, take comment sign out
			lhsList.append(lhsStr)

		for i in lhsList:
			if i in check:
				continue
			else:
				check.append(i)

		return result, check

