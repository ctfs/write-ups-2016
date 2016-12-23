# SECCON CTF Quals 2016 : ropsynth-400

**Category:** Binary
**Points:** 400
**Solves:** 34
**Description:**

ropsynth.pwn.seccon.jp:10000
Read "secret" and output the content such as the following code.

    ==
    fd = open("secret", 0, 0);
    len = read(fd, buf, 256);
    write(1, buf, len);
    ==

[dist.tgz](dist.tgz)

## Write-up

(TODO)

## Other write-ups and resources

* https://tasteless.eu/post/2016/12/seccon-ropsynth/
