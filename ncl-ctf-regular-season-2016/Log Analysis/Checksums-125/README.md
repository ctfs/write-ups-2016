# NCL 2016 : Checksums-125

__Category__: Log Analysis

__Points__: 125

## Write-up

<a href="https://jhalon.github.io/images/nclp-3.png"><img src="https://jhalon.github.io/images/nclp-3.png"></a>

For this challenge we are provided the following file: [NCL-2016-Game2-CorruptedHash.txt](https://jhalon.github.io/download/NCL-2016-Game2-CorruptedHash.txt)

--

__How many unique entries are there in this log?__

```console
root@kali:~# cd Downloads/
root@kali:~/Downloads# cat NCL-2016-Game2-CorruptedHash.txt 
623d9157017ca3805cbbca653724f8e25a52be689f821d0c608f94717342e1e2  node-v0.1.100.tar.gz
44b08c5c9bd0c23d79d447bc67e1767ec1350a02cec0da6e5ce4c7f790b4e773  node-v0.1.101.tar.gz
bd9b1d09ad40ceaef4bdd46019960c5c2fe87026c9598a6fb23c66457510a22d  node-v0.1.102.tar.gz
7482b898a0f9514c74137b490c3ad0810ee5ce1586e8886c5182f6446e56711e  node-v0.1.103.tar.gz
a1c776f44bc07305dc0e56df17cc3260eaafa0394c3b06c27448ad85bec272df  node-v0.1.104.tar.gz
---snip---
```

```console
root@kali:~/Downloads# cat NCL-2016-Game2-CorruptedHash.txt | sort | uniq -u | wc -l
5012
```

__Answer: 5012__

--

__What is the first file entry that does not match the official checksum?__

Here is where it gets a little hard. First we have to navigate to the [NodeJS Distribution Page](https://nodejs.org/dist/). This page contains all the Checksums per version.

<a href="https://jhalon.github.io/images/ncl-nj-1.png"><img src="https://jhalon.github.io/images/ncl-nj-1.png"></a>

In each version link we will have something called __SHASUMS256.txt__.

<a href="https://jhalon.github.io/images/ncl-nj-2.png"><img src="https://jhalon.github.io/images/ncl-nj-2.png"></a>

This text contains the SHA256 Hash Checksum for each "official" version, which will look like something below...

```
623d9157017ca3805cbbca653724f8e25a52be689f821d0c608f94717342e1e2  node-v0.1.100.tar.gz
```

From here we need to grab each Hash Text File and compare it to the Corrupted Hash file we have. To accomplish this, we will use a tool called [WGET](https://www.gnu.org/software/wget/) to grab the contents of each file and print them out to a text file.

We will thus run the following command, which will grab each version file -- this might take a while, so let it run!

```console
root@kali:~# wget -O - https://nodejs.org/dist/v{0..7}.{0..12}.{0..48}/SHASUMS256.txt >> file

--2016-11-20 14:42:59--  https://nodejs.org/dist/v0.0.0/SHASUMS256.txt
Resolving nodejs.org (nodejs.org)... 104.20.22.46, 104.20.23.46, 2400:cb00:2048:1::6814:172e, ...
Connecting to nodejs.org (nodejs.org)|104.20.22.46|:443... connected.
HTTP request sent, awaiting response... 404 Not Found
2016-11-20 14:42:59 ERROR 404: Not Found.

--2016-11-20 14:42:59--  https://nodejs.org/dist/v0.0.1/SHASUMS256.txt
Reusing existing connection to nodejs.org:443.
HTTP request sent, awaiting response... 404 Not Found
2016-11-20 14:43:00 ERROR 404: Not Found.

---snip---
```

Once that's completed... you will have a full listing of all the SHA256 Check Sums in the file called "__file__"

What I did to make life easy was go to [QuickDiff](http://www.quickdiff.com/) to compare the list we made against the Corrupted Hashes we downloaded. Now all we need to do is scroll down the list and find the RED/GREEN highlights, which will be our answer.

<a href="https://jhalon.github.io/images/ncl-nj-3.png"><img src="https://jhalon.github.io/images/ncl-nj-3.png"></a>

__Answer: node-v4.0.0-darwin-x64.tar.gz__

--

__What is the second file entry that does not match the official checksum?__

If we keep scrolling, we will find the 2nd one toward the bottom of the page.

<a href="https://jhalon.github.io/images/ncl-nj-4.png"><img src="https://jhalon.github.io/images/ncl-nj-4.png"></a>

__Answer: node-v7.1.0.pkg__

--

## Other Write-ups and Resources

* https://jhalon.github.io/ncl-regular-season-1/
