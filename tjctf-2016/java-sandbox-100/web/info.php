<?php
session_start();
if (!isset($_SESSION['user'])) {
    header('Location: /');
    exit();
}
if (isset($_GET['code'])) { ?>
<!doctype html>
<html>
<head>
    <title>Java Sandbox</title>
    <script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/8.9.1/highlight.min.js"></script>
    <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/highlight.js/8.9.1/styles/default.min.css">
    <script>hljs.initHighlightingOnLoad();</script>
    <style>html,body,pre{padding:0px;margin:0px}</style>
</head>
<body>
    <pre><code class="java"><?php echo htmlspecialchars(file_get_contents("../Wrapper.java")); ?></code></pre>
</body>
</html>
<?php exit(); } ?>
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
            <div class="form">
                <h3>About The Sandbox</h3>
                <p>Your code is sandboxed using the Java security manager. You can see the class loader code <a href="info.php?code">here</a> to see what you can and can't use.</p>
            </div>
            <div class="form">
                <h3>3rd Party Libraries</h3>
                <p>We have recently added support for third party libraries! Just import the library and we'll configure the classpath. You can see the ones you are allowed to use below:</p>
                <table class="table">
                    <thead>
                        <tr><th>Library</th><th>Version</th><th>Link</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Google Gson</td><td>2.4</td><td>(Removed)</td></tr>
                        <tr><td>Twitter4J</td><td>4.0.4</td><td>(Removed)</td></tr>
                        <tr><td>Secure File Downloader</td><td>1.0</td><td><a href="libs/downloader-1.0.jar">Download</a></td></td></tr>
                    </tbody>
                </table>
            </div>
            <div class="form">
                <h3>Looking for a flag?</h3>
                <p>The flag is located in <b><?php echo realpath(__DIR__ . '/../flag.txt'); ?></b>.<br />You don't have filesystem access though. :(</p>
            </div>
            <div style="text-align:center;margin-bottom:15px"><a href="/editor.php">Back</a></div>
        </div>
    </body>
</html>
