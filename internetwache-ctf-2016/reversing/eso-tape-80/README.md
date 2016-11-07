# Internetwache CTF 2016 : Eso Tape

**Category:** Reversing
**Points:** 80
**Solves:** 69
**Description:**

> Description: I once took a nap on my keyboard. I dreamed of a brand new language, but I could not decipher it nor get its meaning. Can you help me? Hint: Replace the spaces with either '{' or '}' in the solution. Hint: Interpreters don't help. Operations write to the current index.
>
>
> Attachment: [rev80.zip](./rev80.zip)


## Write-up

We are given just one file in the challenge ZIP: `priner.tb`

Opening the file, we are presented with a wonderous mix of #, %, +, -, &, * and & symbols. Given this, plus the name of the challenge and the name/extension of the file, I assumed this is some sort of esoteric language, so I found my way to [esolangs.org's language list](http://esolangs.org/wiki/Language_list) and started investigating.

Considering the challenge name Eso **Tape**, I guessed the t in .tb might also stand for tape. I searched for "tape" on the language list page, and found what I was looking for in the third match: [TapeBagel](http://esolangs.org/wiki/TapeBagel).

The TapeBagel wiki entry details the action each block of characters performs on the program state, however I was unable to find an interpreter I could run on the challenge file. I was (un)lucky enough to be working on this challenge before the hints for it were released, which stated "Interpreters don't help. Operations write to the current index.", which implies that the activity the program performs might be simple enough to work out by hand.......

Instead, I implemented an *extremely* simple (don't judge, it's for a CTF!) TapeBagel interpreter in Python, which I've made available [here](https://github.com/jashanbhoora/TapeBagel-Interpreter)

So! Running the file we are given through my interpreter outputs the string "IW ILOVETAPEBAGEL ".

Replacing the spaces with braces, we get our flag!
I really enjoyed this challenge! Kudos to the creator!

Flag: **IW{ILOVETAPEBAGEL}**

## Other write-ups and resources

* <https://www.xil.se/post/internetwache-2016-rev80-kbeckmann/>
* <https://www.xil.se/post/internetwache-2016-rev-80-arturo182/>
* [Jashan Bhoora](https://github.com/jashanbhoora/write-ups-2016/tree/master/internetwache-ctf-2016/reversing/eso-tape-80)
* [0x90r00t](https://0x90r00t.com/2016/02/22/internetwache-ctf-2016-reverse-80-eso-tape-write-up/)
* [P4 Team](https://github.com/p4-team/ctf/tree/master/2016-02-20-internetwache/re_80)
* <https://github.com/EspacioTeam/write-ups/tree/master/2016/internetwache/exp80>
* <https://github.com/QuokkaLight/write-ups/blob/master/internetwache-ctf-2016/reverse/rev80.md>
* <http://poning.me/2016/02/29/eso-tape/>
[esolangs.org's language list](http://esolangs.org/wiki/Language_list)
[TapeBagel](http://esolangs.org/wiki/TapeBagel)
[TapeBagel Interpreter](https://github.com/jashanbhoora/TapeBagel-Interpreter)
