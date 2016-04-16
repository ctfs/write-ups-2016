<?php
    include "./lib/lib.php";

    $id = $_GET['id'];

    $que = "select id, datetime, writer, type, title, contents from blog where id='$id'";
    $result = mysql_query($que);
    $row = mysql_fetch_array($result);

    if($row['writer'] == "Admin") // I know... it sucks... but you can bypass right :) ?
    {
        echo("<script>alert('You are not allowed to read this post.');history.back();</script>");
        exit();
    }
?>

<!DOCTYPE html >
<!--  Website template by freewebsitetemplates.com  -->
<html>

<head>
    <title>BLOG</title>
    <meta  charset="iso-8859-1" />
    <link href="css/style.css" rel="stylesheet" type="text/css" />
    <!--[if IE 6]>
        <link href="css/ie6.css" rel="stylesheet" type="text/css" />
    <![endif]-->
    <!--[if IE 7]>
        <link href="css/ie7.css" rel="stylesheet" type="text/css" />  
    <![endif]-->
</head>

<body>
    <div id="background">
        <div id="page">
            <div class="header">
                <div class="footer">
                    <div class="body">
                        <div id="sidebar">
                            <a href="index.php"><img id="logo" src="images/logo.gif" with="154" height="74" alt="" title=""/></a>
                            <ul class="navigation">
                                <li><a href="index.php">HOME</a></li>
                                <li><a href="about.php">ABOUT</a></li>
                                <li class="active"><a href="blog.php">BLOG</a></li>
                                <li class="last"><a href="login.php">LOGIN</a></li>
                            </ul>
                            <div class="connect">
                                <a href="#" class="facebook">&nbsp;</a>
                                <a href="#" class="twitter">&nbsp;</a>
                                <a href="#" class="vimeo">&nbsp;</a>
                            </div>
                    
                            <div class="footenote">
                                <span>&copy; Copyright &copy; 2011.</span>
                                <span><a href="index.php">Company name</a> all rights reserved</span>
                            </div>
                        </div>
                        <div id="content">
                            <div class="content" style="height:500px;">
                                <ul>
                                    <li>
                                        <h2><?=$row['title']?></h2>
                                        <p><?=$row['datetime']?>, <?=$row['writer']?></p>
                                        <p><?=$row['contents']?></p>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="shadow"></div>
        </div>
    </div>
</body>
</html>
