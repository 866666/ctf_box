# -*- coding: utf-8 -*-
import os
import base64
with open("jpg.txt", "r") as f:
    imgdata = base64.b64decode(f.read())
file = open('jpg.jpg', 'wb')
file.write(imgdata)
file.close()
