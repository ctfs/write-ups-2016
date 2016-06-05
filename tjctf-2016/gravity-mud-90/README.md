# tjctf-2016 : gravity-mud-90

**Category:** Misc**Points:** 90
**Description:** Wanna hear a joke? north, south, east, west, up, down, examine item `nc p.tjctf.org 8006`

## Write-up

After connecting to the given server on netcat, it is painstakingly obvious this text adventure is similar to Zork (an online text-adventure game). One strategy may be to copy and paste  directions (seperated by a newline) into the netcat connection quickly until you find the flag. I found it easier to write [a Java program](https://gist.github.com/tjgerot/0c49de3d891107186255fc95a9e1d38e) that takes in a series of directions, connects to the server, and executes all the commands in rapid succession. After touring the map, I came across pieces of the flag until you put it together and submit this flag: `tjctf{y0u_m1ght_h@v3_b33n_m1$sing_t3h_fl4g_but_YOUR_A1M_IS_G3TT1NG_B3TT3R}`

## Other write-ups and resources

* [MilWestA - CTFtime.org](https://ctftime.org/writeup/3449)
* [HackCat](http://s0ngsari.tistory.com/entry/TJCTF-gravitymud)
