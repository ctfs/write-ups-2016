# Internetwache CTF 2016 : Brute with Force

**Category:** Code
**Points:** 80
**Solves:** 66
**Description:**

> Description: People say, you're good at brute forcing... Have fun! Hint: You don't need to crack the 31. character (newline). Try to think of different (common) time representations. Hint2: Time is CET
>
>
> Service: 188.166.133.53:11117


## Write-up

**by [LosFuzzys](https://hack.more.systems)**

After telnet'ing to the given host, we received the following challenge from the server:

```
Trying 188.166.133.53...
Connected to 188.166.133.53.
Escape character is '^]'.
People say, you're good at brute forcing...
Hint: Format is TIME:CHAR
Char 0: Time is 19:53:40, 052th day of 2016 +- 30 seconds and the hash is: f7417f29f9760d97724c6f5c575a26b3dcaf39ef
1264373473:I
Nope, that's not the right solution. Try again later!
Connection closed by foreign host.
```

It was rather obvious that our task was to find a character (CHAR) and the time of hashing (TIME), such that the SHA1 digest of both (TIME:CHAR) was equal to the one given.

The annoying part were the format of the TIME and the timezone (the second hint was only added after we solved the challenge).

Usualy such challenges consist of multiple levels, so we again automated the solving using the beloved [pwntools/binjitsu](https://binjit.su).

Except for the guessing of format (Unix-Timestamp), timezone (CET) and some parsing, the main bruteforcing looked like this:

```python
        for offset in range(0, 62):
            for CHAR in string.printable:
                TIME = str(timestamp + offset)
                text = TIME + ':' + CHAR
                if digest == get_SHA(text):
                    log.info('Solution: ' + text)
                    r.sendline(text)
                    flag += CHAR
```

After 31 rounds, we owned the flag:

```
IW{M4N_Y0U_C4N_B3_BF_M4T3RiAL!}
```

The whole python code used to solve this challenge can be found [on GIST](https://gist.github.com/stefan2904/4c8d2a7652a4e739525d)

## Other write-ups and resources

* <https://forum.xeksec.com/f138/t88656/>
* [P4 Team](https://github.com/p4-team/ctf/tree/master/2016-02-20-internetwache/ppc_80)
* <http://losfuzzys.github.io/writeup/2016/02/22/iwctf2016-bruteforce/>
* <https://github.com/Execut3/CTF/tree/master/Participated-CTF/2016/InternetWache/coding/code80>
* <https://github.com/raccoons-team/ctf/tree/master/2016-02-20-internetwache-ctf/code80>
