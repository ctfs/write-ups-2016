# IceCTF-2016 : rotated-20

**Category:** Crypto
**Points:** 20
**Description:**

They went and ROTated the flag by 5 and then ROTated it by 8! The scoundrels! Anyway once they were done this was all that was left VprPGS{jnvg_bar_cyhf_1_vf_3?}

## Writeup

The most classic cipher is ceasar cipher, and with the keyword rotate (ROT), there's a good chance it's a ceasar cipher. Because cipher rotations add up, 5 and 8 combine to make 13. ROT13 is also a very common rotation for ceasar ciphers based on a shift of 1/2 the length of the alphabet. Using an online ceasar cipher solver with a shift of 13 (or a Python script like rawsec), you'll get the result `IceCTF{wait_one_plus_1_is_3?}`

## Other write-ups and resources

* [RawSec](https://rawsec.ml/en/IceCTF-20-Rotated-Cryptograhy/)
* https://github.com/Idomin/CTF-Writeups/blob/master/IceCTF/Rotated-Crypto-20
* http://5k33tz.com/icectf-rotated/
* https://github.com/TeamContagion/CTF-Write-Ups/tree/master/icectf-2016/Crypto/Rotated
* (Japanese)[https://ctftime.org/writeup/3806]
* https://gitlab.com/Babache/writeups/tree/master/CTF/IceCTF2k16/Stage-1/Rotated
