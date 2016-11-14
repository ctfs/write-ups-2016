# EKOPARTY CTF 2016 : metadata-50

**Category:** FBI
**Points:** 50
**Solves:** 311
**Description:**

> Help me to find some metadata!
> `https://silkroadzpvwzxxv.onion`

## Write-up

Some quick Googling reveals `.onion` domains can only be opened with `Tor`. Downloading, installing, and running Tor and navigating to the provided URL gets us to this fake Silk Road website. Metadata is always found in the developer tools, so pressing `Ctrl + Shift + Q` opens this toolbar, and browsing through different components should reveal their certificate contains the flag.

## Other write-ups and resources

* https://youtu.be/0LOKdINpK6M
* [0day](https://0day.work/ekoparty-ctf-2016-writeups/)
* http://yuelab82.hatenablog.com/entry/ekoparty2016_writeup
* [Tech Hacks](https://nacayoshi00.wordpress.com/2016/10/28/ekoparty-ctf-2016-writeup/)
* [P4 Team](https://github.com/p4-team/ctf/blob/master/2016-10-26-ekoparty/fbi_50/README.md)
* https://github.com/burlingpwn/writeups/tree/master/EKOPARTY-CTF-2016/FBI/Metadata
