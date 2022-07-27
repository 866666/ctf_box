from load_file import *


def hex_shell(shell_path='./shell.php'):  # 将webshell转化为hex
    shell_var = loadfile(shell_path).encode('utf-8')
    return shell_var.hex()