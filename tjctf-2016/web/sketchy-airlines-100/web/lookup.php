<?php
include_once 'secret.php';

if (isset($_POST['flight'])) {
    header('Content-Type: application/json');
    if (!preg_match('/^[0-9A-Za-z]{4}-[0-9A-Za-z]{4}-[0-9A-Za-z]{4}-[0-9A-Za-z]{4}-[0-9A-Za-z]{4}$/', $_POST['flight'])) {
        echo json_encode(array('error' => 'Invalid flight number format!'));
        exit();
    }
    if (strcasecmp($FLIGHT_NUM, $_POST['flight']) === 0) {
        echo json_encode(array('redirect' => ('/lookup.php?flight=' . $FLIGHT_NUM)));
        exit();
    }
    echo json_encode(array('error' => 'Your flight number was not found in our database!'));
    exit();
}
if (!isset($_GET['flight'])) {
    header('Location: /');
    exit();
}
if (strcasecmp($FLIGHT_NUM, $_GET['flight']) !== 0) {
    echo 'Invalid flight number!';
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
<script>
$(document).ready(function() {
    $("#download-ticket").click(function(e) {
        window.location.href = 'verify_login.php?flight=<?php echo $FLIGHT_NUM; ?>';
        e.preventDefault();
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
                <h3 style="text-align:center">Your Flight Details</h3>
                <div class="alert-warning" style="padding:10px;margin-bottom:15px"><b>Travel Tip of the Day</b><p style="margin-bottom:0px">Make sure you have a medical form for your recreational oxygen! <span style="color:#ff6600">Sketchy</span><span style="color:#28170b">Airlines</span> does not provide oxygen unless you have a medical reason. (<a href="https://www.tsa.gov/travel/security-screening/prohibited-items" rel="noreferrer">TSA Policies</a>, Explosives/Flammables)</p></div>
                <p><b>Flight Number:</b> <?php echo $FLIGHT_NUM; ?></p>
                <p><b>Passenger:</b> <?php echo $FLIGHT_PASSENGER; ?></p>
                <p><b>Ticket Type:</b> First Class</p>
                <p><b>Seat Number:</b> 13e</p>
                <p><b>Origin:</b> ABC (Gate 117)</p>
                <p><b>Destination:</b> XYZ (Gate 23)</p>
                <p><b>Date:</b> <?php echo date(DATE_RFC2822, mktime(9, 45, 0, date('m'), date('d') + 5, date('Y'))); ?></p>
                <a id="download-ticket" href="#" class="btn btn-primary">Download Your Ticket</a> <a href="#" class="btn btn-danger">Cancel Your Flight</a>
            </div>
        </div>
    </body>
</html>
