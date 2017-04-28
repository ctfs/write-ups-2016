# ABCTF 2016 : just-open-it-15

**Category:** Forensic
**Points:** 15
**Solves:** 545
**Description:**

I'm almost positive we put a flag in this file. Can you find it for me?
[HINT] So many editors out there!

## Write-up

Opening the image in a regular image viewer presents a normal wordle-type image with competition and flag related words. However there is an obviously horizontal anomaly in the image, consistent with inserting a string of text into the image file's contents. Opening this file in a text editor or a hex editor (notepad for Windows or leafpad for Linux) and searching for the substring `ABCTF` in the file should reveal the flag. Unix users can use the `grep` command to search files for strings.

`grep "ABCTF" just_open_it.jpg` or `strings just_open_it.jpg | grep ABCTF`

This should reveal `ABCTF{forensics_1_tooo_easy?}`

## Other write-ups and resources

* [RawSec](https://rawsec.ml/en/ABCTF-15-Just-open-it-Forensics/)
* [RedShield5](https://ctftime.org/writeup/3572)
* [OMECA](https://github.com/nbrisset/CTF/blob/master/abctf-2016/challenges/just-open-it-15)
