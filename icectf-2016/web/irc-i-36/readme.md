# IceCTF-2016 : irc-i-36

**Category:** Web
**Points:** 36
**Description:**

There is someone sharing flags on our IRC server, ca you find him and stop him? glitch.is:6667

## Writeup

Connect to the IRC channel using any client (rawsec suggests Mibbit if you don't have one). Use the `/list` command to list all IRC channels, and one exists called `#6470e394cb_flagshare`. Join the channel using the command `/join #6470e394cb_flagshare`. Finally display the channels topic using the `/topic` command, where it should display `Get your flags here! while they’re hot! IceCTF{pL3AsE_D0n7_5h4re_fL495_JUsT_doNT}`.

## Other write-ups and resources

* [RawSec](https://rawsec.ml/en/IceCTF-35-IRC-1-Misc/)
* [Japanese](https://ctftime.org/writeup/3815)
* https://github.com/Idomin/CTF-Writeups/blob/master/IceCTF/Irc1-Misc-35
* https://youtu.be/MMZec1hxBcQ
