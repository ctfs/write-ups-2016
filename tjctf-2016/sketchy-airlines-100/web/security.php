<!doctype html>
<html>
    <head>
        <title>Sketchy Airlines</title>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
        <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.0.0-alpha/css/bootstrap.min.css">
        <link rel="stylesheet" type="text/css" href="/css/style.css">
        <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.4.0/css/font-awesome.min.css">
        <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/highlight.js/8.9.1/styles/default.min.css">
        <script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/8.9.1/highlight.min.js"></script>
        <script>hljs.initHighlightingOnLoad();</script>
    </head>
    <body>
        <div id="content">
            <div id="logo" class="clearfix">
                <svg width="64" height="64" style="float:left">
                    <image xlink:href="images/sketchyairlines.svg" src="images/sketchyairlines.png" width="64" height="64" />
                </svg>
                <h1 style="font-size:64px;float:left"><span style="color:#ff6600">Sketchy</span><span style="color:#28170b">Airlines</span></h1>
            </div>
            <div class="body">
                <hr />
                <h3 style="text-align:center">Our Security Policies</h3>
                <p>We have a unique login system here at <span style="color:#ff6600">Sketchy</span><span style="color#28170b">Airlines</span>. You can see part of our login code below:</p>
                <pre style="font-size:13px"><code class="php"><?php echo htmlspecialchars(file_get_contents("function.php")); ?></code></pre>
                <p><b>What if someone guesses your secret key?</b></p>
                <p>Impossible! Our secret key is 16 characters long.</p>
                <hr />
                <h5 style="text-align:center"><a href="/">Go Back</a></h5>
            </div>
        </div>
    </body>
</html>
