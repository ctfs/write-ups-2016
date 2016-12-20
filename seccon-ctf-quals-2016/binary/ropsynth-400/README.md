# SECCON CTF QUALS 2016 : ropsynth

**Category:** Binary
**Points:** 400
**Solves:** 34
**Description:**

    ropsynth
    ropsynth.pwn.seccon.jp:10000
    Read "secret" and output the content such as the following code.

    ==
    fd = open("secret", 0, 0);
    len = read(fd, buf, 256);
    write(1, buf, len);
    ==

## Files

dist.tgz was the download for the challenge.

ropsynth_blobs.tgz is a collection of 100 base64 blobs returned from the ropsynth server. These may be useful in your testing as the gadget_generator package was not available to competitors. 

## Write-up

(TODO)

## Other write-ups and resources

