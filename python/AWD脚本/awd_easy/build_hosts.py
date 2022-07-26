#!/usr/bin/env python
# -*- coding:utf-8 -*-
# --生成攻击hosts列表--
import os
import time
ip_header = '172.20'
ip_start = 110
ip_end = 133
port_start = 80
port_end = 81
white_list = '172.20.110.101'  # 白名单
if os.path.exists('host_list.txt'):  # 重命名旧文件
    get_time = time.strftime(
        "%Y-%m-%d_%H_%M_%S", time.localtime(os.path.getmtime('host_list.txt')))
    old_name = 'host_list_' + str(get_time) + '.txt'
    try:
        os.rename('host_list.txt', old_name)
    except Exception as e:
        print('Rename file fail:'+str(e))
    else:
        print('Rename file success:' + old_name)
with open('host_list.txt', 'w') as file:
    file.truncate(0)
for ip_x in range(ip_start, ip_end):
    for port_x in range(port_start, port_end):
        ip = ip_header + '.' + str(ip_x) +'.101'+':'+str(port_x) 
        if ip != white_list:
            with open('host_list.txt', 'a') as file:
                file.write(ip+'\r')
            print(ip)
        else:
            print('white_list IP:' + ip)
