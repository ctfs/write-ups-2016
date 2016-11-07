# IceCTF-2016 : vape-nation-50

**Category:** Stego
**Points:** 50
**Description:**

Go Green!

## Writeup

We are given a .PNG image file, which (to any casual CTF competitor) should suggest trying [steganography](https://en.wikipedia.org/wiki/Steganography#Digital_messages). I ran a Python script called [`Stegpy`](https://github.com/Baldanos/Stegpy) with Linux (can also be run with Windows or Mac with Python installed)

`sudo ./stegpy -V vape_nation_7d550b3069428e39775f31e7299cd354c721459043cf1a077bb388f4f531d459.png`

Because no clear text appears normally, choose the `Reversed colors view` where the flag `IceCTF{420_CuR35_c4NCEr}` should be vary evident. The reversed colors option ensures the script is reading from the green channel, alluded to in the challenge description.

## Other write-ups and resources

* [RawSec](https://rawsec.ml/en/IceCTF-50-Vape-Nation-Stego/)
* https://bryceandress.github.io/2016/08/27/Vape-Nation.html
* https://github.com/Idomin/CTF-Writeups/blob/master/IceCTF/VapeNation-Stego-50
* https://github.com/JosiahPierce/writeups/blob/master/IceCTF2016:Vape_Nation.md
* https://github.com/Ctf-Trinidad/WRITEUPS/tree/master/2016.08.IceCTF/VapeNation
* https://github.com/bburky/mathematica-ctf-writeups/blob/master/LSB%20image/
* http://wumb0.in/icectf-2016-vape-nation.html
* https://github.com/bburky/mathematica-ctf-writeups/blob/master/LSB%20image/
* https://www.youtube.com/watch?v=rOY4SMmTYQI
