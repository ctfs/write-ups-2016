# Hack.lu CTF 2016 : cthcoin-150

**Category:** Crypto
**Points:** 150 (+100)
**Solves:** 20
**Description:**

Cthulhu awakens and all worshippers will be rewarded greatly!
A [new Cryptocurrency](https://cthulhu.fluxfingers.net:1511/) was created,
and Cthulhu generous gives away free coins.
Can you break it, but be careful do not provoke him.

## Write-up

When we register at the site, we are given 3 coins worth 5, 10 and 50 cthcoins. There's a shop, where we can buy the flag for 120.
Every coin looks like:
> {"AM": "5", "CU": "NIST384", "MN": "F9BEB4E1", "NC": "303490", "OW": "qwerty1234", "PK": "b6bd0e420b4984854d916c30108d685e70617434f2d3d82a04a9f92ff20719f74ef79d9a6825fddef8460d6d4833d2ac1e5627d52ec916223a8e051cab16b49a621e6501bf05bdee99dd1f44192876d08e1b413b7cd12d1be88e97eb6a6e1ddb", "SIG": "e12bb51c97b95c12d487f302a9cf2c55c4d3f912bd0f53180c5a34308ecf30a292cf7cebf404514e8d792bc8ff1a7afeb6752f14ea0dc2774cb8fbaf5660a374fb3113aebb94164366ed1906980de316fbc821d10cc8827c33ff3f0a06f8086f", "TS": "1477047047"}

AM - is value of the coin. CU - is number of elliptic curve, MN - some magic number, NC - is nonce, OW - owner (my login), PK - public key, SIG - signature, TS - timestamp.
When we submit the coin into the shop's form, it says "You already sent 5 of 120 Coins." If we try to submit the same coin second time, it says "Double spend attempt detected!" We have eather generate new coins or persuade the shop to accept the same coin again.

But OK, it's a web challange! May be there's something interesting in robots.txt?
>User-Agent: *
>
>Disallow: /login
>
>Disallow: /register
>
>Disallow: /buy
>
>Disallow: /debugcoins
>
>Disallow: /shop

What's at debugcoins? It's a list of MD5 hashes of last 50 spend coins. If we look at the end of code of the page, there's an interesting comment, that tells us how everithing works:
>Its ECDSA
>
>sort_keys=True
>
>SIG < AM, CU, MN, NC, OW, PK, TS
>
>MD5 < AM, CU, MN, NC, OW, PK, SIG, TS


So, SIG(AM, CU, MN, NC, OW, PK, TS) is used to verify the authenticity of the coin and MD5(AM, CU, MN, NC, OW, PK, SIG, TS) is used to check if it has already been spend. If we anyhow change any of signed fields, it says that the signature is wrong, even if the only change is uppercasing a letter in HEX of PK. So it's case-sensitive signed! And it turns out, that MD5 is calculated in a case-sensitive way too! So if we change case of any of letters in SIG field it won't break the signature (hex is case-insensitive) and it will change the MD5! Submitting several times the same coin with different case of letteres of SIG hex, we get the flag:
>flag{mT_g0x_?;_;!_wh3erE_iS_Our__Mon..EY_\//\}

P.S. debugcoins hint wasn't needed really, but it helped somehow.

## Other write-ups and resources

* https://dinhbaoluciusteam.wordpress.com/2016/10/24/cthcoinweb100-hacklu2016/
* https://github.com/ctfs/write-ups-2016/tree/master/hack.lu-ctf-2016/crypto/cthcoin-150
