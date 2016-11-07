# EKOPARTY CTF 2016 : welcome-to-the-dark-side-25

**Category:** FBI
**Points:** 25
**Solves:** 360
**Description:**

> At Silk Road, every precaution is made to ensure your anonymity and security, from connecting to the site, to making your transactions, to receiving your items.
> `https://silkroadzpvwzxxv.onion`


## Write-up

Using Google, you can read up on `.onion` domains. In short, these domains can only by reached through the Tor browser. Download and open this browser and proceed to the given URL. First, take a look at the page source code (right click, inspect element), and on the first line the flag appears: `EKO{buy_me_some_b0ts}`, referring to some `.onion` domains where people do sketchy stuff, including buying botnets.

## Other write-ups and resources

* https://youtu.be/6EHFSwKzDAI
* [0day](https://0day.work/ekoparty-ctf-2016-writeups/)
* http://specterdev.blogspot.ca/2016/10/write-up-ekoparty-2016-ctf-misc-50pt.html
