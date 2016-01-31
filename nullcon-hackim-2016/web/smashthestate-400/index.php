<?php
$FAKE_DATABASE = array (
    "rob" => "60df0ab1a78fd0d95a4cfa4b0854931b", // smashthestate
    "admin" => "8e11a50ef762f924d7af9995889873e4",
);
$page = $_GET['page'];
 
switch ($page) {
    case "login":
        echo "trying to log in";
        $user = $_POST['user'];
        $pass = $_POST['pass'];
        if ($FAKE_DATABASE[$user] === md5($pass)) {
            session_start();
            session_regenerate_id(True);
            $_SESSION['user'] = $user;
            header("Location: ?page=upload");
            die();
        }
        else {
            header("Location: ?");
        }
        break;
    case "admin_login_help":
        session_start();
        if(!isset($_SESSION['login_code']) ){
            $_SESSION['login_code'] = bin2hex(openssl_random_pseudo_bytes(18));
            echo "A login code has been emailed to the administrator. Once you have recieved it, please click <a href='?page=code_submit'>here</a>\n";
        }
        else {
            echo "There is already an active login code for this session";
        }
        break;
    case "code_submit":
        session_start();
        $code = $_POST['code'];
        if (isset($code) && isset($_SESSION['login_code'])) {
            if ($code === $_SESSION['login_code'] ){
                echo "Flag: ";
                passthru("sudo /bin/cat /var/www/html/flag");
            }
            else {
                echo "Invalid code";
            }
        }
        else {
            echo "<html><form action='?page=code_submit' method='POST'>Please input the login code:<input name='code'/><input type='submit' value='submit'/></form>";
        }
        break;
    case "upload":
        session_start();
        if (!isset($_SESSION['user'])) {
            header("Location: ?");
        }
        else {
            echo "Welcome ".$_SESSION['user'] ." <button onclick='document.cookie=\"PHPSESSID=deleted\";location=\"?\"'>Logout</button><br/><br/>";
            echo "Use this form to verify zip integrity<br/><form action='?page=process_upload' method='post' enctype='multipart/form-data'><input type='file' name='zipfile'/><br/><br/><input type='submit' name='submit' value='Upload'/></form>";
        }
        break;
    case "process_upload":
        session_start();
        if (isset($_SESSION['user']) && $_FILES['zipfile']['name']) {
 
 
            if ($_FILES['zipfile']['size'] > 16000) {
                echo "File above max size of 10kb";
                echo "<br/><a href='?page=upload'>back</a>";
                break;
            }
            $tmp_file = '/var/www/html/tmp/upload_'.session_id();
 
            # ZipArchive may not be available
           # $zip = new ZipArchive;
           # $zip->open($_FILES['zipfile']['name']);
           # $zip->extractTo($tmp_file);
           exec('unzip -o '.$_FILES['zipfile']['tmp_name']. ' -d '.$tmp_file);
            echo "Zip contents: <br/>";
            passthru("cat $tmp_file/* 2>&1");
            exec("rm -rf $tmp_file");
            echo "<br/><br/><a href='?page=upload'>back</a>";
        }
        break;
    default:
        echo "<html><form action='?page=login' method='POST'>Username: <input name='user'/><br/>Password: <input type='password' name='pass'/><br/><input type='submit' value='Log in'/></form><a href='?page=admin_login_help'>Admin login help</a></html>";
        break;
}
 
?>