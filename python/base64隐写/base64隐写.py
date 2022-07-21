from typing import TextIO


def inttobin(a, n):
    ret = bin(a)[2:]
    while len(ret) < n:
        ret = '0' + ret
    return ret


table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

f: TextIO = open("stego.txt", "r")
tmpbin = ''
res = ''
line = f.readline()
while line:
    if line[-2] == '=':
        if line[-3] == '=':
            tmpbin += inttobin(table.index(line[-4]), 6)[2:]
        else:
            tmpbin += inttobin(table.index(line[-3]), 6)[4:]
    line = f.readline()
quotient = len(tmpbin) // 8
for i in range(quotient):
    res += chr(int(tmpbin[8 * i:8 * i + 8], 2))
print(res)
