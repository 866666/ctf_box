#!/usr/bin/env python
# -*- coding:utf-8 -*-
# --生成攻击hosts列表--

ip_header = '192.168.15'
ip_start = 101
ip_end = 110
port_start = 8081
port_end = 8088
white_list = '192.168.15.102:8082'  # 白名单
with open('init_hosts.txt', 'w') as file:  # 清空旧文件
    file.truncate(0)
for ip_x in range(ip_start, ip_end):
    for port_x in range(port_start, port_end):
        ip = ip_header + '.' + str(ip_x) + ':' + str(port_x)
        if ip != white_list:
            with open('init_hosts.txt', 'a') as file:
                file.write(ip + '\n')
            print(ip)
        else:
            print('white_list IP:' + ip)
