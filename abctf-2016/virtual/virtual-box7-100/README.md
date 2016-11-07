# ABCTF 2016 : virtual-box7-100

**Category:** Virtual
**Points:** 100
**Solves:** 74
**Description:**

Hmm, I wish I could figure out the team that created Windows 98 without the map hassle.

## Write-up

This one was little bit tricky...
A little google-search revealed there's a easter-egg in Win98 regarding the
developement-team's credit animation.

There are two way's of accessing it, one is related to the "map hassle" and
the other one to the solution, which is described [here](http://www.eeggs.com/items/484.html).

I spent quite some time getting the easter egg running, but it didn't seem to work
correctly.

I thought they placed the flag in the team members enumeration, so I managed to dump the XML-file
which is used in the Weldata.exe...  but there wasn't any flag in there:(

Finally I thought the easter-egg magic string "You_are_a_real_rascal" looks quite like a flag...

so I tried: ABCTF{You_are_a_real_rascal} and...

BOOM! It worked:)

## Other write-ups and resources

* [Takatori Ru (Japanese)](http://yuelab82.hatenablog.com/entry/2016/07/24/042028)
