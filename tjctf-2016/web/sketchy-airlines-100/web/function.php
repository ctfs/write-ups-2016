<?php
include_once 'secret.php'; // contains $SECRET_KEY

function arr_to_str($arr) {
    $out = array();
    foreach ($arr as $key => $val) {
        $v = $val;
        if ($v === true) {
            $v = 'true';
        }
        if ($v === false) {
            $v = 'false';
        }
        $out[] = $key . '=' . $v;
    }
    return join('&', $out);
}

function str_to_arr($str) {
    $pairs = explode('&', $str);
    $out = array();
    foreach ($pairs as $value) {
        $a = explode('=', $value);
        if (count($a) != 2) {
            throw new Exception('Malformed item!');
        }
        $val = $a[1];
        if ($val === 'true') {
            $val = true;
        }
        else if ($val === 'false') {
            $val = false;
        }
        $out[$a[0]] = $val;
    }
    return $out;
}

function get_vars() {
    global $SECRET_KEY;
    $cookie = urldecode($_COOKIE['session']);
    if (!isset($_COOKIE['session'])) {
        $sess = array('logged_in' => false, 'name' => '');
        $sess_str = arr_to_str($sess);
        setcookie('session', urlencode($sess_str));
        setcookie('hash', md5($SECRET_KEY . $sess_str));
        return $sess;
    }
    if (md5($SECRET_KEY . $cookie) !== $_COOKIE['hash']) {
        throw new Exception('Hash does not match!');
    }
    $a = str_to_arr($cookie);
    if (isset($_GET['debug'])) {
        echo "<!--\n";
        print_r($a);
        echo "-->\n";
    }
    return $a;
}

function get_user() {
    $arr = get_vars();
    if (!in_array('logged_in', $arr) || !in_array('name', $arr)) {
        return false;
    }
    if (!$arr['logged_in']) {
        return false;
    }
    return $arr['name'];
}

function encrypt_credit_card($number) {
    return base64_encode($number);
}
