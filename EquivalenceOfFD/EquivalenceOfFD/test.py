

def main():
	set1 = ['{A,B,H}=>{E,G};', '{A}=>{D};', '{A}=>{c}']
	set, key = determination(set1)
	print(set)
	print(key)

def determination(set):
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
		lhsStr = lhsStr.replace(",", "")
		lhsList.append(lhsStr)

	for i in lhsList:
		if i in check:
			continue
		else:
			check.append(i)

	return result, check


if __name__ == "__main__":
	main()