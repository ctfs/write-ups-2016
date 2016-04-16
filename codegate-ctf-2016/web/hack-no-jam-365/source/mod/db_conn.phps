<?php
	mysql_connect("localhost", "bughela", "backsu");
	mysql_select_db("cgwebv");
	$salt = md5(file_get_contents("/etc/passwd"));
