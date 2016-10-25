# Hack.lu CTF 2016 : redacted-200

**Category:** Crypto
**Points:** 200 (-23)
**Solves:** 80
**Description:**

> Someone gave a nice presentation with some redacted ssh keys, I extracted them for you, the seem to belong to berlin@cthulhu.fluxfingers.net on port 1504.
> Good Luck

> Attachment: [redacted](redacted)

## Write-up

If we change "x"->"A" in given base64data and decode it, we get a broken asn1 structure. I've also changed "x" -> "/", base64 decoded, xor'ed it with the first binary structure and got a mask of unknown bits. From the asn1 structure we can extract N, P, Q, e, d,... (i've generated a new key with ssh-keygen and used it as an example) but all numbers except e have broken bits. N has big areas of broken bits, P and Q have less broken bits.

Sinse it's RSA N should be equal to P * Q. So we can recover P and Q bit-by-bit, starting from the lowerst bits!

The algorithm bases on the fact that k lowerst bits of N depend only on k lowers bit of both P and Q. So we can take the lowerst unknown bit of any of P or Q (let's say it's k-th bit of P), try both 0 and 1 values and check which one gives the right k-th bit of N. If k-th bit of N is unknown, we just save both possible values of P and proceed to the next unknow bit.

Having e, P, Q we can reconstruct all RSA parameters. The code is in [recoverer.py](recoverer.py)


## Other write-ups and resources

* http://duksctf.github.io/Hack.lu2016-redacted/
* http://manylostticks.blogspot.lu/2016/10/hacklu-ctf-2016-redacted-write-up.html
* https://github.com/ctfs/write-ups-2016/tree/master/hack.lu-ctf-2016/crypto/redacted-200
