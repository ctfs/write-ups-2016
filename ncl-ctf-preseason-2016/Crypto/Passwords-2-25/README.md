# NCL 2016 Preseason : Passwords-2-25

__Category__: Crypto

__Points__: 25

## Write-up

<a href="https://jhalon.github.io/images/ncl5.png"><img src="https://jhalon.github.io/images/ncl5.png"></a>

--

__znggrefnvy__

Our hint here was "__shift cipher__", so we can assume that this is a [Caesar Cipher](http://practicalcryptography.com/ciphers/caesar-cipher/). Since we do not know the total amount the letters were shifted by, we will have to brute force the cipher.

To do this I went to [Decode.fr](http://www.dcode.fr/caesar-cipher) and used their Brute Force Attack to decrypt all possible passwords.

| Shift         | Password      |
| :-----------: |:-------------:|
|+13		| MATTERSAIL	|
|+24		| BPIITGHPXA	|
|+5		| UIBBMZAIQT	|
|+19		| GUNNYLMUCF	|
|+18		| HVOOZMNVDG	|
|+17		| IWPPANOWEH	|
|+20		| FTMMXKLTBE	|
|+16		| JXQQBOPXFI	|
|+22		| DRKKVIJRZC	|
|+25		| AOHHSFGOWZ	|
|+6		| THAALYZHPS	|
|+23		| CQJJUHIQYB	|
|+15		| KYRRCPQYGJ	|
|+21		| ESLLWJKSAD	|
|+1		| YMFFQDEMUX	|
|+4		| VJCCNABJRU	|
|+12		| NBUUFSTBJM	|
|+7		| SGZZKXYGOR	|
|+2		| XLEEPCDLTW	|
|+3		| WKDDOBCKSV	|
|+8		| RFYYJWXFNQ	|
|+10		| PDWWHUVDLO	|
|+11		| OCVVGTUCKN	|
|+14		| LZSSDQRZHK	|
|+9		| QEXXIVWEMP	|

We see that __mattersail__ is being used again - as it was previously. So we can assume password reuse, and it would be the correct answer!

__Answer: mattersail__

--

## Other Write-ups and Resources

* [Jack Halon - KKB](https://jhalon.github.io/ncl-crypto/)
