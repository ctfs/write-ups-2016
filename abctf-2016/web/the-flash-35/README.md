# ABCTF 2016 : the-flash-35

**Category:** Web
**Points:** 35
**Solves:** 505
**Description:**

Can you somehow get the flag from [this](http://yrmyzscnvh.abctf.xyz/web2/) website?

## Write-up

Being a web problem, the best first step is to check out the source code of the page, either by using the browser's built in developer tools, or I pressed `Ctrl + U` to view the source code in Google Chrome. You should see a comment with base64 text inside: `<!--c3RvcHRoYXRqcw==-->`. Decoding the base64 reveals the string `stopthatjs`. Submitting that decoded string as a password brings you to a page where the flag is displayed for a short time, however the flag text is in the page's source code: `ABCTF{no(d3)_js_is_s3cur3_dasjkhadbkjfbjfdjbfsdajfasdl}`

## Other write-ups and resources

* [RawSec](https://rawsec.ml/en/ABCTF-35-The-Flash-Web-Exploitation/)
* [RedShield5](https://ctftime.org/writeup/3574)
* [Kimiyuki Onaka](https://kimiyuki.net/blog/2016/07/23/abctf-2016/)
* [OMECA](https://github.com/nbrisset/CTF/blob/master/abctf-2016/challenges/the-flash-35)
