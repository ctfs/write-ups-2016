# Sharif University CTF 2016 : We lost the Fashion Flag!

**Category:** Forensics
**Points:** 100
**Solves:** 132
**Description:**

> In Sharif CTF we have lots of task ready to use, so we stored their data about author or creation date and other related information in some files. But one of our staff used a method to store data efficiently and left the group some days ago. So if you want the flag for this task, you have to find it yourself!
>
> Download [fashion.tar.gz](./fashion.tar.gz)


## Write-up

by [Jashan Bhoora](https://github.com/jashanbhoora)

We are given a single file for the challenge: `fashion.tar.gz`

```
file fashion.tar.gz
fashion.tar.gz: gzip compressed data, from Unix, last modified: Thu Feb  4 18:22:33 2016
```

Seems to be pretty standard, so I decompress it (`tar xvzf fashion.tar.gz`), yielding another archive called `sharif_tasks.tgz` and a file called `fashion.model`

```
file sharif_tasks.tgz
sharif_tasks.tgz: gzip compressed data, from Unix, last modified: Mon Dec 21 09:19:30 2015
```

```
file fashion.model
fashion.model: data
```

I decided to look at the `fashion.model` file first. Opening it in `ghex`, it seems to contain hundreds of JSON style entries, and some random bytes filling the end of the file. The most useful part is the header of the file, which mentions "FemtoZip". A quick search for femtozip leads me to a [Github Repository](https://github.com/gtoubassi/femtozip "FemtoZip Github Repository"), that explains that FemtoZip is "a 'shared dictionary' compression library optimized for small documents that may not compress well with traditional tools such as gzip."

Assuming that I would need it later, I installed it and moved on to the tgz.
Decompressing the tgz (`tar xvzf sharif_task.tgz`) yields a single folder `out` with 12,431 files in it, numbered sequentially. Each is around 20-30 bytes in size and contains nothing resembling a flag.

Guessing that the files may each have been compressed with FemtoZip, I started reading the FemtoZip Wiki to see how you decompress its output.
On the third point on the tutorial, I find the command to decompress a folder of files using a model. We seem to have both parts, so I attempt the same command.

```
./fzip --model fashion.model --decompress out/
```

Success! Each file in `out` decompressed into a text file containing a single JSON object with 7 attributes:

e.g. file `0`
{'category': 'pwn', 'author': 'staff_3', 'challenge': 'Fashion', 'flag': 'SharifCTF{c6790c36aab123a82323865ef149afd4}', 'ctf': 'Shairf CTF', 'points': 55, 'year': 2013}

e.g. file `18`
{'category': 'forensic', 'author': 'staff_5', 'challenge': 'Fashion', 'flag': 'SharifCTF{15fea9e049540c22a9fac943c1f84d17}', 'ctf': 'Shairf CTF', 'points': 135, 'year': 2012}

Considering the brief of the challenge, these files should be make up a "catalogue" for the flags used in each Sharif CTF. Therefore, I figured that if we could narrow down the JSON objects to one that was applicable to this challenge, we would find the correct flag.

I used a series of quick and dirty greps to do this. First, take all the files and copy their string into one file, one per line:

```
nl out/* > all.txt
```

then wittle down the entries using a different attribute each time...

```
cat all.txt | grep "forensic" | grep "Fashion" | grep ": 2016" | grep ": 100" > final.txt

cat final.txt

1316    {'category': 'forensic', 'author': 'staff_3', 'challenge': 'Fashion', 'flag': 'SharifCTF{2b9cb0a67a536ff9f455de0bd729cf57}', 'ctf': 'Shairf CTF', 'points': 100, 'year': 2016}
1364  {'category': 'forensic', 'author': 'staff_5', 'challenge': 'Fashion', 'flag': 'SharifCTF{41160e78ad2413765021729165991b54}', 'ctf': 'Shairf CTF', 'points': 100, 'year': 2016}
2124  {'category': 'forensic', 'author': 'staff_2', 'challenge': 'Fashion', 'flag': 'SharifCTF{8725330d5ffde9a7f452662365a042be}', 'ctf': 'Shairf CTF', 'points': 100, 'year': 2016}
4356  {'category': 'forensic', 'author': 'staff_3', 'challenge': 'Fashion', 'flag': 'SharifCTF{1bc898076c940784eb329d9cd1082a6d}', 'ctf': 'Shairf CTF', 'points': 100, 'year': 2016}
11769  {'category': 'forensic', 'author': 'staff_6', 'challenge': 'Fashion', 'flag': 'SharifCTF{c19285fd5d56c13b169857d863a1b437}', 'ctf': 'Shairf CTF', 'points': 100, 'year': 2016}
```

Great! Just 5 potential flags from 12,431! I set about attempting to submit them, and found first one to be the answer!

Fun bit of detective work!

Flag: SharifCTF{2b9cb0a67a536ff9f455de0bd729cf57}

## Other write-ups and resources

* <https://github.com/gtoubassi/femtozip>
* <https://www.xil.se/post/sharifctf-2016-forensics-fashion-flag-arturo182/>
* <https://github.com/ctfs/write-ups-2016/tree/master/su-ctf-2016/forensics/we-lost-the-fashion-flag-100>
* [0x90r00t](https://0x90r00t.com/2016/02/09/sharif-university-ctf-2016-forensic-100-we-lost-the-fashion-flag-write-up/)
