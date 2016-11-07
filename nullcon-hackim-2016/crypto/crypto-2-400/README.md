# nullcon HackIM : Crypto Question 2

**Category:** Crypto
**Points:** 400
**Solves:**
**Description:**

> Some one was here, some one had breached the security and had infiltrated here. All the evidences are touched, Logs are altered, records are modified with key as a text from book.The Operation was as smooth as CAESAR had Conquested Gaul. After analysing the evidence we have some extracts of texts in a file. We need the title of the book back, but unfortunately we only have a portion of it...
>
>
> [The_extract.txt](./The_extract.txt)


## Write-up

by [steelsoldat](https://github.com/steelsoldat)

After reading the description it was pretty clear this was a Caesar cipher. Upon throwing 'The_extract.txt' into [Xarg's Caesar decrypter](http://www.xarg.org/tools/caesar-cipher/) we can recover what seems like an [excerpt from a book](./The_text.txt)(which would match the problem description).

Afterwards we can throw the first sentence of the plaintext into Google Books, where we are met with multiple books, but the first result 'In the Shadow of Greed' is the correct flag!

## Other write-ups and resources

* <https://cryptsec.wordpress.com/2016/01/31/hackim-ctf-2016-write-up-crypto-question-2-400-points/>
* [P4 Team](https://github.com/p4-team/ctf/tree/master/2016-01-29-nullcon/crypto_2#eng-version)
* <https://www.xil.se/post/hackim-2016-crypto-2-arturo182/>
* <http://h4ckx0re-ctf-crew.co.nf/2016/01/31/hackim-ctf-2016-crypto-2/>
* <https://github.com/Team-Sportsball/CTFs-2016/blob/master/nullcon-hackim-2016/crypto_2/crypto_2.md>
* <https://github.com/Desiprox/NullCon-2016/tree/master/crypto_2>
* [Chinese](http://www.cnblogs.com/Christmas/p/5176509.html)
* [0x90r00t](https://0x90r00t.com/2016/02/03/hackim-2016crypto-400-crypto-question-2-write-up/)
* <http://err0r-451.ru/hackim-crypto-question-2-400pts/>
