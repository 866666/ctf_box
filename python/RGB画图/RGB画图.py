from PIL import Image
import os

# os.chdir(
#     r'C:\xxx\attachment (4)\0573\0114\0653\0234\0976\0669\0540\0248\0275\0149\0028\0099\0894\0991\0414\0296\0241\0914')
string = ''

file = open('qr.txt')
MAX = 200

picture = Image.new("RGB", (MAX, MAX))
for y in range(MAX):
    for x in range(MAX):
        string = file.readline()
        picture.putpixel([x, y], eval(string))  # 直接使用eval()可以转为元组
picture.show()
