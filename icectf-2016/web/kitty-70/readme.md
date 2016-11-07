# IceCTF-2016 : kitty-70

**Category:** Web
**Points:** 70
**Description:**

They managed to secure their website this time and moved the hashing to the server :(. We managed to leak this hash of the admin's password though! c7e83c01ed3ef54812673569b2d79c4e1f6554ffeb27706e98c067de9ab12d1a. Can you get the flag?kitty.vuln.icec.tf

## Writeup

Before running against known hashes, use [a hash identifier](http://www.onlinehashcrack.com/hash-identification.php)
to get some good guesses at the has algorithm. Start with the most popular hashing algorithms like `SHA-256` and `Haval` because to find a known hash, you'd need a commonly used hash. The website [MD5decrypt](http://md5decrypt.net/en/Sha256/) has a SHA-256 hash cracker so paste the hash into the input. Solve the CAPTCHAs and it should output `Vo83*`. Use this to login to the website as `admin`, and the cracked password for the password, and the flag `IceCTF{i_guess_hashing_isnt_everything_in_this_world}` should appear.

## Other write-ups and resources

* [RawSec](https://rawsec.ml/en/IceCTF-70-Kitty-Web/)
* https://github.com/WCSC/writeups/tree/master/icectf-2016/kitty
* https://github.com/grocid/CTF/tree/master/IceCTF/2016#kitty-80-p
* https://github.com/TeamContagion/CTF-Write-Ups/blob/master/icectf-2016/Web/Kitty
* [Japanese](https://ctftime.org/writeup/3812)
* https://github.com/burlingpwn/writeups/tree/master/IceCTF-2016/kitty
