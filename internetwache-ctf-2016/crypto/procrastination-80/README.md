# Internetwache CTF 2016 : Procrastination

**Category:** Crypto
**Points:** 80
**Solves:** 47
**Description:**

> Description: Watching videos is fun! Hint: Stegano skills required.
>
>
> Attachment: [crypto80.zip](./crypto80.zip)
>
>
> Service: <https://procrastination.ctf.internetwache.org>

Sources: <https://github.com/internetwache/Internetwache-CTF-2016/tree/master/tasks/crypto80/code/website>

## Write-up

**by [LosFuzzys](https://hack.more.systems)**

Given was a website including a `song.webm` file. Running `mediainfo` got us the hint,
that there is a second audio trace inside the file.
We used `ffmpeg` to receive the audio file in `wav` format:

```
ffmpeg -i song.webm -map 0:2 out.wav
```

After listening to it, we concluded that it must be some dial-up noise. So we ran some DTMF analysis.

```
multimon-ng -t wav -a DTMF out.wav
```

This gave us some numbers separated by zeros:

```
111 127 173 104 122 60 116 63 123 137 127 61 124 110 137 120 110 60 116 63 123
```

We knew that it must be something like `IW{..}`.
So we looked in the ASCII Table and saw that this must be some OCT representation.


So the flag was `IW{DR0N3S_W1TH_PH0N3S}`.


## Other write-ups and resources

* <https://www.xil.se/post/internetwache-2016-crypto-80-arturo182/>
* [0x90r00t](https://0x90r00t.com/2016/02/22/internetwache-ctf-2016-crypto-80-procrastination-write-up/)
* <http://losfuzzys.github.io/writeup/2016/02/22/iwctf2016-procrastination/>
* <https://github.com/WesternCyber/CTF-WriteUp/blob/master/2016/Internetwache/Crypto/Crypto80.md>
* <http://sexyplatypussies.com/writeups/InternetwacheCTF2016/crypto80.txt>
* <https://blog.amishsecurity.com/-crypto80-procrastination/>
