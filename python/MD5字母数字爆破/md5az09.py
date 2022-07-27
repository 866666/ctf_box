import sys
import hashlib


def loadfile(filepath):
    try:
        file = open(filepath, "r")
        return str(file.read())
    except:
        print("找不到文件：" + filepath)
        sys.exit()


def MD5_demo(str):
    md = hashlib.md5()  # 创建md5对象
    md.update(str.encode(encoding='utf-8'))
    return md.hexdigest()


if __name__ == '__main__':
    md5_txt = loadfile('./md5s.txt')
    md5_list = md5_txt.split('_')
    flag = ''
    for i in md5_list:
        for j in range(32, 128):
            if i == MD5_demo(chr(j)):
                flag += chr(j)
            else:
                continue

    print(flag)
