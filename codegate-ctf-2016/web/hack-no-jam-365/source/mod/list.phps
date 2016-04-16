<?php
	include("./db_conn.php");

	$result = mysql_query("select uidx,userid from users order by uidx asc");
	$list = [];
	while($row = mysql_fetch_row($result)) :
		$row[1] = htmlentities($row[1]);
		$list[] = $row;
	endwhile;

	header('Content-type: application/json');
	die(json_encode($list));
