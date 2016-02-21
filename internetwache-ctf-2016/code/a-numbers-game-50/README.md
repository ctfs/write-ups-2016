# Internetwache CTF 2016 : A numbers game

**Category:** Code
**Points:** 50
**Solves:** 360
**Description:**

> Description: People either love or hate math. Do you love it? Prove it! You just need to solve a bunch of equations without a mistake.
> 
> 
> Service: 188.166.133.53:11027


## Write-up

This problem is made trivial with `sympy`. Using `socket` to connect to the server, we simply read the equation, stick it into `sympy`, and then reply.

```python
import socket
from sympy import *

x = symbols("x")

s = socket.socket()
s.connect(("188.166.133.53", 11027))
print s.recv(1024)

while True:
	eq = s.recv(40)
	print "eq: %s" % eq
	lvl = eq.split(".: ")[0]
	eq = eq.split(".: ")[1].split(" = ")
	sol = eval("solve(Eq(%s, %s), x)" % (eq[0], eq[1]))[0]
	s.send("%s\n" % sol)

	print s.recv(19)
```

Flag is `IW{M4TH_1S_34SY}` (not that it really matters now)

## Other write-ups and resources

* <https://0x90r00t.com/2016/02/22/internetwache-ctf-2016-code-50-a-numbers-game-write-up/>
* <https://github.com/p4-team/ctf/tree/master/2016-02-20-internetwache/ppc_50>
