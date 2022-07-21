import matplotlib.pyplot as plt
import numpy as np

with open('hex.txt', 'r') as h:
    h = h.read()
with open('ascii.txt', 'a') as a:
    for i in range(0, len(h), 2):
        tmp = '0x' + h[i] + h[i + 1]
        tmp = int(tmp, base=16)
        if chr(tmp) != '(' and chr(tmp) != ')':
            a.write(chr(tmp))

x, y = np.loadtxt('./ascii.txt', delimiter=',', unpack=True)
plt.plot(x, y, '.')
plt.show()
