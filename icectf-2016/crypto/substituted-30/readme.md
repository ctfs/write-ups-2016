# IceCTF-2016 : substituted-30

**Category:** Crypto
**Points:** 30
**Description:**

We got a substitute flag, I hear they are pretty lax on the rules

## Writeup

The use of the word `substitute` indicates that this may be a substitution cipher. This one happens to be based on letter frequency, so a quick Google search will pull up an English letter frequency list. Either manually, or using a Python script (like rawsec) substituting each letter for its partner in frequency, you will get the following output:

```
Hi!

Welcome to IceCTF!

I'll be your substitute flag for the day. For today, we are studying basic cryptography and its applications. Cryptography has a long history, although with the advent of computers it has gotten really complicated. Some simple old ciphers are the Caesar cipher, the Vigenere cipher, the substitution cipher, which is this one, and so on. Almost all of these ciphers are easily broken today with the help of computers. Some new encryption methods are AES, the current standard for encryption, along with RSA. Cryptography is a vast field and is very interesting though. So kick back, read up on some cool ciphers and have fun!

Oh and for your records my name is IceCTF{always_listen_to_your_substitute_flags}.
```

## Other write-ups and resources

* [RawSec](https://rawsec.ml/en/IceCTF-30-Substituted-Cryptography/)
* https://youtu.be/xQJ4Ndke9HM
* http://5k33tz.com/icectf-substituted/
* https://github.com/TeamContagion/CTF-Write-Ups/tree/master/icectf-2016/Crypto/Substituted
* [Japanese](https://ctftime.org/writeup/3807)
