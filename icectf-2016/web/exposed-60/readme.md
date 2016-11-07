# IceCTF-2016 : exposed-60

**Category:** Web
**Points:** 60
**Description:**

John is pretty happy with himself, he just made his first website! He used all the hip and cool systems, like NginX, PHP and Git! Everyone is so happy for him, but can you get him to give you the flag?

## Writeup

While NginX and PHP have their vulnerabilities, any experienced web developer can tell you that Git, when incorrectly secured, is an exploit waiting to happen. Chances are, this site's repository on GitHub is public. This is testable by running `git clone http://exposed.vuln.icec.tf/.git`. View the list of commits and use `git diff` for each commit to view the changes made. The commit `added colors` contains the following flag: `IceCTF{secure_y0ur_g1t_repos_pe0ple}`

## Other write-ups and resources

* https://github.com/WCSC/writeups/tree/master/icectf-2016/Exposed
* https://mrpnkt.github.io/2016/icectf2016-exposed-writeup/
* [RawSec](https://rawsec.ml/en/IceCTF-60-Exposed-Web/)
* https://github.com/Idomin/CTF-Writeups/blob/master/IceCTF/Exposed-Web-60
* http://hyp3rv3locity.com/content/icectf-2016-exposed-web-60-pt
* https://www.youtube.com/watch?v=FVU-A3mbl0E
