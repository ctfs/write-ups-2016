# IceCTF-2016 : flag-storage-50

**Category:** Web
**Points:** 50
**Description:**

What a cheat, I was promised a flag and I can't even log in. Ca you get in for me? flagstorage.buln.icec.tf. They seem to hash their passwords, but I think the problem is somehow related to [this](https://en.wikipedia.org/wiki/SQL_injection)

## Writeup

Normally, passwords are sent to the server encrypted only through SSL/TLS to ther server, where they are sanitized, hashed, and compared. However, looking through the source code, it is apparent that a JavaScript function exists to SHA-256 hash the password before it is sent to the server (we can assume they don't hash again on server). Logging in with any creds, and analyzing the POST request reveals the hash `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`, which from reasearch, is the hash of a null string. We need to keep the same hash, but with a different, malicious password. Either by editing the POST request as it's sent, or with `curl` filtered by `grep`:
```
curl -s -iL flagstorage.vuln.icec.tf/login.php -d "username=admin&password=1'+OR+'1'='1&password_plain=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"|grep IceCTF
```

will filter out `IceCTF{why_would_you_even_do_anything_client_side}`

## Other write-ups and resources

* [RawSec](https://rawsec.ml/en/IceCTF-50-Flag-Storage-Web/)
* https://github.com/318BR/IceCTF/tree/master/2016/Stage2/Flag_Storage
* https://github.com/TeamContagion/CTF-Write-Ups/tree/master/icectf-2016/Web/Flag%20Storage
* https://www.youtube.com/watch?v=-_tdCiwBuco&feature=youtu.be
