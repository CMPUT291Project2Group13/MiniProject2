

def main():
	set1 = ['{A,B,H}=>{E,G};', '{A}=>{D}']
	set = determination(set1)
	print(set)

def determination(set):
	result = []
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
	return result


if __name__ == "__main__":
	main()