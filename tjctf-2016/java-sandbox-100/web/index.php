<?php
if (isset($_GET['logout'])) {
    session_start();
    session_destroy();
    header('Location: /');
    exit();
}

function res($msg) {
    echo json_encode(array('error' => $msg));
    exit();
}

function generatePassword($length = 16) {
    $chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    $count = strlen($chars);

    for ($i = 0, $result = ''; $i < $length; $i++) {
        $index = rand(0, $count - 1);
        $result .= substr($chars, $index, 1);
    }

    return $result;
}

function check($user, $pass) {
    try {
        $db = new SQLite3(':memory:');
        $db->query('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)');
        $us = array('admin', 'user', 'member', 'bob');
        foreach ($us as $u) {
            $db->query("INSERT INTO users (username, password) SELECT '" . $u . "', '" . generatePassword() . "' WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = '" . $u . "')");
        }
        if (strlen($user) > 32 || strlen($pass) > 32) {
            res('Username or password too long!');
        }
        $res = $db->query("SELECT COUNT(*) FROM users WHERE username = '$user' AND password = '$pass'");
        if (!$res) {
            res('SQL Error: ' . $db->lastErrorMsg());
        }
        $row = $res->fetchArray();
        return $row[0] != 0;
    }
    catch (Exception $e) {
        res('Error: ' . $e->getMessage());
        error_log($e);
    }
}

if (isset($_POST['username']) && isset($_POST['password'])) {
    $user = $_POST['username'];
    $pass = $_POST['password'];
    if (!extension_loaded('sqlite3')) {
        res('SQLite3 is not installed on the server!<br />Please contact a CTF organizer.');
    }
    if (!check($user, $pass)) {
        echo json_encode(array('error' => 'Wrong username or password!', 'clippy' => 'It looks like you\'re having trouble logging in. Perhaps you could try <a href="https://en.wikipedia.org/wiki/SQL_injection">SQL Injection</a>?'));
        exit();
    }
    session_start();
    $_SESSION['user'] = $user;
    echo json_encode(array('redirect' => '/editor.php'));
    exit();
}
?>
<!doctype html>
<html>
    <head>
        <title>Java Sandbox</title>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
        <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.0.0-alpha/css/bootstrap.min.css">
        <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.4.0/css/font-awesome.min.css">
        <link rel="stylesheet" type="text/css" href="/css/style.css">
        <script src="/js/script.js"></script>
    </head>
    <body>
        <div id="container">
            <h1>Java Sandbox</h1>
            <form class="form" action="index.php" method="POST">
                <h2>Login</h2>
                <div class="alert" style="display:none"></div>
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" name="username" id="username" class="form-control" />
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" name="password" id="password" class="form-control" />
                </div>
                <input type="submit" class="btn btn-primary" value="Login" />
            </form>
            <div class="form">
                <h2>Registration</h2>
                <div class="alert alert-warning"><b>Java Sandbox is in closed beta!</b><br />You can gain access if you ask a friend to invite you.</div>
            </div>
            <div id="clippy"><span></span><img src="images/clippy.png" /></div>
        </div>
    </body>
</html>
