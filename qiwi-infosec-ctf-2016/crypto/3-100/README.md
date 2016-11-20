# Qiwi Infosec CTF 2016 : 3-100

**Category:** Crypto
**Points:** 100
**Solves:**
**Description:**

> The flag is a plaintext
> **Ciphertext**: `GGTTCAATGGGCTTGTCAATGGTTCGCATATCCATGGGCACGGTTCGCGGCTCA`
> **Hint 1:**: Change space to `_`

## Write-up

A brief look at the stream of letters in our ciphertext indicates there are only four characters that occur. With either a bit of Googling or by previous education, we can determine the four letters represent the four nucleobases in DNA:

> C = Cytosine

> G = Guanine

> A = Adenine

> T = Thymine

Unfortunately, this information alone does not tell us how to decrypt the message. Googling `DNA Encryption` or `DNA Cryptography` brings up some interesting pages, but taking a look inside the images Google provides, gives us better insight into the encryption scheme. Within the first ten images, this substitution key appears:

![Cipher Key](http://www.polestarltd.com/ttg/isspeeches/051403/slide14.jpg)

Substituting the nucleobase sequences with their plaintext counterparts (by hand or by computer) gives you `FRIEDRICH MIESCHER`, which by nature of the challenge's hint becomes your flag: `FRIEDRICH_MIESCHER`

## Other write-ups and resources

* [U.S. Coast Guard Academy](https://github.com/USCGA/writeups/tree/master/online_ctfs/qiwi_infosec_ctf_2016/crypto_100_3_COMPLETE)
