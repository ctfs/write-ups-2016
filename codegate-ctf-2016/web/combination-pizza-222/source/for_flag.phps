<?php
    $flag_connect = mysql_connect('localhost', 'for_flag', 'almost_there!!') or die('DB connect fail');
    mysql_select_db('flag_db', $flag_connect);

    $flag_que = "select flag from flag_table";
    $flag_result = mysql_query($flag_que);
    $flag_row = mysql_fetch_array($flag_result);

    $flag = $flag_row['flag'];
?>
