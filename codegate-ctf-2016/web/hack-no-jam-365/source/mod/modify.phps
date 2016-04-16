<?php
	include("./db_conn.php");

	$input = file_get_contents("php://input");
	$input = json_decode($input, true);
	if (strlen($input[2])<6) die("minleng err");
	if (strlen($input[3])<6) die("minleng err");
	sleep(1);
	$input[2] = myhash($input[2]);
	$input[3] = myhash($input[3]);
	if (update_userpass($input)) {
		die("success");
	} else {
		die("authenticate failed..");
	}

	function myhash($v){
		global $salt;
		return md5($salt.$v);
	}

	function get_userdata($userid){
		$userid = mysql_real_escape_string($userid);
		$result = mysql_query("select * from users where userid = '{$userid}'");
		$row = mysql_fetch_row($result);
		return $row;
	}

	function authenticate($input){
		$userdata = get_userdata($input[1]);
		if ($input===$userdata) return true;
		return false;
	}

	function update_userpass($input){
		$change = $input[3];
		array_pop($input);
		if (!authenticate($input)) return false;
		$input[0] = mysql_real_escape_string($input[0]);
		mysql_query("update users set userps='{$change}' where uidx='{$input[0]}'");
		return true;
	}
?>
