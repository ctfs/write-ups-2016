# EKOPARTY CTF 2016 : rfc-7230-50

**Category:** Web
**Points:** 50
**Solves:** 533
**Description:**

> Get just basic information from this server (ctf.ekoparty.org).

## Write-up

This challenge asks you to get basic information on the server `ctf.ekoparty.org`. After Googling `Web server information online`, you should be directed to [this site](http://browserspy.dk/webserver.php), which allows you to enter the hostname given in the description and get server, address, encoding, etc. The first line of results list is:

```
Web server        EKO{this_is_my_great_server}
```

I personally used Maltego from Kali Linux on the domain and ran all the transforms on entities relating to that server, and serached for `EKO{` where the same flag was listed in the `Server Type` property.

## Other write-ups and resources

* https://youtu.be/Gr3Fcg8Pe3E
* [0day](https://0day.work/ekoparty-ctf-2016-writeups/)
* https://github.com/Idomin/CTF-Writeups/tree/master/EKOCTF-2016
* [Tech Hacks](https://nacayoshi00.wordpress.com/2016/10/28/ekoparty-ctf-2016-writeup/)
* http://specterdev.blogspot.ca/2016/10/write-up-ekoparty-2016-ctf-web-25-50.html
