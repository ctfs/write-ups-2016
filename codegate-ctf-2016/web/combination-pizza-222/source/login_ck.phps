<?php
    include "./lib/for_flag.php";
    include "./lib/lib.php";

    $user = mysql_real_escape_string($_POST['user']);
    $pass = mysql_real_escape_string($_POST['pass']);
    $token = $_POST['token'];

    $que = "select user from login where user='{$user}' and pass=md5('{$pass}')";
    $result = mysql_query($que);
    $row = mysql_fetch_array($result);

    if($row['user'] == 'Admin')
    {
        if(md5("blog".$token) == '0e689047178306969035064392896674')
        {
            echo "good job !!!<br />FLAG : <b>".$flag."</b>";
        }
        else
        {
            echo "Incorrect Token";
        }
    }
    else
    {
        echo "Incorrect ID or Password";
    }
?>
