# Internetwache CTF 2016 : It's Prime Time!

**Category:** Code
**Points:** 60
**Solves:** 338
**Description:**

> Description: We all know that prime numbers are quite important in cryptography. Can you help me to find some?
> 
> 
> Service: 188.166.133.53:11059


## Write-up

Same thing as the previous problem; if you stick the input into `sympy`, it simplifies the task.

```python
import socket
from sympy import nextprime

s = socket.socket()
s.connect(("188.166.133.53", 11059))
print s.recv(1024)

while True:
	problem = s.recv(1024)
	print problem
	N = int(problem.split("Find the next prime number after ")[1].strip(":\n"))
	sol = nextprime(N)
	s.send("%s\n" % sol)
	print s.recv(19)
```

## Other write-ups and resources

* <https://0x90r00t.com/2016/02/22/internetwache-ctf-2016-code-60-its-prime-time-write-up/>
* <https://forum.xeksec.com/f138/t88655/>
