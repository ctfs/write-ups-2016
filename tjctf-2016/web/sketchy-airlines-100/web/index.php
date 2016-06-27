<!doctype html>
<html>
    <head>
        <title>Sketchy Airlines</title>
        <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" />
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
        <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.0.0-alpha/css/bootstrap.min.css">
        <link rel="stylesheet" type="text/css" href="/css/style.css">
        <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.4.0/css/font-awesome.min.css">
<script>
$(document).ready(function() {
    $("#lookup-flight").submit(function(e) {
        e.preventDefault();
        $("#info").slideUp('fast');
        $.post($(this).attr("action"), $(this).serialize(), function(data) {
            if (data.error) {
                $("#info").text(data.error).slideDown('fast');
            }
            else {
                window.location.href = data.redirect;
            }
        }, 'json');
    });
});
</script>
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
                <h3 style="text-align:center"><a href="#">Travel Info</a> - <a href="#">Book A Flight</a></h3>
                <hr />
                <p style="font-size:15px;text-align:center"><span style="color:#ff6600">Sketchy</span><span style="color:#28170b">Airlines</span> is an air transportation service. Why should you use us?</p>
                <div class="row" style="text-align:center">
                    <div class="col-md-4"><div class="fa fa-plane" style="font-size:48px"></div><br /><span style="color:#ff6600">Sketchy</span><span style="color:#28170b">Airlines</span> guarantees fast, efficient, and comfortable travel!</div>
                    <div class="col-md-4"><div class="fa fa-lock" style="font-size:48px"></div><br />We use cutting edge <b>Base64 encryption</b> to keep your credit cards secure!</div>
                    <div class="col-md-4"><div class="fa fa-coffee" style="font-size:48px"></div><br />Free food and drinks with the purchase of any international flight!</div>
                </div>
                <div class="row" style="text-align:center;font-size:10px">
                    <div class="col-md-4">Click <a href="#">here</a> to learn more about the quality of our flights.</div>
                    <div class="col-md-4">Click <a href="security.php">here</a> to learn more about our security practices.</div>
                    <div class="col-md-4">Click <a href="#">here</a> to learn more about the advantages of flying with us.</div>
                </div>
                <hr />
                <p>Enter your flight number below to see your flight details.</p>
                <div id="info" style="display:none;padding:5px;padding-left:15px;margin-bottom:20px;margin-top:5px" class="alert-danger"></div>
                <form id="lookup-flight" action="lookup.php" method="POST">
                    <div class="input-group">
                        <input type="text" name="flight" style="font-family:monospace" placeholder="XXXX-XXXX-XXXX-XXXX-XXXX" maxlength="24" class="form-control">
                        <span class="input-group-btn">
                            <button class="btn btn-primary" type="submit">Lookup Flight</button>
                        </span>
                    </div>
                </form>
                <hr />
                <div style="text-align:center"><a href="#">Terms of Service</a> - <a href="#">Privacy Policy</a></div>
            </div>
        </div>
    </body>
</html>
