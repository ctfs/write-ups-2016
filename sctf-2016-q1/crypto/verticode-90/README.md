# sCTF 2016 Q1 : verticode-90

**Category:** Crypto
**Points:** 90
**Solves:** 270
**Description:**

Welcome to Verticode, the new method of translating text into vertical codes.

Each verticode has two parts: the `color shift` and the `code`.

The code takes the inputted character and translates it into an ASCII code, and then into binary, then puts that into an image in which each black pixel represents a 1 and each white pixel represents a `0`.

For example, `A is 65` which is `1000001` in binary, `B is 66` which is `1000010`, and `C is 67` which is `1000011`, so the corresponding verticode would look like [this](https://github.com/ctfs/write-ups-2016/tree/master/sctf-2016-q1/crypto/verticode-90/A-Code.png).

Except, it isn't that simple.

A color shift is also integrated, which means that the color before each verticode shifts the ASCII code, by adding the number that the color corresponds to, before translating it into binary. In that case, the previous verticode could also look like [this](https://github.com/ctfs/write-ups-2016/tree/master/sctf-2016-q1/crypto/verticode-90/B-Code.png).

The table for the color codes is:

0 = Red  
1 = Purple  
2 = Blue  
3 = Green  
4 = Yellow  
5 = Orange  

This means that a red color shift for the letter `A`, which is `65 + 0 = 65`, would translate into `1000001` in binary; however, a green color shift for the letter `A`, which is `65 + 3 = 68`, would translate into `1000100` in binary.

Given [this verticode](https://github.com/ctfs/write-ups-2016/tree/master/sctf-2016-q1/crypto/verticode-90/code1.png), read the verticode into text and find the flag.

Note that the flag will not be in the typical `sctf{flag}` format, but will be painfully obvious text. Once you find this text, you will submit it in the `sctf{text}` format. So, if the text you find is adunnaisawesome, you will submit it as `sctf{adunnaisawesome}`.


SHA512 Solution Hash(es):
* 2daf3b3818d0ccb51134f7875fe3fd2221657151de15c5ca39a1902fbe81104e40e3fb4f6d27bbfd85b7445c4566153de1388dffac10608b7102fa8988b89fe7

**Hint**
Try looking up some imaging libraries.

## Write-up

(TODO)

## Other write-ups and resources

* https://github.com/HackThisCode/CTF-Writeups/tree/master/2016/SCTF/Verticode
* https://github.com/318br/sctf/tree/master/2016q1/Verticode
* http://hack.carleton.team/2016/04/18/sctf-io-2016-q1-verticode-90-points/
* [iPush](http://ipushino.blogspot.com/2016/04/sctf-2016-q-verticode-crypto.html)
* https://sardinachanx.gitbooks.io/sctf-2016q1-write-ups/content/verticode_90_pts.html
* https://pequalsnp-team.github.io/writeups/verticode
