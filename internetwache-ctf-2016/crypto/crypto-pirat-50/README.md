# Internetwache CTF 2016 : Crypto-Pirat

**Category:** Crypto
**Points:** 50
**Solves:** 35
**Description:**

> Description: Did the East German Secret Police see a Pirat on the sky? Help me find out! Hint: We had 9 planets from 1930–2006... Hint2: Each planet has a number. (There's a table on a well-known website). After that you might be interested in ciphers used by the secret police.
>
>
> Attachment: [crypto50.zip](./crypto50.zip)

## Write-up

**by [LosFuzzys](https://hack.more.systems)**

Given was a text-file with the following content:

```
 ♆♀♇♀♆ ♇♇♀♆⊕ ♇♀♇♀♆ ♇♆♇♆⊕ ♆♇♆♇♇ ♀♆♇♆⊕ ♆♇♆♇♆ ♇♆♇♆⊕ ♆♇♇♀♇ ♀♆⊕♇♀ ♆⊕♇♀♆ ⊕♆♇♆♇
 ♇♀♆♇♆ ⊕♇♀♇♀ ♆⊕♆♇♆ ♇♆♇♇♀ ♆⊕♆♇♆ ♇♆♇♆⊕ ♆♇♆♇♆ ♇♆⊕♇♀ ♆♇♇♀♆ ♇♆⊕♇♀ ♆♇♆♇♇ ♀♆⊕♆♇
 ♆♇♇♀♇ ♀♇♀♆⊕ ♆♇♆♇♇ ♀♆⊕♇♀ ♇♀♆♇♆ ⊕♆♇♇♀ ♆⊕♇♀♆ ♇♇♀♇♀ ♆⊕♆♇♆ ♇♆♇♆♇ ♆⊕♇♀♆ ♇♇♀♆♇
 ♆⊕♇♀♆ ♇♆♇♇♀ ♆⊕♆♇♆ ♇♇♀♇♀ ♇♀♆⊕♇ ♀♆♇♆♇ ♆⊕♇♀♇ ♀♇♀♆⊕ ♇♀♇♀♆ ♇♆♇♆⊕ ♆♇♆♇♆ ♇♆⊕♆♇
 ♇♀♇♀♆ ⊕♆♇♆♇ ♆♇♆♇♇ ♀♆⊕♇♀ ♇♀♆♇♆ ♇♆⊕♆♇ ♆♇♆♇♇ ♀♇♀♆⊕ ♆♇♆♇♆ ♇♆⊕♆♇ ♇♀♆♇♆ ♇♆⊕♆♇
 ♆♇♆♇♆ ♇♆♇♆⊕ ♆♇♇♀♇ ♀♆⊕♇♀ ♇♀♆♇♆ ⊕♆♇♆⊕ ♆♇♆♇♇ ♀♇♀♇♀ ♆⊕♇♀♆ ♇♇♀♆♇ ♆⊕♇♀♇ ♀♆♇♆♇
 ♆♇♆⊕♇ ♀♆♇♆⊕ ♇♀♇♀♆ ♇♆♇♆⊕ ♆♇♆♇♆ ♇♆⊕♇♀ ♆♇♆♇♇ ♀♆⊕♆♇ ♆⊕♇♀♇ ♀♇♀♆⊕ ♆♇♇♀♆ ♇♆⊕♆♇
 ♇♀♇♀♇ ♀♆⊕♆♇ ♇♀♇♀♆ ♇♆⊕♆♇ ♆♇♇♀♆ ⊕♇♀♆♇ ♆♇♆♇♇ ♀♆⊕♇♀ ♆♇♆♇♆ ♇♇♀♆⊕ ♇♀♆♇♆ ♇♆♇♇♀
 ♆⊕♇♀♆ ♇♆♇♆♇ ♇♀♆⊕♇ ♀♆♇♆♇ ♆♇♇♀♆ ⊕♇♀♆♇ ♆♇♆♇♇ ♀
```
Since all this symbols represent symbols of planets, we mapped all of them to their corresponding planet-number (see [Wikipedia](https://en.wikipedia.org/wiki/Planet#/media/File:Mercury_symbol.svg)):

* ♆ - Neptun ... planet 8
* ♇ - Pluto  ... planet 9
* ♀ - Venus   ... planet 2
* ⊕ - Earth ... planet 3

This gave us the following numbers:

```
 82928 99283 92928 98983 89899 28983 89898 98983 89929 28392 83928 38989 92898 39292 83898 98992
 83898 98983 89898 98392 89928 98392 89899 28389 89929 29283 89899 28392 92898 38992 83928 99292
 83898 98989 83928 99289 83928 98992 83898 99292 92839 28989 83929 29283 92928 98983 89898 98389
 92928 38989 89899 28392 92898 98389 89899 29283 89898 98389 92898 98389 89898 98983 89929 28392
 92898 38983 89899 29292 83928 99289 83929 28989 89839 28983 92928 98983 89898 98392 89899 28389
 83929 29283 89928 98389 92929 28389 92928 98389 89928 39289 89899 28392 89898 99283 92898 98992
 83928 98989 92839 28989 89928 39289 89899 2
```
So what's next? After some quick checks, we followed the first hint and searched the Internet for ciphers used by the Stasi. Already the second search-result let us to a cipher called [**TAPIR**](https://rgpsecurity.wordpress.com/2014/10/17/stasi-vernam-cipher-gernator-tapir/).

TAPIR looks like to be an OTP based crypto system, so with only one message this looked like a dead end. But since TAPIR is an anagram of the word PIRAT (from the challenge name) we assumed to be on the right path, and gave it a closer loook.

Before applying OTP (from the agents codebook), TAPIR uses a decoding via the following substituion table:

![TAPIR](/images/posts/2016-02-21-iwctf2016-crypto-pirat-tapir.jpg)

Mind the fact that some characters are mapped to a single digit, while others are mapped to two digits.

Some quick python did the job ...

```python
tapirDecoded = ''
while len(clist) > 0:
    c = clist.pop(0)
    if len(clist) <= 0:
        break
    if int(float(c)) >= 5:
        c2 = clist.pop(0)
        char = tapir[c + c2]
    else:
        char = tapir[c]
    if char not in blacklist:  # Control chars are not relevant
        tapirDecoded += char
    if char == 'ZwR':  # 'Zwr' is 'Zwischenraum'
        tapirDecoded += ' '

print tapirDecoded
```

... and since luckily no OTP was used, revealed the plaintext ... almost:

```
-.- --.. ..-. .... .-- - - ..-. -- ...- ... ... -.-. -..- ..--- ..- --. .- -.-- .... -.-. -..-
..--- -.. --- --.. ... .-- ....- --.. ...-- ... .-.. ..... .-- --. . ..--- -.-. --... -. --.. ...
-..- . --- .-. .--- .--. ..- -...- -...- -...- -...- -...- -...-
```

This is of course morse code. So more python to the rescue:

```python
morseDecoded = morse_talk.decode(tapirDecoded)
print morseDecoded
```

Decoding to the following string:

```
KZFHWTTFMVSSCX2UGAYHCX2DOZSW4Z3SL5WGE2C7NZSXEORJPU
```

The flag? Not yet.

It's also not the obvious Base64, so what else? Of course you cannot decode arbitrary characters in morse, so something with a smaller alphabet has to be used. Base32 to the rescue!

Vuolá! The flag!

```
VJ{Neee!_T00q_Cvengr_lbh_ner:)}
```
Well ... not yet. Of course, the obligatory flag-format *IW{...}* is not present. But this time it's easy. We are still in the crypto category, so ... Caesar cipher, and here we go:

```
IW{Arrr!_GWWd_Pirate_you_are:)}
```

The whole python code used to solve this challenge, plus the TAPIR table in text form, can be found [on GIST](https://gist.github.com/stefan2904/9e92cf559be94ded4f3d).


## Other write-ups and resources

* <https://losfuzzys.github.io/writeup/2016/02/21/iwctf2016-crypto-pirat/>
* <http://cafelinux.info/articles/writeups-internetwache-ctf-2016-crypto-pirat-crypto50>
* [CTF.RIP](https://ctf.rip/internetwache-2016-crypto-pirat-cryptography-challenge/)
* <http://ctfwriteups.blogspot.de/2016/02/internetwache-ctf-2016-crypto-pirat.html>
* <http://www.melodia.pw/2016/02/22/internetwache-ctf-2016-writeup-crypto-50/>
