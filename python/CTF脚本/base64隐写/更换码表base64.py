import base64
import string

b64table_xor = '(RBYTP[FG@QEUWDAZKMVINJHLOS32:1;04756rbytp{fg`qeuwdazkmvinjhlos,'
b64table = ''

for i in range(len(b64table_xor)):
    b64table += chr(ord(b64table_xor[i]) ^ 3)

b64text = 'Lat7LudgOb1tO6L5VNybVaJjFUYbTb1cOIDuL4yuLZ75VaL7Tb5gT67l'
b64oritable = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

print(base64.b64decode(b64text.translate(str.maketrans(b64table, b64oritable))))