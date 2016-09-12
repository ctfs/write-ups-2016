# IceCTF-2016 : rsa-50

**Category:** Crypto
**Points:** 50
**Description:**

John was messing with RSA again... he encrypted our flag! I have a strong feeling he had no idea what he was doing however, can you get the flag for us? flag.txt

## Writeup

Using the [wikipedia page for RSA](https://en.wikipedia.org/wiki/RSA_%28cryptosystem%29) as reference, `p` and `q` are our two prime numbers which multiply to make the public modulus `N`. The letter `c` represents the encryption key, and letter `d` represents the decryption key. In terms of math, the modulus operator uses two numbers, ex. `A mod B` (or in programming usually `A % B`). This operator divides `A` by `B` and returns the remainder. Therefore, `11 mod 5` would equal `1`, because `5` goes into `11` twice (to make 10) and has a remainder of `1` (`11 - 10`). Modulus is an useful operator only when `A` is greater than `B`. The description mentions John doesn't know what he is doing with RSA, which is evident in the cipher. Wikipedia tells us the following formulas:

```
N = p * q
e * d = 1 mod phi
phi = p * q
```

We have `N`, `e`, and `c` from [`flag.txt`](flag.txt). We call see that `e` is `1` (which is just converting hexadecimal to decimal). So we can fill in part of the equation so that `1 * d = 1 mod phi`, which simplifies to `d = 1 mod phi`. Also, since `N = p * q` and `N` is a very large number, it is safe to assume that `p` and `q` are relatively large prime numbers. Therefore, it's possible to imagine `phi` is also a large number based on `p` and `q` (definately larger than `1`). Since `d = 1 mod phi`, and we assume `phi` is larger than 1, we know the modulus operation will simply return `1` because the right side is greater than the left. This is where John went wrong. Now, `d = 1`. With this decryption key, it is mathematically reasonable to do it by hand, but computers were invented for a reason; WCSC suggests you use the [online RSA tool](http://nmichaels.org/rsa.py). Simply enter `N` for the `Public Modulus` field, `e` for the `Public Exponent` field, `d` for the `Private Exponent` field, and lastly `c` in the `Text` field. Don't forget to check the `Hexadecimal` radio button before hitting `Decrypt`. The text field should then output `IceCTF{falls_apart_so_easily_and_reassembled_so_crudely}`

## Other write-ups and resources

* https://github.com/WCSC/writeups/tree/master/icectf-2016/RSA1
* https://capturetheflags.blogspot.in/2016/08/icectf-2016-rsa.html
* [Japanese](https://ctftime.org/writeup/3811)
* https://github.com/grocid/CTF/tree/master/IceCTF/2016#rsa-50-p
* https://www.youtube.com/watch?v=k9hiLH3i9Rw&feature=youtu.be
