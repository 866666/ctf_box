<?php
class Flag{//flag.php
    public $file='flag.php';
}
$f = new Flag();
$t = serialize($f);
echo $t;
?>