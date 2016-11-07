# Internetwache CTF 2016 : Hashdesigner

**Category:** Crypto
**Points:** 70
**Solves:** 68
**Description:**

> Description: There was this student hash design contest. All submissions were crap, but had promised to use the winning algorithm for our important school safe. We hashed our password and got '00006800007d'. Brute force isn't effective anymore and the hash algorithm had to be collision-resistant, so we're good to go, aren't we?
>
>
> Attachment: [crypto70.zip](./crypto70.zip)
>
>
> Service: 188.166.133.53:10009


## Write-up

Writeup by [unicornsasfuel](https://github.com/unicornsasfuel)

We are presented with a custom hash algorithm, one which, upon playing with it, results in a lot of collisions through pure brute force attempts. Contrary to the description, which suggests that neither brute force nor collisions will be effective, this is a very viable route to the solution.

Upon connecting to the service, we are asked for a proof-of-work:

~~~
$ ncat 188.166.133.53 10009
You need to provide your proof of work: A sha1 hash with the last two bytes set to 0. It has 40159607 as the prefix. It should match ^[0-9a-z]{15}$
Enter work:
~~~

We can generate the proof-of-work through brute force with the following python script:

~~~python
import sha
import sys
import itertools
import string

prefix = sys.argv[1]

for combo in itertools.combinations_with_replacement(string.lowercase+string.digits,15-len(prefix)):
   if sha.new(prefix + ''.join(combo)).hexdigest()[-4:] == '0000':
      print sha.new(prefix  + ''.join(combo)).hexdigest()
      print prefix + ''.join(combo)
      break
~~~

Upon providing the proof of work, we are presented with a password prompt. We know the correct hash is `00006800007d`, so we use a modified version of the custom hash algorithm script to perform the brute force for us. However, the service does not accept any password shorter than 18 characters. Unfortunately, we are only told this restriction exists once we've done a brute force already. We modify our script to try only 18 character passwords:

~~~
#!/usr/bin/python2
import binascii
import textwrap
import itertools
import string

def tb(s):
	return bin(int(binascii.hexlify(s),32/2)).lstrip("0b")

def te(s):
	p = 2 << 6
	return s + "0" * (p-len(s)%p)

def tk(s):
	return textwrap.wrap(s, 2<<5) #64

def tj(s):
	return textwrap.wrap(s, 2<<3) #16

def ti(l):
	return int(l,2)

def tr(x,y):
	return (x<< y) or (x >> (16-y));

def th(x):
	return "{0:#0{1}x}".format(x,8)

def tp(x,y):
	s = th(x) + th(y)
	s = s.replace("0x","")
	return s

def myhash(text):

	b = tb(text)

	p = te(b)

	bl = tk(p)

	t11 = 3
	q2 = 5

	tu = [ y**2 for y in range(2<<4>>1)]
	to = [2, 7, 8, 2, 5, 3, 7, 8, 9, 4, 11, 13, 5, 8, 14, 15]

	for i in bl:
		t1 = t11
		t2 = q2

		tl = tj(i)
		tq = map(ti, tl)

		for j in range(16):
			if(j >= 12 ):
				tz = (tq[0] & tq[1]) | ~tq[2]
			elif(j >= 8):
				tz = (tq[3] | tq[2])
			elif(j >= 4):
				tz = (~tq[2] & tq[0]) & (tq[1] | ~tq[0])
			elif(j >= 0):
				tz = (tq[0] | ~tq[2]) | tq[1]
			else:
				pass

			t1 = t1 + tr(tz + tu[j] + tq[j%(16>>2)],to[j])
			t2 = t1 + tr(t2,to[j]) %t1

		t11 += t1
		q2 += t2

	t11 = t11 % 0xFF # Should be 0xFFFFFFFF, right?
	q2 = q2 % 0xFF # Same here... 0xFFFFFFFF

	return tp(t11,q2)


print "Starting brute force"

for combo in itertools.combinations_with_replacement(string.lowercase+string.digits,18):
   if myhash(''.join(combo)) == '00006800007d':
      print "Answer found: %s" % (''.join(combo))
~~~

Using our hash collision generator we eventually come up with a suitable password:

~~~
$ pypy myhash.py
Starting brute force
Answer found: aaaaaaaaaaaaablry6

$ ncat 188.166.133.53 10009
You need to provide your proof of work: A sha1 hash with the last two bytes set to 0. It has 40159607 as the prefix. It should match ^[0-9a-z]{15}$
Enter work:40159607aaainn9
Thank you. Please continue with the login process...
Password: aaaaaaaaaaaaablry6
Logged in!
IW{redacted_flag}
~~~

## Other write-ups and resources

* <https://www.xil.se/post/internetwache-2016-crypto70-kbeckmann/>
* [P4 Team](https://github.com/p4-team/ctf/tree/master/2016-02-20-internetwache/crypto_70)
