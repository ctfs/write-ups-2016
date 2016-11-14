# Hack the Vote CTF 2016 : topkek-50

**Category:** Crypto
**Points:**
**Solves:**
**Description:**

> A CNN reporter had only one question that she couldn't get off her mind&gt; Do we even know, who is this 4 CHAN???    So she set out to find who this 400lb hacker is. During her investigation, she came across this cryptic message on some politically incorrect forum online, can you figure out what it means?    [kek](<https://s3.amazonaws.com/hackthevote/kek.43319559636b94db1c945834340b65d68f90b6ecbb70925f7b24f6efc5c2524e.txt)>  author's irc nick: krx


## Write-up

Attacking this challenge from a computer-esque direction assumes `TOP` is `1` and `KEK` is `0`. Because they never repeat directly after another, it appears the varying quantity of exclamation points following each `TOP` or `KEK` indicate how many times that digit is used. We don't know which is `0` and which is `1` so we had to switch between until it came out correctly. Here is a Python script (courtesy [John Hammond](https://github.com/USCGA)) that will decipher the text:

```python
import binascii

reader = open("kek.txt", "r")
contents = reader.read()
reader.close()

parts = contents.split()
output = []
for part in parts:
  if "KEK" in part:
    character = "0"
  else:
    character = "1"
  multiplier = part.count("!")
  output.append(character * multiplier)
  end = "".join(output)
  print("".join([chr(int(end[i:i + 8], 2)) for i in range(len(end), 8)]))
```

Executing this script on the ciphertext file should provide you with the flag:

`flag{T0o0o0o0o0P______1m_h4V1nG_FuN_r1gHt_n0W_4R3_y0u_h4v1ng_fun______K3K!!!}`

## Other write-ups and resources

* [Rawsec](http://rawsec.ml/en/Hack-The-Vote-2016-50-topkek/)
* [Aneesh Kotnana](https://github.com/Alaska47/HackTheVote-2016-Writeups/tree/master/crypto/50-TOPKEK)
* [Harvey Hunt](https://github.com/HarveyHunt/ctfs/blob/master/2016/hackthevote/crypto/topkek/topkek.md)
* [Carl Loendahl](https://github.com/grocid/CTF/tree/master/Hack%20the%20vote/2016#topkek-50-p)
* https://s3.amazonaws.com/hackthevote/kek.43319559636b94db1c945834340b65d68f90b6ecbb70925f7b24f6efc5c2524e.txt
* [United States Coast Guard Academy](https://github.com/USCGA/writeups/tree/master/online_ctfs/hackthevote2016/crypto50)
* [P4 Team](https://github.com/p4-team/ctf/tree/master/2016-11-05-hack-the-vote/kek_crypto_50)
