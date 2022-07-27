import sys

def loadfile(filepath):
    try:
        file = open(filepath, "r")
        return str(file.read())
    except:
        print("找不到文件：" + filepath)
        sys.exit()
