# NCL 2016 Preseason : Passwords-4-25

__Category__: Crypto

__Points__: 35

## Write-up

<a href="https://jhalon.github.io/images/ncl7.png"><img src="https://jhalon.github.io/images/ncl7.png"></a>

For this question we are provided with the following encryption algorithm - written in Python..

```python
def encrypt(str):
	ret = ""
	for char in str:
		ret += rot7(rot3(char))
	return ret
```

--

__qbkl dro owksvc ypp dro wksvcobfob__

Since we already have the code, and know how the password is encrypted - all we have to do is enter our encyrpted string.

The code is basically taking a string, and for each character in the string it rotates the letter +3, then +7 and adds it to ret. Once done, it returns the string ret. So for us to get the password from the encryption, just enter the encrypted password and it will reverse it for us.

```python
str = "qbkl dro owksvc ypp dro wksvcobfob"
def encrypt(str):
	ret = ""
	for char in str:
		ret += rot7(rot3(char))
	return ret
```

__Answer: grab the emails off the mailserver__

--

## Other Write-ups and Resources

* [Jack Halon - KKB](https://jhalon.github.io/ncl-crypto/)
