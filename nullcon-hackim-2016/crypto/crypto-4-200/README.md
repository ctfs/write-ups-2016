# nullcon HackIM : Crypto Question 4

**Category:** Crypto
**Points:** 200
**Solves:**
**Description:**

> He is influential, he is powerful. He is your next contact you can get you out of this situation. You must reach him soon. Who is he? The few pointers intrecpted by KGB are in the file. Once we know him, we can find his most valuable possession, his PRIDE.
>
>
> [whatsHisPride.md5s](./whatsHisPride.md5s)


## Write-up

by [steelsoldat](https://github.com/steelsoldat)

Opening the file attatched leads to a list of MD5 hashes. After running them through a rainbow table they come out to the following
* d80517c8069d7702d8fdd89b64b4ed3b : Carrie
* 088aed904b5a278342bba6ff55d0b3a8 : Grease
* 56cdd7e9e3cef1974f4075c03a80332d : Perfect
* 0a6de9d8668281593bbd349ef75c1f49 : Shout
* 972e73b7a882d0802a4e3a16946a2f94 : Basic
* 1cc84619677de81ee6e44149845270a3 : Actor
* b95086a92ffcac73f9c828876a8366f0 : Aircraft
* b068931cc450442b63f5b3d276ea4297 : name

After we take those words and plug them into Google the first result is John Travolta, which matches the problem description of an influential man. Next we need to find out what his PRIDE is. The terms all seemed to be related to his acting career other than the last two words: Aircraft, and name.

Looking at his [Wikipdea page](https://en.wikipedia.org/wiki/John_Travolta) we can see he does own a plane, which has a name. *"He owns five aircraft, including an ex-Qantas Boeing 707-138 airliner that bears the name Jett Clipper Ella in honor of his children"*

The name of his aircraft is the flag! Jett Clipper Ella

## Other write-ups and resources

* <https://cryptsec.wordpress.com/2016/01/31/hackim-ctf-2016-write-up-crypto-question-4-200-points/>
* [P4 Team](https://github.com/p4-team/ctf/tree/master/2016-01-29-nullcon/crypto_4#eng-version)
* <http://h4ckx0re-ctf-crew.co.nf/2016/01/31/hackim-ctf-2016-crypto-4/>
* <http://err0r-451.ru/hackim-crypto-question-4-200pts/>
* [Chinese](http://www.cnblogs.com/Christmas/p/5176564.html)
