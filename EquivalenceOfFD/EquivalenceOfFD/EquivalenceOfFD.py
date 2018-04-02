import connectDB
import normalize

class EquivalenceOfFD:


	def _init_(self):
		self.EquivalenceOfFD()
		return

	def main(self):
		firstSet = []
		secondSet = []
		schemasSelectedOne = []	
		schemasSelectedTwo = []	
		superKeyOne = []
		superKeyTwo = []
		menuHeader = ['\n','#'*65,'MENU'.center(63),'#'*65]
		menuList = ['1- enter schema for F1 set\n','2- enter schema for F2 set\n', '3- confirm\n', '4- Exit\n']


		while True:
			for item in menuHeader:
				print(item)
			for item in menuList:
				print(item)	
			option = input('Please enter a number to select one of the options listed above:' )

			if option == '1':
				returnDataList, newSchemas, key = self.option(schemasSelectedOne)
				if returnDataList != None:
					superKeyOne.extend(key)
					print("Attributes: " + str(superKeyOne))
					schemasSelectedOne = newSchemas
					if not firstSet:
						firstSet = returnDataList
					else:		
						firstSet.extend(returnDataList)
					print("First set: " + str(firstSet))

			elif option == '2':
				returnDataList, newSchemas, key = self.option(schemasSelectedTwo)
				if returnDataList != None:
					superKeyTwo.extend(key)
					print("Attributes:" + str(superKeyTwo))
					schemasSelectedOne = newSchemas
					if not firstSet:
						secondSet = returnDataList
					else:		
						secondSet.extend(returnDataList)
					print("Second set: " + str(secondSet))

			elif option == '3':
				firstSet.sort()
				secondSet.sort()
				newSet1, key1 = self.determination(firstSet)
				newSet2, key2 = self.determination(secondSet)
				print("First set: " + str(newSet1))
				print("Second set: " + str(newSet2))

				if not newSet1:
					print("first set is empty")
					return
				if not newSet2:
					print("second set is empty")
					return
#				keyOne = str(superKeyOne).split(",")
#				keyTwo = str(superKeyTwo).split(",")
#				print("superkey one: " + str(keyOne) + "superkey two: "+ str(keyTwo))
				print("key1" + str(key1))
				print("key2" + str(key2))
				firstClosure = normalize.get_attr_closure(key1, newSet2)
				secondClosure = normalize.get_attr_closure(key2, newSet1)
				print("First closure: "+ str(firstClosure))
				print("Second closure: " + str(secondClosure))
				if firstClosure == secondClosure:
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

		schemas = input("please choose the schemas: ")
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

		return newList, schemasSelected, attributes

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
