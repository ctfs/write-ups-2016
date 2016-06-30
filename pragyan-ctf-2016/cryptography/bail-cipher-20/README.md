# Pragyan CTF 2016 : BAIL Cipher

**Category:** Cryptography
**Points:** 20
**Solves:** 
**Description:**

>  Bob and Alice have come up with a new encryption to communicate. But they want you to figure out if its possible to decipher their messages easily. Can you decipher it?
> 
> 
>  VGF4ME9GaGxnIHdXMkZqaDVlZiBzeFFtNHY5IGlsdWI=
> 
>  Hint! BAIL is made of BAse and raIL


## Write-up

BAIL Cipher itself says Base64 + Rail Cipher, So the Cipher initially given is `VGF4ME9GaGxnIHdXMkZqaDVlZiBzeFFtNHY5IGlsdWI=` , decoding it with base64 will give `Tax0OFhlg wW2Fjh5ef sxQm4v9 ilub` , Now keeping the Number of Rails = 4 , this would be the Flag `The flag is xwxlQW02mu4FOjvb9hF5`

## Other write-ups and resources

* none yet
