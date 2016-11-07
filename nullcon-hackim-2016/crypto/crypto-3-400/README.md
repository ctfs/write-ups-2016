# nullcon HackIM : Crypto Question 3

**Category:** Crypto
**Points:** 400
**Solves:**
**Description:**

> After entring the luxurious condomium,you get the feel that you are in home of a yester Star. the extravagant flooring and furnishings shows the richness of this star. But where is she? There she is, lying peacefuly on her couch. See what Envy has done to her...with a perfectly well maintained attractive body she still looks sex diva, except for her face beyond recogniton. Her identity is crucial to know who killed her and why? In absence of any personal data around there is only a file. with a cryptic text in it. Preity sure she has used her own name to XOR encrypt the file. And challenge is to know her name.
>
>
> [AncientSecretsOfTheKamaSutra.txt](./AncientSecretsOfTheKamaSutra.txt)


## Write-up

by [steelsoldat](https://github.com/steelsoldat)

Crypto 3: We're given a text file that we can't read 'AncientSecretsOfTheKamaSutra.txt'

Upon googling the name of the text file we *come* up with a 1997 Adult Film.
The hints tell us someone was dead over a couch, but luckily you dont need to watch the porno to find out if that is a scene in the film.

I began xoring the contents of the text file with various star names(first with in-film names) then converting the reverting hex to ascii

Upon xoring with 'Jeanna Fine' we get a huge block of hex

```
a5dadc7e636b274d282f4d476f2f58104e33422073241946702067020ca9d6d324476f606a3d496e5c2c0340466a68207b29030f706a1620746865792077616e74203440246d652361124762720f184a657b2f3a4886d1d86762607c44432d4c7f207f43205e27636b2422036a60476f2f6221552c086d0a4b0f747a726a8e9ffb5f6b6e4e1c5e796a2f214986d1d878646a62160b36427f2068402c41622e2479632c7b63417d8ed1d3402608780b0f5b6c6a20636b6962726172390f7367657d24a9d6d3574b6e7d44568e9ffb86d1d8476f2f81d1dccff9d44a634b6b4b45696f3b5c282f4d476f6681d1dc44782c7c6e476f722b5c7b6e4b63020f5b6c6a2044200b4e27581a74728ed1d3236e433c5a8af5d88ed1d3630a7e86d1d8a5dadc6364662f010f7363a5dadc1d04712f4186d1d85f204973696c2a2242676840722f792754cff9d4742021416766658e9ffb7c81daf76a6663646d4b2c7b676e56618ed1d353214d754442a5dadc6a742fcff9d481daf74e8ed1d37c313e4678770a2b54264d28234a1050724e787c2f2952cff9d4636fa5dadc17044e34446e6a8af5d84669636b651f5781daf7726a2081de9d084b277fa5dadc05476c2a4274207002466520400a074228537e5f374627738e9ffb00568af5d87473208e9ffb274c2c488aded3054f360773686107037c6f2b060b4d71207b476f204b627c653b4b81daf7766a207b29035627660a6574206d616e7920706568401f4781d1dc615f6f608af5d8577561675e656f81daf767637681de9d74656163280f70676562610b4e69720f0244796a2f05a9d6d3286d2c5c7e1059240774656718467c73258e9ffb0e2b535662743a4d666e411a044a4e6a8ed1d36e612046696e250f0e
```

that turns into the following ASCII
```
¥ÚÜ~ck'M(/MGo/XN3B s$Fp g©ÖÓ$Go`j=In\,@Fjh {)pj they want 4@$me#aGbrJe{/:HÑØgb`|DC-L C ^'ck$"j`Go/b!U,m
Ktzrjû_knN^yj/!IÑØxdjb6B h@,Ab.$yc,{cA}ÑÓ@&x[lj ckibrar9sge}$©ÖÓWKn}DVûÑØGo/ÑÜÏùÔJcKkKEio;\(/MGofÑÜDx,|nGor+\{nKc[lj D N'XtrÑÓ#nC<ZõØÑÓc
~ÑØ¥ÚÜcdf/sc¥ÚÜq/AÑØ_ Isil*"Bgh@r/y'TÏùÔt !Agfeû|Ú÷jfcdmK,{gnVaÑÓS!MuDB¥ÚÜjt/ÏùÔÚ÷NÑÓ|1>Fxw
+T&M(#JPrNx|/)RÏùÔco¥ÚÜN4DnjõØFickeWÚ÷rj ÞK'¥ÚÜGl*Bt pFe @
```
'they want me' is in that output, so 'Jeanna Fine' is the flag.

## Other write-ups and resources

* <https://cryptsec.wordpress.com/2016/01/31/hackim-ctf-2016-write-up-crypto-question-3-400-points/>
* <https://www.xil.se/post/hackim-2016-crypto-3-arturo182/>
* <https://github.com/WesternCyber/CTF-WriteUp/blob/master/2016/HackIM/crypto-3.md#nullcon-hackim-crypto-question-3>
* [Chinese](http://www.cnblogs.com/Christmas/p/5176542.html)
* [0x90r00t](https://0x90r00t.com/2016/02/03/hackim-2016crypto-400-crypto-question-3-write-up/)
