# NCL 2016 Preseason : Passwords-1-45

__Category__: Crypto

__Points__: 45

## Write-up

<a href="https://jhalon.github.io/images/ncl4.png"><img src="https://jhalon.github.io/images/ncl4.png"></a>

--

__0x616761696e74687265653538__

We can tell that this password is in Hex format due to the __0x__ at the start of the password. We can covert the hex to ASCII in Linux by simply running the following command.

```console
root@kali:~# echo 0x616761696e74687265653538 | xxd -r -p
againthree58
```

And there we have it. The output is our password!

__Answer: againthree58__

--

__cGVvcGxlY3Jvd2Q1MQ==__

This password was [Base64 Encoded](https://en.wikipedia.org/wiki/Base64). We can decode it in our Linux terminal.

```console
root@kali:~# echo cGVvcGxlY3Jvd2Q1MQ== | base64 --decode
peoplecrowd51
```

__Answer: peoplecrowd51__

--

__01101101 01100001 01110100 01110100 01100101 01110010 01110011 01100001 01101001 01101100 00110110 00110010__

This password was in binary form. You can go [BinaryHexConverter](http://www.binaryhexconverter.com/binary-to-ascii-text-converter) and convert it to ASCII.

__Answer: mattersail62__

--

## Other Write-ups and Resources

* [Jack Halon - KKB](https://jhalon.github.io/ncl-crypto/)
