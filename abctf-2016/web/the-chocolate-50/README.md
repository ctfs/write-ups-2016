# ABCTF 2016 : the-chocolate-50

**Category:** Web
**Points:** 50
**Solves:** 440
**Description:**

If you could become admin you would get a flag. [Link](http://yrmyzscnvh.abctf.xyz/web3/)

## Write-up

On the website linked in the description, opening developer tools in your browser should allow you to view your browser's request for the page. Inside this request is a line `Set-Cookie: coookie=e2FkbWluOmZhbHNlfQ%3D%3D`. URL decoding this string gives you this base64 string: `e2FkbWluOmZhbHNlfQ==` which decoded to ASCII becomes `{admin:false}`. Changing this to `{admin:true}` (hopefully to have the site recognize you as an admin) then encoding that into base64 (`e2FkbWluOnRydWV9`) and setting your browser's cookie (with the same name) equal to the new string. This can be done using the developer tool's cookie view, or by running the following JavaScript:

```javascript
document.cookie = "cookie=coookie=e2FkbWluOnRydWV9";
```

Refreshing the page with the new cookie set, your are presented with the flag: `ABCTF{don't_trust_th3_coooki3}`

## Other write-ups and resources

* [RawSec](https://rawsec.ml/en/ABCTF-50-Chocolate-Web-Exploitation/)
* [RedShield5](https://ctftime.org/writeup/3576)
* [Kimiyuki Onaka](https://kimiyuki.net/blog/2016/07/23/abctf-2016/)
