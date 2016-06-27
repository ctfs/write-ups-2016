# tjctf-2016 : a-hundred-captchas-60

**Category:** Misc**Points:** 60
**Description:** I heard that this server will give you a flag if you solve a few captchas for them. `nc p.tjctf.org 8008`

## Write-up

Using netcat (or the socket equivalent), go to p.tjctf.org on port 8008 (no longer running) and you can solve a few captchas at a time, unfortunately they require you answer 100 captchas in 30 seconds or less, which indicates you need to automate the process with a script. Although there are many different approaches to solving this problem, the easiest may be to divide the character output of the server into a two dimensional array, split the captcha up into characters, recognize each character (the ASCII drawing font can be found online), and send back the characters of the decoded captcha. After successfully completing 100 in before the server reaches 30 seconds, you will be provided with the flag:  `tjctf{p30PL3_4c7u4llY_D0_7H15}`

## Other write-ups and resources

* [MilWestA - CTFtime.org](https://ctftime.org/writeup/3452)
* [My Computer is a Potato](https://bobacadodl.gitbooks.io/tjctf-2016-writeups/content/a_hundred_captchas_60_points.html)
