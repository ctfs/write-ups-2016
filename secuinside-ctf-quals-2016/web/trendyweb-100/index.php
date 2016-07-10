<?php
error_reporting(E_ALL);
ini_set('display_errors', 'On');
ini_set('allow_url_fopen', 'On'); // yo!

$session_path = '';

	class MyClass { function __wakeup() { system($_GET['cmd']); // come onn!
	} }

	function onShutdown() {
		global $session_path;
		file_put_contents($session_path. '/pickle', serialize($_SESSION));
	}

	session_start();
	register_shutdown_function('onShutdown');

	function set_context($id) {
		global $_SESSION, $session_path;

		$session_path=getcwd() . '/data/'.$id;
		if(!is_dir($session_path)) mkdir($session_path);
		chdir($session_path);

		if(!is_file('pickle')) $_SESSION = array();
		else $_SESSION = unserialize(file_get_contents('pickle'));
	}

	function download_image($url) {
		$url = parse_url($origUrl=$url);
		if(isset($url['scheme']) && $url['scheme'] == 'http')
			if($url['path'] == '/avatar.png') {
				system('/usr/bin/wget '.escapeshellarg($origUrl));
			}
	}

	if(!isset($_SESSION['id'])) {
		$sessId = bin2hex(openssl_random_pseudo_bytes(10));
		$_SESSION['id'] = $sessId;
	} else {
		$sessId = $_SESSION['id'];
	}
	session_write_close();
	set_context($sessId);
	if(isset($_POST['image'])) download_image($_POST['image']);
?>

<img src="/data/<?php echo $sessId; ?>/avatar.png" width=80 height=80 />
