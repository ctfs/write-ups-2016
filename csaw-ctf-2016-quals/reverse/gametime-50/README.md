# CSAW CTF 2016 Quals: Gametime

**Category:** Reverse
**Points:** 50
**Solves:**
**Description:**

@brad_anton

Premise -
A game that requires a user to type either space ('s'), 'm' or 'x' when prompted. If they are fast enough, they get the key.

Warnings -
Everything should be statically compiled. I tested on two different  Win8.1 VMs with no problem. If someone gets DLL loading errors, they most likely need to download Microsoft's Visual C Runtime Library.

## Write-up
You *could* maybe check your speed with the game, but really the solution to reverse out the leading sequence of character presses (they're static), then either reverse out the key or probably much quicker is to:

1. Attach the debugger, set the following breakpoints to overwrite register values to fast track you to the key. You'll need to adjust the image address at run time:

bp image010c0000 + 18d8 "r edx=1;g;"
bp image010c0000 + 1916 "r esi=13;g;"

2. Let the program start, paste in the following sequence, including spaces:

' xm xmmx mmxxmx  xm'

A vuln in the program logic allows the user to add character to the key press buffer before they're prompted to.

Finally the program will spit out:
'key is  (no5c30416d6cf52638460377995c6a8cf5)'

## Other write-ups and resources

* https://youtu.be/MoGtAHvagJw
* http://anee.me/gametime-csaw-ctf-2016-writeup/
* https://blog.michaelz.xyz/csaw-ctf-2016-quals/
* https://github.com/ctfs/write-ups-2016/issues/2116
* http://www.megabeets.net/csaw-2016-gametime-writeup/
* http://ropgadget.com/posts/4.html#csaw16_re_gametime
* https://glennmcgui.re/blog/2016/csaw-ctf-2016-gametime/
* [Jhin Su](https://github.com/JhinSu/CSAW-2016-Write-Ups/tree/master/Reverse/Gametime)
* https://github.com/73696e65/ctf-notes/blob/master/2016-ctf.csaw.io/reversing-50-gametime.md
