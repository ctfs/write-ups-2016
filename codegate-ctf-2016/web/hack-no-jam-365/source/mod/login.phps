<?php session_start();
	$input = file_get_contents("php://input");
	$input = json_decode($input, true);
	if (!isset($input[0])) die();
	sleep(1);
	include("db_conn.php");
	$userid = mysql_real_escape_string($input[1]);
	$userps = mysql_real_escape_string($input[2]);
	if (strlen($userid)<4) die("minleng err");
	if (strlen($userps)<6) die("minleng err");
	$result = mysql_query("select md5('".$salt.$userps."')");
	$row = mysql_fetch_row($result);
	$userps = $row[0];
	$result = mysql_query("select * from users where userid='{$userid}' and userps='{$userps}'");
	$row = mysql_fetch_row($result);
	if ($row[0] != "") {
		$_SESSION['login'] = $row;
		die("success");
	}
	die("failed");
