# Internetwache CTF 2016 : A numbers game II

**Category:** Code
**Points:** 70
**Solves:** 199
**Description:**

> Description: Math is used in cryptography, but someone got this wrong. Can you still solve the equations? Hint: You need to encode your answers.
> 
> 
> Attachment: [code70.zip](./code70.zip)
> 
> 
> Service: 188.166.133.53:11071


## Write-up

This is the same thing as the previous problems, except now they give you an encoding function.

```python
def encode(eq):
	out = []
	for c in eq:
		q = bin(ord(c)^(2<<4)).lstrip("0b")
		q = "0" * ((2<<2)-len(q)) + q
		out.append(q)
	b = ''.join(out)
	pr = []
	for x in range(0,len(b),2):
		c = chr(int(b[x:x+2],2)+51)
		pr.append(c)
	s = '.'.join(pr)
	return s
```

The first part converts it to binary, and pads it to 128 characters. The second part converts it to a number in ASCII apparently and joins the array with a bunch of `.`s. Playing around with it produces the following decoding function:

```python
def decode(s):
	pr = map(lambda i: bin(ord(i) - 51)[2:].zfill(2), s.split("."))
	b = "".join(pr)
	m = ""
	for i in range(0, len(b), 8):
		x = b[i:i+8]
		m += chr(int(x, 2) ^ 32)
	return m
```

Once we have these functions, we just rinse and repeat the last two exercises.

```python
import socket
import sys
from sympy import *

s = socket.socket()
s.connect(("188.166.133.53", 11071))
print s.recv(80)

while True:
	problem = ""
	try:
		problem = s.recv(1024).replace("\n", "")
		q = decode(problem.split(": ")[1].strip("\n"))
		print q
		eq = q.split(" = ")
		sol = str(eval("solve(Eq(%s, %s), x)" % (eq[0], eq[1]))[0])
		print encode(sol)
		s.send("%s\n" % encode(sol))

		print s.recv(19)
	except:
		print problem
		sys.exit(1)
```

## Other write-ups and resources

* none yet
