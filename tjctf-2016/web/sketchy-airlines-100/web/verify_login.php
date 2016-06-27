<?php
include_once 'function.php';

try {
    $user = get_user();
}
catch (Exception $e) {
    $fail = $e;
    $user = false;
}
if ($user) {
    if (!isset($_GET['flight']) || empty($_GET['flight'])) {
        header('Content-Type: text/plain');
        echo 'You must specify which ticket you want to download!';
        exit();
    }
    if (strcmp($user, $FLIGHT_PASSENGER) !== 0 || strcasecmp($_GET['flight'], $FLIGHT_NUM) !== 0) {
        header('Content-Type: text/plain');
        echo 'Your account is not allowed to download this file!';
        exit();
    }
    header('Content-type: application/pdf');
    header('Content-Disposition:attachment;filename="ticket.pdf"');
    readfile('../ticket.pdf');
    exit();
}
?>
<!doctype html>
<html>
    <head>
        <title>Sketchy Airlines</title>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
        <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.0.0-alpha/css/bootstrap.min.css">
        <link rel="stylesheet" type="text/css" href="/css/style.css">
        <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.4.0/css/font-awesome.min.css">
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
                <h3 style="text-align:center">Login</h3>
                <p>We need to verify your identity before you can download this ticket.</p>
                <?php if (isset($fail)) { echo '<div class="alert-danger" style="margin-bottom:15px;padding:10px">' . $fail . '</div>'; }
                    else if (isset($_POST['username']) && isset($_POST['password'])) {
                        if ($_POST['username'] !== $FLIGHT_PASSENGER) {
                            echo '<div class="alert-warning" style="margin-bottom:15px;padding:10px">User does not exist!</div>';
                        }
                        else {
                            echo '<div class="alert-warning" style="margin-bottom:15px;padding:10px">Wrong password!</div>';
                        }
                } ?>
                <form action="verify_login.php?flight=<?php echo addslashes($_GET['flight']); ?>" method="POST">
                    <div class="form-group">
                        <label>Username</label>
                        <input class="form-control" type="text" name="username" placeholder="Your Name" />
                    </div>
                    <div class="form-group">
                        <label>Password</label>
                        <input class="form-control" type="text" name="password" placeholder="Your Password" />
                    </div>
                    <input type="submit" value="Login" class="btn btn-success" />
                </form>
            </div>
        </div>
    </body>
</html>
