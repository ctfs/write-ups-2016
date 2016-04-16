<?php
	session_start();
	if (isset($_GET['p'])) $page = $_GET['p']; else $page = "pages/home";
?><!DOCTYPE html>
<!-- Website template by freewebsitetemplates.com -->
<html>
<head>
	<meta charset="UTF-8">
	<title>Zerotype Website Template</title>
	<link rel="stylesheet" href="css/style.css" type="text/css">
	<script src="jquery-1.10.2.js"></script>
</head>
<body>
	<div id="header">
		<div>
			<div class="logo">
				<a href="./">Zero Type</a>
			</div>
			<ul id="navigation">
				<li class="active">
					<a href="?p=pages/home">Home</a>
				</li>
				<li>
					<a href="?p=pages/accounts">Accounts</a>
				</li>
				<?php if (isset($_SESSION['login'])) : ?>
				<?php if ($_SESSION['login'][1] == "admin") : ?>
				<li>
					<a href="?p=pages/admin">Admin</a>
				</li>
				<?php endif; ?>
				<li>
					<a href="?p=pages/mypage">MyPage</a>
				</li>
				<li>
					<a href="?p=pages/logout">Logout</a>
				</li>
				<?php else : ?>
				<li>
					<a href="?p=pages/reg">Register</a>
				</li>
				<li>
					<a href="?p=pages/login">Login</a>
				</li>
				<?php endif; ?>
			</ul>
		</div>
	</div>
<?php include($page.".php"); ?>
	<div id="footer">
		<div class="clearfix">
			<div id="connect">
				<a href="http://freewebsitetemplates.com/go/facebook/" target="_blank" class="facebook"></a><a href="http://freewebsitetemplates.com/go/googleplus/" target="_blank" class="googleplus"></a><a href="http://freewebsitetemplates.com/go/twitter/" target="_blank" class="twitter"></a><a href="http://www.freewebsitetemplates.com/misc/contact/" target="_blank" class="tumbler"></a>
			</div>
			<p>
				© 2023 Zerotype. All Rights Reserved.
			</p>
		</div>
	</div>
</body>
</html>
