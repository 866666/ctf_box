import requests
import json
import re


def submit(ip, flag_text):  # 提交flag
    try:
        # 构造submit flag 参数
        submit_url = 'http://192.168.15.80:19999/api/flag'
        submit_header = {
            "Content-Type": "application/json;charset=utf-8",
            "Authorization": "1b1fae078083811a61e7794e8320755b",
        }
        # json格式化flag
        submit_data = json.dumps({"flag": flag_text})
        r = requests.post(submit_url, data=submit_data, headers=submit_header)
        submit_re = re.search(r'\"msg\"\:\".*\"', r.text).group()

        if submit_re.find('success') != -1:
            print('\033[0;32m[提交FLAG成功]\033[0m' +
                  ip + '-->' + submit_re)
        else:
            print('\033[0;31m[提交FLAG失败]\033[0m' +
                  ip + '-->' + submit_re)
    except Exception as e:
        print(
            '\033[1;35m[提交FLAG异常]\033[0m' + ip + '-->' + str(e))
        return False
