import string

str = "100888210610071905578878610699109864888508912081681081029071571029810957488812286111817274108102816161"

i = 0
j = 0
flag = ''
print(len(str))
while i < len(str):
    j = i + 3
    if int(str[i:j]) < 128:
        flag += chr(int(str[i:j]))
        i += 3
        print(flag)
    else:
        j = i + 2
        flag += chr(int(str[i:j]))
        i += 2
        print(flag)
