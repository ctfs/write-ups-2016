# sCTF 2016 Q1 : pythagoras-hash-100

**Category:** Crypto
**Points:** 100
**Solves:** 9
**Description:**
You have part of the source to a really bad hash function, and an oracle that will hash anything up to 32 bytes. Hash the following string.

the flag the flag the flag the flag the flag the flag the flag the game

*(71 bytes — sorry, the oracle will not hash it for you)*

You may access the oracle at <http://problems1.2016q1.sctf.io:17117/>. The oracle accepts a base64-encoded input passed via the query string. You can interface with the oracle using your browser (e.g. <http://problems1.2016q1.sctf.io:17117/?dGhlIGZsYWc=)>, cURL, or anything you want, really.

    $ hash() { curl 'http://problems1.2016q1.sctf.io:17117/?'\"$(echo -n $1 | base64)\"; }
    $ hash 'the flag'
    d0d27218a363a192


SHA512 Solution Hash(es):
* f066d440d0184c9beb3d6d939fa7c950b1d5eaa8bce6b12fca30b0d1315f4dbce95aed328b0a2576aa548016e922555690285d270e3cb5569e45b77ce675fc84

**Hint**
Sliding window

## Write-up

(TODO)

## Other write-ups and resources

* none yet
