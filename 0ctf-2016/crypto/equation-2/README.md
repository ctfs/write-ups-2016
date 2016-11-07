# 0CTF : equation-2

**Category:** Crypto
**Points:** 2
**Solves:** 44
**Description:**

> Here is a RSA private key with its upper part masked. Can your recover the private key and decrypt the file?


## Write-up

We are given the following picture of a fragment of the RSA private key.

![Private Key Fragment](https://github.com/p4-team/ctf/blob/master/2016-03-12-0ctf/equation/mask.png?raw=true)

which displays the following bse64 string:

```
Os9mhOQRdqW2cwVrnNI72DLcAXpXUJ1HGwJBANWiJcDUGxZpnERxVw7s0913WXNtV4GqdxCzG0pG5EHThtoTRbyX0aqRP4U/hQ9tRoSoDmBn+3HPITsnbCy67VkCQBM4xZPTtUKM6Xi+16VTUnFVs9E4rqwIQCDAxn9UuVMBXlX2Cl0xOGUF4C5hItrX2woF7LVS5EizR63CyRcPovMCQQDVyNbcWD7N88MhZjujKuSrHJot7WcCaRmTGEIJ6TkU8NWt9BVjR4jVkZ2EqNd0KZWdQPukeynPcLlDEkIXyaQx
```

In order to determine what information we have and what we don't, we need to figure out the structure through which the components of an RSA Private key are encoded. I began with a Google search for `RSA private key encoding`, and was able to establish these keys are encoded under the ISO (International Standards Organization) standard [`Abstract Syntax Notation One (ASN.1)`](https://en.wikipedia.org/wiki/Abstract_Syntax_Notation_One#Example_encoded_in_DER). The same Google results show RSA private keys (and most cryptographics) use a specific syntax form named [`Distinguished Encoding Rules (DER)`](https://en.wikipedia.org/wiki/X.690#DER_encoding). In order to ascertain the specific structure of RSA private keys, I made a second Google search: `ANS1 DER RSA private key structure`. One of the first results was [this page](https://tls.mbed.org/kb/cryptography/asn1-key-structures-in-der-and-pem) which sounded promising. Scrolling down two thirds of the page shows me this code block:

```
-----BEGIN RSA PRIVATE KEY-----
BASE64 ENCODED DATA
-----END RSA PRIVATE KEY-----
```
Look familiar? And right below it, I am shown the structure of the RSA private key:

```
RSAPrivateKey ::= SEQUENCE {
  version           Version,
  modulus           INTEGER,  -- n
  publicExponent    INTEGER,  -- e
  privateExponent   INTEGER,  -- d
  prime1            INTEGER,  -- p
  prime2            INTEGER,  -- q
  exponent1         INTEGER,  -- d mod (p-1)
  exponent2         INTEGER,  -- d mod (q-1)
  coefficient       INTEGER,  -- (inverse of q) mod p
  otherPrimeInfos   OtherPrimeInfos OPTIONAL
}
```

Remember we said the string of text from the image was base64? Well to be able to pull the components from the data, we need to convert it to the computer's most basic encoding; binary. This is what we get:

```
00111010 11001111 01100110 10000100 11100100 00010001 01110110 10100101 10110110 01110011 00000101 01101011 10011100 11010010 00111011 11011000 00110010 11011100 00000001 01111010 01010111 01010000 10011101 01000111
00011011 00000010 01000001 00000000 11010101 10100010 00100101 11000000 11010100 00011011 00010110 01101001
10011100 01000100 01110001 01010111 00001110 11101100 11010011 11011101 01110111 01011001 01110011 01101101
01010111 10000001 10101010 01110111 00010000 10110011 00011011 01001010 01000110 11100100 01000001 11010011
10000110 11011010 00010011 01000101 10111100 10010111 11010001 10101010 10010001 00111111 10000101 00111111
10000101 00001111 01101101 01000110 10000100 10101000 00001110 01100000 01100111 11111011 01110001 11001111
00100001 00111011 00100111 01101100 00101100 10111010 11101101 01011001 00000010 01000000 00010011 00111000
11000101 10010011 11010011 10110101 01000010 10001100 11101001 01111000 10111110 11010111 10100101 01010011
01010010 01110001 01010101 10110011 11010001 00111000 10101110 10101100 00001000 01000000 00100000 11000000
11000110 01111111 01010100 10111001 01010011 00000001 01011110 01010101 11110110 00001010 01011101 00110001
00111000 01100101 00000101 11100000 00101110 01100001 00100010 11011010 11010111 11011011 00001010 00000101
11101100 10110101 01010010 11100100 01001000 10110011 01000111 10101101 11000010 11001001 00010111 00001111
10100010 11110011 00000010 01000001 00000000 11010101 11001000 11010110 11011100 01011000 00111110 11001101
11110011 11000011 00100001 01100110 00111011 10100011 00101010 11100100 10101011 00011100 10011010 00101101
11101101 01100111 00000010 01101001 00011001 10010011 00011000 01000010 00001001 11101001 00111001 00010100
11110000 11010101 10101101 11110100 00010101 01100011 01000111 10001000 11010101 10010001 10011101 10000100
10101000 11010111 01110100 00101001 10010101 10011101 01000000 11111011 10100100 01111011 00101001 11001111
01110000 10111001 01000011 00010010 01000010 00010111 11001001 10100100 00110001
```

 To understand the binary, we also need reference Wikipedia's page for [`ASN.1`](https://en.wikipedia.org/wiki/Abstract_Syntax_Notation_One#Example_encoded_in_DER) under the [Example encoded in DER](https://en.wikipedia.org/wiki/Abstract_Syntax_Notation_One#Example_encoded_in_DER) subheading. We already know from the block above nearly every component of this binary is representing integers. This `Example encoded in DER` section lets us know that every integer has `02` before it. This table is technically in hexadecimal, but we can do the hard conversion, where `02` in base6 (hexadecimal) converts to `00000010` in binary. We now go through and find all (4) instances of `00000010`. We know that `02` indicated the start of the integer, looking under that table, it reads:

 > Note: DER uses a pattern of [type-length-value triplets](https://en.wikipedia.org/wiki/Type-length-value), and uses well known byte constants for encoding type tags

 For each `00000010` in the binary string, we know the following value will be the integer length. The table has lists the units of the length value to be `length in octets of value that follows`, but since we converted to binary (and 1 octect = 8 bits = 1 byte) it will tell us the length of the integer in bytes. Looking back at our huge binary string, our first instance of `00000010` (our first visible RSA integer, which is the 26th byte) indicates the start of an integer. The next byte `01000001` (converted to base10/decimal) indicates the integer's value is the next `65` bytes (large number). Whether you work it by hand, or programmatically, the integer's value should be

 ```
 11,188,888,442,779,478,492,506,783,674,852,186,314,949,555,636,014,740,182,307,607,993,518,479,864,690,065,244,102,864,238,986,781,155,531,033,697,982,611,187,514,703,037,389,481,147,794,554,444,962,262,361
 ```

Doing this for each type-length-value triplet where the type is encoded is `00000010` should give you 3 decimal values.

> Why do you say 3 decimal values when `00000010` shows up 4 times?

> Because the length byte of the 3rd triplet says the next 65 bytes are part of the integer's value, meaning the next 65 bytes represent part of the value and shouldn't be treated as any indicator. So the 4th instance of `00000010` isn't indicating a new integer, but is part of the third integer's value.

Given three large integers, we can reference our aforementioned table, which says the last three integers are `exponent1`, `exponent2`, and `coefficient` which are `d mod (p-1)`, `d mod (q-1)`, and `(inverse of q) mod p` respectively. Note, the binary that appears before the start of the first integer start is part of `prime 2 (q)`, but the method we will use to recover the whole private key won't be helped through a fragment of the prime. To find a method of RSA private key recovery, I Google searched `RSA private key recovery` where I found [this blackhat slideshow](https://www.blackhat.com/docs/us-16/materials/us-16-Ortisi-Recover-A-RSA-Private-Key-From-A-TLS-Session-With-Perfect-Forward-Secrecy.pdf) which references the `Chinese Remainder Theorem (CRT)`. Understanding the [recovery algorithm](https://eprint.iacr.org/2004/147.pdf) itself would take some time to implement, but here's what an implementation would look like this:

```python
def recover_parameters(dp, dq, qinv, e):
    results = []
    d1p = dp * e - 1
    for k in range(3, e):
        if d1p % k == 0:
            hp = d1p // k
            p = hp + 1
            if is_prime(p):
                d1q = dq * e - 1
                for m in range(3, e):
                    if d1q % m == 0:
                        hq = d1q // m
                        q = hq + 1
                        if is_prime(q):
                            if (qinv * q) % p == 1 or (qinv * p) % q == 1:
                                results.append((p, q, e))
                                print(p, q, e)
    return results
```

Running that Python function given the three integers we found should give you

```
p=12883429939639100479003058518523248493821688207697138417834631218638027564562306620214863988447681300666538212918572472128732943784711527013224777474072569

q =12502893634923161599824465146407069882228513776947707295476805997311776855879024002289593598657949783937041929668443115224477369136089557911464046118127387

e = 65537
```

I then Googled `Decrypt RSA with p q e` which directed me to [this Stack Exchange page](http://crypto.stackexchange.com/questions/19444/rsa-given-q-p-and-e), listing the EGCD algorithm as the best option. Below is a Python implementation of the EGCD decryption algorithm (courtesy of [Pharisaeus](https://github.com/Pharisaeus)). The output?

`0ctf{Keep_ca1m_and_s01ve_the_RSA_Eeeequati0n!!!}`

```python
def egcd(a, b):
    u, u1 = 1, 0
    v, v1 = 0, 1
    while b:
        q = a // b
        u, u1 = u1, u - q * u1
        v, v1 = v1, v - q * v1
        a, b = b, a - q * b
    return u


def get_d(p, n, e):
    q = n / p
    phi = (p - 1) * (q - 1)
    d = egcd(e, phi)
    if d < 0:
        d += phi
    return d


with open("flag.enc", "rb") as input_file:
    n = p * q
    data = input_file.read()
    ct = bytes_to_long(data)
    d = get_d(p, n, e)
    pt = pow(ct, d, n)
    print("pt: " + long_to_bytes(pt))
```

## Other write-ups and resources

* [0day](https://0day.work/0ctf-2016-quals-writeups/)
* [P4 Team](https://github.com/p4-team/ctf/tree/master/2016-03-12-0ctf/equation)
