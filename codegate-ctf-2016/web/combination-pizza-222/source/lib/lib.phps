<?php
    $connect = mysql_connect('localhost', 'blog', 'sbsbdjfma') or die('DB connect fail');
    mysql_select_db('blog_db', $connect);
?>
