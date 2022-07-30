# -*- coding: utf-8 -*-
# PHP弱类型比较 number == MD5(number)，MD5碰撞
# result:
# 0e215962017
# 0e291242476940776845150308577824

import hashlib


def md5vale(key):
    input_name = hashlib.md5()

    input_name.update(key.encode("utf-8"))

    return input_name.hexdigest()


a = 0
for i in range(20000000000000000):
    a += 1
flag = "0e" + str(a)

flag1 = md5vale(flag)

print(a)

if flag1[2:].isdigit():

    if flag1[0:2] == "0e":
        print(flag)

        print(flag1)

        exit()
