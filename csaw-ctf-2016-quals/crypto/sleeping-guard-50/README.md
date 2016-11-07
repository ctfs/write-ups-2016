# CSAW CTF 2016 Quals: Sleeping_Guard

**Category:** Crypto
**Points:** 50
**Solves:**
**Description:**

Only true hackers can see the image in this magic PNG....

## Write-up

Answer:
(flag printed in the decrypted magic.png file)
flag{l4zy_H4CK3rs_d0nt_g3T_MAg1C_FlaG5}

Organizer Description:
    This challenge is a server which sends you a base64 encoded PNG image. The hint is given in the title to solve this. First that the encoding mechanism is a Xor and the way to decrypt is use the fact that all PNG's have the same first 12 byte headers.

To distribute:
    sleeping_49d06c703032f66151ae07066d509c61.py  (md5sum appended)

Setup:
    Distrubute the server code after REMOVING the encryption key used in the Xor.
    Server side run the server with the correct key in it.

Hints:
    Possible hints are look at the title for clues. All files have same magic header.

Solution Script:
    Attached is the solution script to recover the key to xor with.

## Other write-ups and resources

* https://github.com/grocid/CTF/tree/master/CSAW/2016
* http://www.megabeets.net/csaw-2016-sleeping-guard-writeup/
* [P4 Team](https://github.com/p4-team/ctf/tree/master/2016-09-16-csaw/sleeping_guard)
* https://github.com/73696e65/ctf-notes/blob/master/2016-ctf.csaw.io/crypto-50-sleeping_guard.md
* https://github.com/grocid/CTF/tree/master/CSAW/2016#sleeping-guard-50-p
* https://crackinglandia.wordpress.com/2016/09/21/csaw-ctf-2016-qualification-round-crypto-sleeping-guard-50-pts/
* https://binarystud.io/csaw-2016-sleeping-guard-writeup.html
