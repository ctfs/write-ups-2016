# NCL 2016 : Passwords-1-75

__Category__: Crypto

__Points__: 75

## Write-up

<a href="https://jhalon.github.io/images/nclp-1.png"><img src="https://jhalon.github.io/images/nclp-1.png"></a>

--

__0x3736736f72746c6f76653231__

Taking a look at this password, we can tell that it's in HexDecimal due to the 0x at the beginning. We can easily convert this to ASCII in out Terminal.

```console
root@kali:~# echo 0x3736736f72746c6f76653231 | xxd -r
76sortlove21
```

__Answer: 76sortlove21__

--

__MjN3cml0dGVuY2hhbmdlNDM=__

The "__=__" at the end of the file should be a clue that this is a base64 encoded password. We can decode it in our Terminal.

```console
root@kali:~# echo MjN3cml0dGVuY2hhbmdlNDM= | base64 --decode
23writtenchange43
```

__Answer: 23writtenchange43__

--

__00110100 00110001 01100011 01101111 01101111 01101011 01110011 01110100 01100001 01110010 00110111 00110010__

Just go to this [Binary to Ascii Converter](http://www.binaryhexconverter.com/binary-to-ascii-text-converter) and you will get the answer.

__Answer: 41cookstar72__

--

__TkRadlluTmxjblpsYzJWMIpYSmhiRE16__

This one was pretty interesting, it took me a little bit to figure out what encoding this was, after a while I figured out that this was double base64 encoded. So we can simply decode this in our Terminal two times.

```console
root@kali:~# echo TkRadlluTmxjblpsYzJWMIpYSmhiRE16 | base64 --decode
NDZvYnNlcnZlc2V0XJhbDMz
root@kali:~# echo NDZvYnNlcnZlc2V0XJhbDMz | base64 --decode
46observeset\�[
               �base64: invalid input
```

__Answer: 46observeset__

--

## Other Write-ups and Resources

* https://jhalon.github.io/ncl-regular-season-1/
