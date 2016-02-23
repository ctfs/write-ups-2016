# Internetwache CTF 2016 : Replace with Grace

**Category:** Web
**Points:** 60
**Solves:** 229
**Description:**

> Description: Regular expressions are pretty useful. Especially when you need to search and replace complex terms.
> 
> 
> Service: <https://replace-with-grace.ctf.internetwache.org/>

Sources: <https://github.com/internetwache/Internetwache-CTF-2016/tree/master/tasks/web60/code>

## Write-up

**by [LosFuzzys](https://hack.more.systems)**

The given website is used to "Search & Replace" with regular expressions.
From other challenges we know, that we can execute php code using:

```php
/(.*)/e
```

(Check out [this Stackoverflow answer](http://stackoverflow.com/a/16986549/1518225) for details.)

The problem was, that the website filtered some inputs like:

* file
* open


It worked with:

```php
var_dump(show_source('flag.php'));
```

A simple, but nice challenge.

```
IW{R3Pl4c3_N0t_S4F3}
```

## Other write-ups and resources

* <https://github.com/raccoons-team/ctf/tree/master/2016-02-20-internetwache-ctf/web60>
* <https://forum.xeksec.com/f138/t88658/>
* <http://losfuzzys.github.io/writeup/2016/02/22/iwctf2016-ReplaceWithGrace/>
* <http://cafelinux.info/articles/writeups-internetwache-ctf-2016-replace-with-grace-web60>
* <http://rektsec.github.io/writeups/ctf/internetwatche-2016-ctf-replace-with-grace-web-60/>
* <http://ctfwriteups.blogspot.de/2016/02/internetwache-ctf-2016-replace-with.html>
* <https://github.com/WesternCyber/CTF-WriteUp/blob/master/2016/Internetwache/Web/Web60.md>
