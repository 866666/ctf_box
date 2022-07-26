import sys
def loadfile(filepath):
	try : 
		file = open(filepath,"rb")
		return str(file.read())
	except : 
		print("找不到文件："+ filepath)
		sys.exit()


if __name__ == '__main__':
	while True:
		ms = raw_input("Attack Method > ")
		shellstr=loadfile("./webshell.txt")
		list = shellstr.split("\r\n")
		#print str(list)
		i = 0
		url={}
		passwd={}
		method={}