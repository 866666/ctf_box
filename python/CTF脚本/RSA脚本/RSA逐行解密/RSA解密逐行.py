import gmpy2

N, p, q, e = 920139713, 18443, 49891, 19  # 首先N分解得出p,q
d = gmpy2.invert(e, (p - 1) * (q - 1))
result = []

with open("C:\\Users\\shang\\PycharmProjects\\pythonProject\\data.txt", "r") as f:
    for line in f.readlines():
        line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        result.append(chr(pow(int(line), d, N)))

for i in result:
    print(i, end='')
