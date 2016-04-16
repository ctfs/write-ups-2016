<?php
	$input = file_get_contents("php://input");
	$input = json_decode($input, true);
	if (!isset($input[0])) die();
	include("db_conn.php");
	sleep(1);
	$userid = mysql_real_escape_string($input[1]);
	$userps = mysql_real_escape_string($input[2]);
	if (strlen($userid)<4) die("minleng err");
	if (strlen($userps)<6) die("minleng err");
	$result = mysql_query("select md5('".$salt.$userps."')");
	$row = mysql_fetch_row($result);
	$userps = $row[0];
	$res = mysql_query("insert into users value (null, '{$userid}', '{$userps}')");
	if (mysql_error() != "") die("failed"); else die("success");
	
