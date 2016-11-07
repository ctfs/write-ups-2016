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

* [0x90r00t](https://0x90r00t.com/2016/02/22/internetwache-ctf-2016-code-50-a-numbers-game-write-up/)
* [P4 Team](https://github.com/p4-team/ctf/tree/master/2016-02-20-internetwache/ppc_50)
* <https://github.com/Kileak/CTF/tree/master/2016/internetwache/code/numbersgame>
* <http://cafelinux.info/articles/writeups-internetwache-ctf-2016-a-numbers-game-code50>
* <http://rektsec.github.io/writeups/ctf/internetwatche-2016-ctf-a-numbers-game-code-50/>
* <https://github.com/Execut3/CTF/tree/master/Participated-CTF/2016/InternetWache/coding/code50>
* <https://github.com/WesternCyber/CTF-WriteUp/blob/master/2016/Internetwache/Code/Code50.md>
* <http://err0r-451.ru/internetwache-code-a-numbers-game-50pts/>
* <http://poning.me/2016/03/03/a-numbers-game/>
* [Whitehatters Academy](https://www.whitehatters.academy/internetwache-ctf-code50/)
