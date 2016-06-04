<?php
session_start();
if (!isset($_SESSION['user'])) {
    header('Location: /');
    exit();
}
if (isset($_POST['code'])) {
    $code = $_POST['code'];
    exec('python3 ../runapi.py ' . escapeshellarg($_POST['code']), $output, $ret);
    echo json_encode(array('output' => implode("\n", $output)));
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
        <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.2.2/ace.js"></script>
        <script src="/js/script.js"></script>
        <script src="/js/editor.js"></script>
        <style>.ace_editor {min-height:300px}</style>
    </head>
    <body>
        <div id="container">
            <h1>Java Sandbox</h1>
            <form class="form" action="editor.php?run" method="POST">
                <h2>Run Java Code</h2>
                <div class="alert" style="display:none"></div>
                <div class="form-group">
                    <div id="editor"></div>
                    <pre id="template" style="display:none">/* package whatever; // don't place package name! */

import java.util.*;
import java.lang.*;

public class Main
{
    public static void main (String[] args) throws java.lang.Exception
    {
        // your code goes here
    }
}</pre>
                    <textarea class="form-control" name="code" id="code"></textarea>
                </div>
                <input type="submit" value="Run Code" class="btn btn-primary" /><input type="button" value="Reset Code" class="btn btn-danger pull-right" id="reset-code" />
                <pre id="output" style="background-color:#eee;margin-top:15px;padding:5px;margin-bottom:0px">Press "Run Code" to run your code.</pre>
            </form>
            <div style="text-align:center;margin-bottom:15px"><a href="/index.php?logout">Logout</a> - <a href="/info.php">Sandbox Information</a></div>
        </div>
    </body>
</html>
