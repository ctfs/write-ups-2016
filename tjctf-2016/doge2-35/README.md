# tjctf-2016 : doge2-35

**Category:** Forensics**Points:** 35
**Description:** Do the red colors look a little bit odd in this picture to you?

## Write-up

Because the question points to the red bits, any experienced CTF'er knows this is a reference to least significant bit (LSB) steganography. LSB steganography operates by taking the end of RGB values (only red this time), representing them in binary form (0 - 255), then changing the last bit to either a 0 or a 1 so that when one collects a the ends of all the red bytes, it will reveal either a text flag, or the contents of an image that displays the flag. In this case, running the image through [a trusty online steganography detector](http://incoherency.co.uk/image-steganography/#unhide), will present to you an image with the following flag: `tjctf{0dd5_4nd_3v3n5}`

## Other write-ups and resources

* [MilWestA - CTFtime.org](https://ctftime.org/task/2449)
